/* The Tail — the marquee view.

   Each entrant owes 24 proposals. A shot clock runs 24 seconds. Both are a bounded
   window in which you must produce something non-obvious: early clock is rehearsed,
   late clock is where you either manufacture something or force a bad shot. So the
   clock reads down the middle and the two offenses run either side of it.

   HONESTY CONTRACT. Until real panel verdicts exist, the onset is not a panel's
   judgment — it is a literal word-prefix match this file computes. So in preview the
   controls are labelled by the match width they set, never by a panel's name, and the
   page does not claim isolation it has not got. Panel names and the isolation claim
   appear only once `data.yields` actually carries a panel's REPETITION ONSET. The
   tournament has already convicted one entrant for dressing a judgment as a
   measurement (HANDOFF.md:327), and a hub that did the same would be worse. */
(function () {
  var el = window.HUB.el;
  var CLOCK = 24;
  var BAND = 17;
  var WIDTHS = [2, 3, 4];

  function opening(text, words) {
    return String(text).toLowerCase().replace(/[^a-z0-9 ]/g, " ")
      .split(/\s+/).filter(Boolean).slice(0, words).join(" ");
  }

  /* First position whose opening move repeats one already played, plus the earlier
     position it repeats — the commissioner has to be able to check the claim. */
  function computeOnset(ideas, words) {
    var seen = {};
    for (var i = 0; i < ideas.length; i++) {
      var key = opening(ideas[i], words);
      if (!key) { continue; }
      if (seen[key] !== undefined) { return { onset: i + 1, echoes: seen[key] + 1 }; }
      seen[key] = i;
    }
    return { onset: null, echoes: null };
  }

  /* Preview controls name the parameter they set. Real ones name the panel. */
  function controls(data, game) {
    var given = (data.yields || {})[game.g];
    if (given) {
      return (data.panels || []).map(function (panel) {
        return { key: panel.name, label: panel.name, real: true };
      });
    }
    return WIDTHS.map(function (w) {
      return { key: String(w), label: w + "-word match", width: w, real: false };
    });
  }

  function reading(pick, ideas, given) {
    if (pick.real) { return given || { onset: null, echoes: null }; }
    return computeOnset(ideas, pick.width);
  }

  /* The early clock is where the repeated move usually sits, so every tick carries its
     proposal and the echoed one is marked. A claim you cannot inspect is not evidence. */
  function rail(ideas, read, side) {
    var ticks = el("div", { cls: "tail-ticks side-" + side });
    for (var n = 1; n < BAND; n++) {
      var mark = el("i", {
        cls: (read.onset && n >= read.onset ? "stalled" : "")
           + (read.echoes === n ? " echo" : "")
           + (read.onset === n ? " onset" : "") });
      mark.setAttribute("title", n + ". " + (ideas[n - 1] || ""));
      ticks.appendChild(mark);
    }
    return ticks;
  }

  function railSide(ideas, read, side) {
    var wrap = el("div", { cls: "rail-side side-" + side });
    wrap.appendChild(rail(ideas, read, side));
    if (read.onset && read.onset < BAND) {
      wrap.appendChild(el("div", { cls: "rail-tag", text: label(read) }));
    }
    return wrap;
  }

  function label(read) {
    if (!read.onset) { return ""; }
    return read.onset + " repeats " + read.echoes;
  }

  function verdict(read) {
    if (!read.onset) { return "ran to the buzzer"; }
    return "stalled at " + read.onset + " — " + (CLOCK - read.onset + 1) + " of 24 spent repeating";
  }

  function rule(side) {
    var bar = el("div", { cls: "onset-rule side-" + side });
    bar.appendChild(el("span", { cls: "onset-tag" }));
    return bar;
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

    var opts = controls(data, game);
    var chosen = opts.filter(function (o) { return o.key === window.HUB.state.panel; })[0] || opts[0];
    var given = (data.yields || {})[game.g] || {};

    container.appendChild(el("h2", { text: "Where each one stopped being surprising" }));
    var note = el("p", { cls: "counter" });
    container.appendChild(note);

    var head = el("div", { cls: "tail-head" });
    var nameA = el("div", { cls: "side-a" }), gap = el("div", {}), nameB = el("div", { cls: "side-b" });
    [[nameA, game.A], [null], [nameB, game.B]].forEach(function (pair) {
      if (!pair[0]) { head.appendChild(gap); return; }
      var meta = (data.field || {})[pair[1]] || { name: pair[1] };
      pair[0].appendChild(el("h3", { text: meta.name }));
      pair[0].appendChild(el("div", { cls: "who" }));
      head.appendChild(pair[0]);
    });
    container.appendChild(head);

    var railRow = el("div", { cls: "tail-rail" });
    container.appendChild(railRow);

    var grid = el("div", { cls: "tail-body" });
    var cellsA = [], cellsB = [];
    for (var n = BAND; n <= CLOCK; n++) {
      var left = el("div", { cls: "tail-row side-a" });
      left.appendChild(el("span", { cls: "tail-text", text: a.ideas[n - 1] || "—" }));
      var right = el("div", { cls: "tail-row side-b" });
      right.appendChild(el("span", { cls: "tail-text", text: b.ideas[n - 1] || "—" }));
      cellsA.push(left); cellsB.push(right);
      grid.appendChild(left);
      grid.appendChild(el("div", {
        cls: "tail-n" + (n === CLOCK ? " buzzer" : ""), text: String(n) }));
      grid.appendChild(right);
    }
    var ruleA = rule("a"), ruleB = rule("b");
    grid.appendChild(ruleA); grid.appendChild(ruleB);
    container.appendChild(grid);

    /* The horizontal rule belongs to the band. An onset on the rail is marked there
       instead, so the line never pins to a position it does not actually occupy. */
    function place(bar, cells, read) {
      if (!read.onset || read.onset < BAND) { bar.classList.add("clear"); return; }
      bar.classList.remove("clear");
      var target = cells[Math.min(read.onset - BAND, cells.length - 1)];
      var top = target.getBoundingClientRect().top - grid.getBoundingClientRect().top;
      bar.style.transform = "translateY(" + top + "px)";
      bar.firstChild.textContent = label(read);
    }

    /* Update in place. Re-rendering through HUB.go wipes the root, and a rule drawn on
       a brand-new node cannot travel — which is the whole point of the gesture. */
    function apply(pick) {
      var readA = reading(pick, a.ideas, given[pick.key + ":A"]);
      var readB = reading(pick, b.ideas, given[pick.key + ":B"]);
      note.textContent = "Game " + game.g + ". Judged on ideas 17 to 24, the late clock. "
        + (pick.real
            ? "Read by the " + pick.label + " panel."
            : "No panel has read these yet. The line below is a literal "
              + pick.width + "-word prefix match computed in the page.");
      nameA.lastChild.textContent = verdict(readA);
      nameB.lastChild.textContent = verdict(readB);
      railRow.textContent = "";
      railRow.appendChild(railSide(a.ideas, readA, "a"));
      railRow.appendChild(el("div", { cls: "rail-label", text: "1–16" }));
      railRow.appendChild(railSide(b.ideas, readB, "b"));
      cellsA.forEach(function (box, i) {
        box.classList.toggle("dead", !!(readA.onset && i + BAND >= readA.onset)); });
      cellsB.forEach(function (box, i) {
        box.classList.toggle("dead", !!(readB.onset && i + BAND >= readB.onset)); });
      var settle = function () {
        place(ruleA, cellsA, readA); place(ruleB, cellsB, readB);
      };
      requestAnimationFrame(settle);
      if (document.fonts && document.fonts.ready) { document.fonts.ready.then(settle); }
      if (window.HUB.onResize) { window.HUB.onResize(settle); }
    }

    var toggle = el("div", { cls: "panel-toggle" });
    opts.forEach(function (opt) {
      var button = el("button", { text: opt.label });
      button.setAttribute("aria-pressed", String(opt.key === chosen.key));
      button.addEventListener("click", function () {
        window.HUB.state.panel = opt.key;
        toggle.querySelectorAll("button").forEach(function (other) {
          other.setAttribute("aria-pressed", String(other === button)); });
        apply(opt);
      });
      toggle.appendChild(button);
    });
    container.appendChild(toggle);
    container.appendChild(el("p", { cls: "counter",
      text: chosen.real
        ? "Three panels read the same proposals in isolation. Switch between them and the line moves."
        : "Widening the match flags less. Hover any early-clock tick to read its proposal." }));

    apply(chosen);
  });
}());
