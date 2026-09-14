/* Run Floor: the sixteen official runs and how far each has travelled. */
(function () {
  var el = window.HUB.el;
  var STEPS = ["pending", "dispatched", "recorded", "gated"];

  function counter(rows) {
    var gated = rows.filter(function (r) { return r.stage === "gated"; }).length;
    return gated + " of " + rows.length + " records gated";
  }

  function row(entry, field) {
    var meta = field[entry.code] || { name: entry.code, state: "", flag: "" };
    var cells = [
      el("td", {}, [el("span", { cls: "code", text: entry.code })]),
      el("td", { text: meta.name }),
      el("td", { text: meta.state || "—" }),
      el("td", { cls: "muted", text: meta.flag || "" }),
      el("td", { text: String(entry.receipts) }),
      el("td", {}, [el("span", { cls: "stage-" + entry.stage, text: entry.stage })])
    ];
    var line = el("tr", {});
    cells.forEach(function (cell) { line.appendChild(cell); });
    line.addEventListener("click", function () { window.HUB.go("entrant", null); });
    return line;
  }

  window.HUB.register("runfloor", function (container, data) {
    container.appendChild(el("h2", { text: "The run floor" }));
    container.appendChild(el("p", { cls: "muted", text: counter(data.floor) }));
    var head = el("tr", {});
    ["Code", "Entrant", "Evidence", "Flag", "Receipts", "Stage"].forEach(function (name) {
      head.appendChild(el("th", { text: name }));
    });
    var table = el("table", {}, [el("thead", {}, [head])]);
    var body = el("tbody", {});
    data.floor.forEach(function (entry) { body.appendChild(row(entry, data.field)); });
    table.appendChild(body);
    container.appendChild(el("div", { cls: "scroll" }, [table]));
    container.appendChild(el("p", { cls: "muted",
      text: "Stages: " + STEPS.join(" → ") + ". Stage is observed from repo state, not ruled." }));
  });
}());
