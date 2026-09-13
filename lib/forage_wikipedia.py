"""Bounded E2 Wikipedia random-revision fetcher and independent verifier.

Exports:
    fetch_random(endpoint) -> dict
    verify_remote(artifact, completed_utc) -> list[str]

Uses only the Python standard library. All network access is restricted to
the allowlist of MediaWiki API endpoints over HTTPS.
"""

import hashlib
import json
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urlencode, urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

__all__ = ["fetch_random", "verify_remote"]

_ALLOWED_ENDPOINTS = frozenset({
    "https://en.wikipedia.org/w/api.php",
    "https://simple.wikipedia.org/w/api.php",
})
_ALLOWED_HOSTS = frozenset(
    urlparse(e).hostname for e in _ALLOWED_ENDPOINTS
)

_USER_AGENT = "TempAgencyHarness/0.1 (https://github.com/blakeyoh/temp-agency)"
_TIMEOUT_SECONDS = 20
_MAX_RESPONSE_BYTES = 8 * 1024 * 1024

_RANDOM_PARAMS = {
    "action": "query",
    "generator": "random",
    "grnnamespace": "0",
    "grnlimit": "1",
    "prop": "revisions",
    "rvprop": "ids|timestamp|content",
    "rvslots": "main",
    "format": "json",
    "formatversion": "2",
}

_VERIFY_PARAMS_BASE = {
    "action": "query",
    "prop": "revisions",
    "rvprop": "ids|timestamp|content",
    "rvslots": "main",
    "format": "json",
    "formatversion": "2",
}


def _check_endpoint(endpoint):
    """Validate endpoint is an exact allowlisted HTTPS API URL. Return it."""
    if not isinstance(endpoint, str) or endpoint not in _ALLOWED_ENDPOINTS:
        raise ValueError(
            "endpoint must be one of %s" % sorted(_ALLOWED_ENDPOINTS)
        )
    return endpoint


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Wikipedia API redirects are not permitted")


def _http_get(url):
    """GET url with UA, timeout, and 8 MiB bound. Return (body, final_url).

    Raises ValueError on any transport-level failure, redirect outside the
    allowlist, oversized body, or non-200 status.
    """
    request = Request(url, headers={"User-Agent": _USER_AGENT})
    opener = build_opener(_NoRedirect())
    try:
        response = opener.open(request, timeout=_TIMEOUT_SECONDS)
    except Exception as exc:  # noqa: BLE001 - any transport error is fatal
        raise ValueError("request failed: %r" % (exc,))
    try:
        final_url = response.geturl()
        parsed = urlparse(final_url)
        if parsed.scheme != "https" or parsed.hostname not in _ALLOWED_HOSTS:
            raise ValueError("redirect outside allowed endpoints: %s" % final_url)
        chunks = []
        total = 0
        while True:
            chunk = response.read(65536)
            if not chunk:
                break
            total += len(chunk)
            if total > _MAX_RESPONSE_BYTES:
                raise ValueError("response exceeds 8 MiB bound")
            chunks.append(chunk)
        body = b"".join(chunks)
        status = getattr(response, "status", None) or response.getcode()
        headers = response.headers
    finally:
        response.close()
    if status != 200:
        raise ValueError("HTTP status %s from %s" % (status, final_url))
    return body, headers


def _parse_json(body):
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("invalid JSON response: %r" % (exc,))


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _parse_http_date(headers):
    raw = headers.get("Date")
    if not raw:
        raise ValueError("missing HTTP Date header")
    try:
        dt = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        raise ValueError("unparseable HTTP Date header: %r" % raw)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _parse_utc_iso(value, label):
    if not isinstance(value, str) or not value:
        raise ValueError("missing %s" % label)
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("unparseable %s: %r" % (label, value))
    if dt.tzinfo is None:
        raise ValueError("%s must include timezone" % label)
    return dt.astimezone(timezone.utc)


