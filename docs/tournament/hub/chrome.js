/* Chrome: phase banner, matchup switcher, view routing. Holds no tournament data. */
(function () {
  var views = {};
  var state = { view: "runfloor", game: 1 };
  var root = null;
  var ALL = { runfloor: true, bracket: true, entrant: true };  // views with no single subject

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
    bar.appendChild(el("span", { text: "The 99th Idea Bracket" }));
    bar.appendChild(el("span", { cls: "live", text: "● " + (d ? d.phase : "no data") }));
    if (d) { bar.appendChild(el("span", { cls: "muted", text: "built " + d.generated })); }
    bar.appendChild(switcher());
    return bar;
  }

  function tabs() {
    var bar = el("div", { cls: "tabs" });
    Object.keys(views).forEach(function (name) {
      var button = el("button", { text: name });
      if (name === state.view) { button.setAttribute("aria-current", "true"); }
      button.addEventListener("click", function () { go(name, state.game); });
      bar.appendChild(button);
    });
    return bar;
  }

  function render() {
    if (!root) { return; }
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
    go: go,
    mount: function (node) {
      root = node;
      document.addEventListener("keydown", function (event) {
        if (event.key === "ArrowRight") { step(1); }
        if (event.key === "ArrowLeft") { step(-1); }
      });
      render();
    }
  };
}());
