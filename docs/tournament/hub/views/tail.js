/* The Tail — the marquee view.

   Each entrant owes 24 proposals. A shot clock runs 24 seconds. Both are a bounded
   window in which you must produce something non-obvious: early clock is rehearsed,
   late clock is where you either manufacture something or force a bad shot. So the
   clock reads down the middle and the two offenses run either side of it.

   Ideas 1-16 compress to a rail. The judged band is 17-24 and only it carries text.
   The onset rule marks where an entrant began repeating itself — the offense stalling.

   When real panel verdicts exist the onset comes from them. Until then it is COMPUTED
   from repetition actually present in the proposals: three prefix widths stand in for
   three judges reading the same list with different strictness. They disagree, which
   is the point — watching the rule move between panels is the evidence. */
(function () {
  var el = window.HUB.el;
  var CLOCK = 24;
  var BAND = 17;
  var DIAMOND = "◆";

  function opening(text, words) {
    return String(text).toLowerCase().replace(/[^a-z0-9 ]/g, " ")
      .split(/\s+/).filter(Boolean).slice(0, words).join(" ");
  }

  /* First position whose opening move repeats one already played. */
  function computeOnset(ideas, words) {
    var seen = {};
    for (var i = 0; i < ideas.length; i++) {
      var key = opening(ideas[i], words);
      if (!key) { continue; }
      if (seen[key]) { return i + 1; }
      seen[key] = true;
    }
    return null;
  }

  /* The late-clock proposal carrying the most vocabulary not already spent. */
  function computeStrongest(ideas) {
    var spent = {}, best = null, bestScore = -1;
    ideas.forEach(function (idea, index) {
      var words = opening(idea, 40).split(" ").filter(Boolean);
      if (index + 1 >= BAND) {
        var fresh = words.filter(function (w) { return w.length > 3 && !spent[w]; }).length;
        var score = fresh / Math.max(words.length, 1);
        if (score > bestScore) { bestScore = score; best = index + 1; }
      }
      words.forEach(function (w) { spent[w] = true; });
    });
    return best;
  }

  function readings(data) {
    return (data.panels || []).map(function (panel, index) {
      return { name: panel.name, widths: [2, 3, 4][index] || 3 };
    });
  }

  function sideReading(reading, ideas, given) {
    if (given) { return given; }
    return {
      onset: computeOnset(ideas, reading.widths),
      strongest: computeStrongest(ideas)
    };
  }

  function rail(onset, side) {
    var ticks = el("div", { cls: "tail-ticks side-" + side });
    for (var n = 1; n < BAND; n++) {
      ticks.appendChild(el("i", { cls: onset && n >= onset ? "stalled" : "" }));
    }
    return ticks;
  }

  function onsetLabel(onset) {
    return onset < BAND ? "repeating since " + onset : "repetition from " + onset;
  }

  function cell(ideas, read, n, side) {
    var onset = read.onset;
    var dead = onset && n >= onset;
    var opens = onset && (n === onset || (onset < BAND && n === BAND));
    var box = el("div", {
      cls: "tail-row side-" + side + (dead ? " dead" : "") + (opens ? " onset" : "") });
    if (opens) { box.appendChild(el("span", { cls: "onset-tag", text: onsetLabel(onset) })); }
    /* A strongest mark inside the dead run would contradict the run. */
    if (read.strongest === n && !dead) {
      box.appendChild(el("span", { cls: "tail-strong", text: DIAMOND }));
    }
    box.appendChild(el("span", { cls: "tail-text", text: ideas[n - 1] || "—" }));
    return box;
  }

  /* One grid, not two columns: a row's three cells must share a baseline, and
     independent columns drift the moment one side's text wraps further. */
  function band(a, b, readA, readB) {
    var grid = el("div", { cls: "tail-body" });
    for (var n = BAND; n <= CLOCK; n++) {
      grid.appendChild(cell(a.ideas, readA, n, "a"));
      grid.appendChild(el("div", {
        cls: "tail-n" + (n === CLOCK ? " buzzer" : ""), text: String(n) }));
      grid.appendChild(cell(b.ideas, readB, n, "b"));
    }
    return grid;
  }

  function verdict(read) {
    if (!read.onset) { return "ran to the buzzer"; }
    var spent = CLOCK - read.onset + 1;
    return "stalled at " + read.onset + " — " + spent + " of 24 spent repeating";
  }

  function header(data, game, readA, readB) {
    var head = el("div", { cls: "tail-head" });
    [["a", game.A, readA], [null], ["b", game.B, readB]].forEach(function (entry) {
      if (!entry[0]) { head.appendChild(el("div", {})); return; }
      var meta = (data.field || {})[entry[1]] || { name: entry[1] };
      var box = el("div", { cls: "side-" + entry[0] });
      box.appendChild(el("h3", { text: meta.name }));
      box.appendChild(el("div", { cls: "who", text: verdict(entry[2]) }));
      head.appendChild(box);
    });
    return head;
  }

  window.HUB.register("tail", function (container, data, state) {
    var game = (data.games || []).filter(function (g) { return g.g === state.game; })[0]
      || (data.games || [])[0];
    if (!game) {
      container.appendChild(el("p", { cls: "muted", text: "No draw loaded." }));
      return;
    }

    var tails = data.tails || {};
    var a = tails[game.A], b = tails[game.B];
    if (!a || !b) {
      container.appendChild(el("h2", { text: "The tail" }));
      container.appendChild(el("p", { cls: "muted",
        text: "No proposals yet for this matchup. Generate the official runs, or build "
            + "the hub with --demo to preview the view against scrimmage text." }));
      return;
    }

    var panels = readings(data);
    var chosen = window.HUB.state.panel || (panels[0] || {}).name;
    var pick = panels.filter(function (p) { return p.name === chosen; })[0] || panels[0];
    var given = (data.yields || {})[game.g] || {};
    var readA = sideReading(pick, a.ideas, given[pick.name + ":A"]);
    var readB = sideReading(pick, b.ideas, given[pick.name + ":B"]);

    container.appendChild(el("h2", { text: "Where each one stopped being surprising" }));
    container.appendChild(el("p", { cls: "counter",
      text: "Game " + game.g + ". Judged on ideas 17 to 24, the late clock. "
          + (given[pick.name + ":A"]
              ? "Read by the " + pick.name + " panel."
              : "Preview reading: repetition measured in the proposals themselves.") }));

    container.appendChild(header(data, game, readA, readB));

    var railRow = el("div", { cls: "tail-rail" });
    railRow.appendChild(rail(readA.onset, "a"));
    railRow.appendChild(el("div", { cls: "rail-label", text: "1–16" }));
    railRow.appendChild(rail(readB.onset, "b"));
    container.appendChild(railRow);

    container.appendChild(band(a, b, readA, readB));

    var toggle = el("div", { cls: "panel-toggle" });
    panels.forEach(function (panel) {
      var button = el("button", { text: panel.name });
      button.setAttribute("aria-pressed", String(panel.name === chosen));
      button.addEventListener("click", function () {
        window.HUB.state.panel = panel.name;
        window.HUB.go("tail", state.game);
      });
      toggle.appendChild(button);
    });
    container.appendChild(toggle);
    container.appendChild(el("p", { cls: "counter",
      text: "Three panels read the same proposals in isolation. Switch between them "
          + "and the line moves." }));
  });
}());