def _extract_revision(payload):
    """Validate the query payload schema. Return (page, revision)."""
    if not isinstance(payload, dict):
        raise ValueError("payload is not an object")
    if payload.get("error") is not None or "error" in payload:
        raise ValueError("API error in response")
    query = payload.get("query")
    if not isinstance(query, dict):
        raise ValueError("missing query object")
    pages = query.get("pages")
    if not isinstance(pages, list) or len(pages) != 1:
        raise ValueError("expected exactly one page, got %r" % (pages,))
    page = pages[0]
    if not isinstance(page, dict):
        raise ValueError("page is not an object")
    if "missing" in page or "invalid" in page:
        raise ValueError("page missing or invalid")
    if not _is_int(page.get("pageid")) or page["pageid"] <= 0:
        raise ValueError("invalid pageid")
    if not _is_int(page.get("ns")) or page["ns"] != 0:
        raise ValueError("expected ns == 0")
    title = page.get("title")
    if not isinstance(title, str) or not title:
        raise ValueError("missing or empty title")
    revisions = page.get("revisions")
    if not isinstance(revisions, list) or len(revisions) != 1:
        raise ValueError("expected exactly one revision")
    revision = revisions[0]
    if not isinstance(revision, dict):
        raise ValueError("revision is not an object")
    if not _is_int(revision.get("revid")) or revision["revid"] <= 0:
        raise ValueError("invalid revid")
    _ts = _parse_utc_iso(revision.get("timestamp"), "revision timestamp")
    slots = revision.get("slots")
    if not isinstance(slots, dict):
        raise ValueError("missing slots")
    main = slots.get("main")
    if not isinstance(main, dict):
        raise ValueError("missing main slot")
    content = main.get("content")
    if not isinstance(content, str) or not content:
        raise ValueError("missing or empty content")
    if "texthidden" in main or "texthidden" in revision or "suppressed" in revision:
        raise ValueError("suppressed content")
    return page, revision


def _build_artifact(endpoint, page, revision, response_date):
    content = revision["slots"]["main"]["content"]
    host = urlparse(endpoint).netloc
    return {
        "endpoint": endpoint,
        "pageid": page["pageid"],
        "title": page["title"],
        "revid": revision["revid"],
        "revision_timestamp": revision["timestamp"],
        "response_date": response_date.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "content": content,
        "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "revision_url": "https://%s/w/index.php?oldid=%d"
        % (host, revision["revid"]),
    }


def _fetch_random(endpoint):
    """Fetch one genuine random revision from an allowlisted endpoint.

    Returns the artifact dict; raises ValueError on any failure. No retry,
    no silent alternate draw.
    """
    endpoint = _check_endpoint(endpoint)
    url = endpoint + "?" + urlencode(_RANDOM_PARAMS)
    body, headers = _http_get(url)
    payload = _parse_json(body)
    page, revision = _extract_revision(payload)
    response_date = _parse_http_date(headers)
    rev_dt = _parse_utc_iso(revision["timestamp"], "revision timestamp")
    if rev_dt > response_date:
        raise ValueError("revision timestamp is later than server Date")
    return _build_artifact(endpoint, page, revision, response_date)


def _claim(artifact, key, checker, message, problems):
    value = artifact.get(key) if isinstance(artifact, dict) else None
    if not checker(value):
        problems.append(message)
        return None
    return value


