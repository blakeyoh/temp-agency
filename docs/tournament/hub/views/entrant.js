/* Entrant cards: definition, the not-native claim, R32 status, evidence state. */
(function () {
  var el = window.HUB.el;

  function card(entry) {
    var box = el("div", { cls: "card" });
    var head = el("h3", {});
    head.appendChild(el("span", { cls: "code", text: entry.code + " " }));
    head.appendChild(el("span", { text: entry.name + (entry.owner ? " ◆" : "") }));
    box.appendChild(head);
    if (entry.note) {
      box.appendChild(el("p", { cls: "muted", text: entry.note }));
    }
    box.appendChild(el("p", { text: entry.summary }));
    if (entry.not_native) {
      box.appendChild(el("p", { cls: "muted", text: "Not native: " + entry.not_native }));
    }
    if (entry.status) {
      box.appendChild(el("p", { cls: "muted", text: entry.status }));
    }
    box.appendChild(el("p", {
      text: "Evidence: " + (entry.state || "—") + (entry.flag ? " · " + entry.flag : "")
    }));
    return box;
  }

  window.HUB.register("entrant", function (container, data) {
    container.appendChild(el("h2", { text: "Entrants" }));
    container.appendChild(el("p", { cls: "muted",
      text: "The sixteen still standing. ◆ marks an owner idea." }));
    var grid = el("div", { cls: "cards" });
    data.floor.forEach(function (row) {
      var entry = data.field[row.code];
      if (entry) { grid.appendChild(card(entry)); }
    });
    container.appendChild(grid);
  });
}());
