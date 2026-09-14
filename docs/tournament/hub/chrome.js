/* Chrome: phase banner, matchup switcher, view routing. Holds no tournament data. */
(function () {
  var views = {};
  var state = { view: "runfloor", game: 1 };
  var root = null;
  var ALL = { runfloor: true, bracket: true, entrant: true };  // views with no single subject
  var PHASE_RANK = { runfloor: 0, output: 1, mechanism: 2 };
  var NEEDS_PHASE = { tail: 1 };  // unlisted views are available at every phase  // views with no single subject

  function data() { return window.HUB_DATA || null; }

  function el(tag, attrs, kids) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") { node.textContent = attrs[k]; }
      else if (k === "cls") { node.className = attrs[k]; }
      else { node.setAttribute(k, attrs[k]); }
    });
    (kids || []).forEach(function (kid) { node.appendChild(kid); });
    return node;
  }

  function games() { return (data() && data().games) || []; }

  function label(game) {
    var f = data().field;
    var a = f[game.A] || { name: game.A };
    var b = f[game.B] || { name: game.B };
    return "Game " + game.g + " · " + a.name + " v " + b.name;
  }

  function switcher() {
    var box = el("div", { cls: "switcher" });
    if (ALL[state.view] || !games().length) { return box; }
    var current = games().filter(function (g) { return g.g === state.game; })[0] || games()[0];
    var list = el("ul", { hidden: "hidden" });
    var toggle = el("button", { text: label(current) + "  ▾", "aria-expanded": "false" });
    toggle.addEventListener("click", function () {
      var open = list.hidden;
      list.hidden = !open;
      toggle.setAttribute("aria-expanded", String(open));
    });
    games().forEach(function (game) {
      var pick = el("button", { text: label(game) });
      pick.addEventListener("click", function () { go(state.view, game.g); });
      list.appendChild(el("li", {}, [pick]));
    });
    box.appendChild(toggle);
    box.appendChild(list);
    return box;
  }

  function step(delta) {
    if (ALL[state.view] || !games().length) { return; }
    var order = games().map(function (g) { return g.g; });
    var at = order.indexOf(state.game);
    go(state.view, order[(at + delta + order.length) % order.length]);
  }

  function banner() {
    var d = data();
    var bar = el("div", { cls: "chrome" });
    bar.appendChild(el("span", { cls: "mark", text: "The 99th Idea Bracket" }));
    if (d) {
      // The phase drives the whole environment: house lights up before anything is at
      // stake, the bowl once scores are released. Stamped on the root so CSS owns it.
      document.documentElement.setAttribute("data-phase", d.phase);
      bar.appendChild(el("span", { cls: "live", text: d.phase }));
      if (d.demo) {
        bar.appendChild(el("span", { cls: "preview",
          text: "preview data — no official run generated" }));
      }
      bar.appendChild(el("span", { text: "built " + d.generated }));
    } else {
      bar.appendChild(el("span", { text: "no data" }));
    }
    bar.appendChild(switcher());
    return bar;
  }

  function released(name) {
    var d = data();
    var rank = d ? (PHASE_RANK[d.phase] || 0) : 0;
    return rank >= (NEEDS_PHASE[name] || 0);
  }

  function tabs() {
    var bar = el("div", { cls: "tabs" });
    Object.keys(views).filter(released).forEach(function (name) {
      var button = el("button", { text: name });
      if (name === state.view) { button.setAttribute("aria-current", "true"); }
      button.addEventListener("click", function () { go(name, state.game); });
      bar.appendChild(button);
    });
    return bar;
  }

  var resizers = [];
  window.addEventListener("resize", function () {
    resizers.forEach(function (fn) { fn(); });
  });

  function render() {
    if (!root) { return; }
    resizers.length = 0;
    root.textContent = "";
    var wrap = el("div", { cls: "wrap" });
    wrap.appendChild(banner());
    if (!data()) {
      wrap.appendChild(el("p", { cls: "muted",
        text: "No data file loaded. Run build_hub.py and publish its output alongside this page." }));
      root.appendChild(wrap);
      return;
    }
    wrap.appendChild(tabs());
    var body = el("div", {});
    views[state.view](body, data(), state);
    wrap.appendChild(body);
    root.appendChild(wrap);
  }

  function go(view, game) {
    // Mutate rather than reassign: window.HUB.state exports this object by reference,
    // and a reassignment here would leave that export pointing at a stale snapshot.
    state.view = views[view] ? view : state.view;
    state.game = game || state.game;
    render();
  }

  window.HUB = {
    state: state,
    el: el,
    register: function (name, render_) { views[name] = render_; },
    onResize: function (fn) { resizers.push(fn); },
    go: go,
    mount: function (node) {
      root = node;
      if (released("tail")) { state.view = "tail"; }
      document.addEventListener("keydown", function (event) {
        if (event.key === "ArrowRight") { step(1); }
        if (event.key === "ArrowLeft") { step(-1); }
      });
      render();
    }
  };
}());