def _verify_remote(artifact, completed_utc):
    """Independently verify an artifact against the same endpoint.

    Returns a list of problem strings; empty list means verified. Network
    or parse failures are recorded as problems, never as verified.
    """
    problems = []

    completed = None
    if isinstance(completed_utc, str) and completed_utc:
        try:
            completed = _parse_utc_iso(completed_utc, "completed_utc")
        except ValueError as exc:
            problems.append(str(exc))
    else:
        problems.append("missing or invalid completed_utc")

    if not isinstance(artifact, dict):
        problems.append("artifact is not a dict")
        return problems

    endpoint = artifact.get("endpoint")
    if not isinstance(endpoint, str) or endpoint not in _ALLOWED_ENDPOINTS:
        problems.append("artifact endpoint not in allowlist")
    claimed_title = artifact.get("title")
    if not isinstance(claimed_title, str) or not claimed_title:
        problems.append("artifact title missing or empty")
    revid = artifact.get("revid")
    if not _is_int(revid) or revid <= 0:
        problems.append("artifact revid missing or invalid")
    pageid = artifact.get("pageid")
    if not _is_int(pageid) or pageid <= 0:
        problems.append("artifact pageid missing or invalid")
    claimed_ts = None
    if isinstance(artifact.get("revision_timestamp"), str):
        try:
            claimed_ts = _parse_utc_iso(
                artifact["revision_timestamp"], "revision_timestamp"
            )
        except ValueError as exc:
            problems.append(str(exc))
    else:
        problems.append("artifact revision_timestamp missing or invalid")
    claimed_date = None
    if isinstance(artifact.get("response_date"), str):
        try:
            raw = artifact["response_date"]
            dt = parsedate_to_datetime(raw)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            claimed_date = dt.astimezone(timezone.utc)
        except (TypeError, ValueError):
            problems.append("artifact response_date unparseable")
    else:
        problems.append("artifact response_date missing or invalid")

    content = artifact.get("content")
    if not isinstance(content, str) or not content:
        problems.append("artifact content missing or empty")
    claimed_hash = artifact.get("content_sha256")
    if not isinstance(claimed_hash, str) or len(claimed_hash) != 64:
        problems.append("artifact content_sha256 missing or invalid")

    if claimed_ts is not None and claimed_date is not None:
        if claimed_ts > claimed_date:
            problems.append("claimed revision_timestamp after response_date")
    if claimed_date is not None and completed is not None:
        if claimed_date > completed:
            problems.append("claimed response_date after completed_utc")

    host_ok = isinstance(endpoint, str) and endpoint in _ALLOWED_ENDPOINTS
    revid_ok = _is_int(revid) and revid > 0
    if not (host_ok and revid_ok):
        return problems

    params = dict(_VERIFY_PARAMS_BASE)
    params["revids"] = str(revid)
    url = endpoint + "?" + urlencode(params)
    try:
        body, headers = _http_get(url)
        payload = _parse_json(body)
        page, revision = _extract_revision(payload)
    except ValueError as exc:
        problems.append("verification fetch failed: %s" % exc)
        return problems

    if "missing" in page or page.get("pageid") != pageid:
        problems.append("pageid mismatch or page missing")
    if revision["revid"] != revid:
        problems.append("revid mismatch")
    remote_ts = _parse_utc_iso(
        revision["timestamp"], "remote revision timestamp"
    )
    if claimed_ts is not None and remote_ts != claimed_ts:
        problems.append("revision timestamp mismatch")
    remote_content = revision["slots"]["main"]["content"]
    remote_hash = hashlib.sha256(
        remote_content.encode("utf-8")
    ).hexdigest()
    if content is not None and remote_content != content:
        problems.append("content mismatch (fabricated or edited)")
    if isinstance(claimed_hash, str) and claimed_hash != remote_hash:
        problems.append("content_sha256 mismatch")

    expected_url = "https://%s/w/index.php?oldid=%d" % (
        urlparse(endpoint).netloc,
        revid,
    )
    if artifact.get("revision_url") != expected_url:
        problems.append("revision_url mismatch")

    return problems


def fetch_random(endpoint):
    """Fetch once; any transport, decoding or schema failure fails the operation."""
    try:
        return _fetch_random(endpoint)
    except Exception as exc:
        raise ValueError("Wikipedia fetch failed: %s" % exc) from exc


def verify_remote(artifact, completed_utc):
    """No network or malformed-data exception may authenticate a claimed artifact."""
    try:
        return _verify_remote(artifact, completed_utc)
    except Exception as exc:
        return ["Wikipedia verification failed: %s" % exc]
