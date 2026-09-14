/* Bracket: eight game cards with the state of both sides. */
(function () {
  var el = window.HUB.el;

  function stageOf(floor, code) {
    var found = floor.filter(function (r) { return r.code === code; })[0];
    return found ? found.stage : "pending";
  }

  function side(data, code) {
    var meta = data.field[code] || { name: code, owner: false };
    var line = el("div", {});
    line.appendChild(el("span", { cls: "code", text: code + " " }));
    line.appendChild(el("span", { text: meta.name + (meta.owner ? " ◆" : "") }));
    line.appendChild(el("div", { cls: "stageline stage-" + stageOf(data.floor, code),
                                 text: stageOf(data.floor, code) }));
    return line;
  }

  function card(data, game) {
    var box = el("div", { cls: "card" });
    box.appendChild(el("h3", { text: "Game " + game.g }));
    box.appendChild(side(data, game.A));
    box.appendChild(el("p", { cls: "muted", text: "versus" }));
    box.appendChild(side(data, game.B));
    box.addEventListener("click", function () { window.HUB.go("entrant", game.g); });
    return box;
  }

  window.HUB.register("bracket", function (container, data) {
    container.appendChild(el("h2", { text: "Sweet 16" }));
    container.appendChild(el("p", { cls: "muted",
      text: "Eight games. Draw seed " + (data.games.length ? "frozen" : "unset") + "." }));
    var grid = el("div", { cls: "cards" });
    data.games.forEach(function (game) { grid.appendChild(card(data, game)); });
    container.appendChild(grid);
  });
}());
