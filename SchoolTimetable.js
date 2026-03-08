// School Timetable Widget for Scriptable (Large)
// ASCII-only source file

// --- Timetable Data ---
// Days: Mon=0, Tue=1, Wed=2, Thu=3, Fri=4
// Periods indexed 0-8 (P1-P9)
var SUBJECTS = [
  ["Maths",     "English",   "French",   "DCG",       "Free"    ], // P1
  ["Maths",     "Physics",   "English",  "Chemistry", "Free"    ], // P2
  ["Chemistry", "Physics",   "Gaeilge",  "Chemistry", "Gaeilge" ], // P3
  ["DCG",       "Gaeilge",   "PE",       "Gaeilge",   "Free"    ], // P4
  ["French",    "DCG",       "Physics",  "English",   "English" ], // P5
  ["Free",      "DCG",       "DCG",      "Maths",     "Maths"   ], // P6
  ["Gaeilge",   "Free",      "Free",     "French",    "Chemistry"], // P7
  ["English",   "Maths",     "Maths",    "French",    "Physics" ], // P8
  ["English",   "Chemistry", "Free",     "Free",      "Free"    ]  // P9
];

// Bell schedule: minutes from midnight
function mins(h, m) { return h * 60 + m; }

// Each slot: label, start, end, subjIdx (-1 = break/lunch)
var SLOTS = [
  { lbl: "P1",  start: mins(9,0),   end: mins(9,40),  si: 0 },
  { lbl: "P2",  start: mins(9,40),  end: mins(10,20), si: 1 },
  { lbl: "P3",  start: mins(10,20), end: mins(11,0),  si: 2 },
  { lbl: "BRK", start: mins(11,0),  end: mins(11,15), si: -1 },
  { lbl: "P4",  start: mins(11,15), end: mins(11,55), si: 3 },
  { lbl: "P5",  start: mins(11,55), end: mins(12,35), si: 4 },
  { lbl: "P6",  start: mins(12,35), end: mins(13,15), si: 5 },
  { lbl: "LCH", start: mins(13,15), end: mins(14,0),  si: -1 },
  { lbl: "P7",  start: mins(14,0),  end: mins(14,40), si: 6 },
  { lbl: "P8",  start: mins(14,40), end: mins(15,20), si: 7 },
  { lbl: "P9",  start: mins(15,20), end: mins(16,0),  si: 8 }
];

var SCHOOL_START = mins(9, 0);
var SCHOOL_END   = mins(16, 0);

// --- Colours stored as hex strings so alpha variants can be constructed ---
var BG_HEX = {
  "Maths":     "#1A3A5C",
  "English":   "#3A1A1A",
  "French":    "#1A3A1A",
  "DCG":       "#2A1A3A",
  "Chemistry": "#3A2A1A",
  "Physics":   "#1A2A3A",
  "Gaeilge":   "#3A1A2A",
  "PE":        "#1A3A2A",
  "Free":      "#111318"
};

var FG_HEX = {
  "Maths":     "#5B9BD5",
  "English":   "#D55B5B",
  "French":    "#5BD58A",
  "DCG":       "#A05BD5",
  "Chemistry": "#D5A05B",
  "Physics":   "#5BA0D5",
  "Gaeilge":   "#D55B9B",
  "PE":        "#5BD5C0",
  "Free":      "#555A66"
};

// Abbreviations for narrow cells
var ABBREV = {
  "Maths":     "Math",
  "English":   "Eng",
  "French":    "Fr",
  "DCG":       "DCG",
  "Chemistry": "Chem",
  "Physics":   "Phys",
  "Gaeilge":   "Gaei",
  "PE":        "PE",
  "Free":      "---"
};

// Theme colours
var C_BG          = new Color("#070A12");
var C_HEADER_BG   = new Color("#0D1120");
var C_TODAY_COL   = new Color("#141A2E");
var C_ACTIVE_ROW  = new Color("#1B2440");
var C_DIVIDER     = new Color("#0A0D18");
var C_LABEL       = new Color("#8892AA");
var C_DAY         = new Color("#C8D0E0");
var C_TODAY_DAY   = new Color("#FFFFFF");
var C_TIME        = new Color("#444A5A");
var C_BADGE_BG    = new Color("#1A2540");
var C_BADGE_ACT   = new Color("#2A4080");
var C_BADGE_TXT   = new Color("#E0E8FF");
var C_WEEKEND     = new Color("#8892AA");
var C_DIV_TXT     = new Color("#3A4060");

// --- Helpers ---
function getNow() {
  var d = new Date();
  return {
    jsDay: d.getDay(),
    mins:  d.getHours() * 60 + d.getMinutes(),
    secs:  d.getSeconds()
  };
}

// JS day: 0=Sun,1=Mon,...,6=Sat => school day Mon=0..Fri=4, -1=weekend
function schoolDay(jsDay) {
  if (jsDay >= 1 && jsDay <= 5) return jsDay - 1;
  return -1;
}

function getCurrentSlot(m) {
  for (var i = 0; i < SLOTS.length; i++) {
    if (m >= SLOTS[i].start && m < SLOTS[i].end) return i;
  }
  return -1;
}

function getNextSlot(m) {
  for (var i = 0; i < SLOTS.length; i++) {
    if (SLOTS[i].start > m) return i;
  }
  return -1;
}

function fmtTime(m) {
  var h = Math.floor(m / 60);
  var mm = m % 60;
  var ap = h >= 12 ? "PM" : "AM";
  var h12 = h % 12;
  if (h12 === 0) h12 = 12;
  return h12 + ":" + (mm < 10 ? "0" : "") + mm + ap;
}

function fmtCountdown(totalSecs) {
  var m = Math.floor(totalSecs / 60);
  var s = totalSecs % 60;
  if (m > 0) {
    return m + "m " + (s < 10 ? "0" : "") + s + "s";
  }
  return s + "s";
}

function getStatus(now, sd) {
  var m = now.mins;
  var s = now.secs;
  if (sd < 0) {
    return { line1: "WEEKEND", line2: "", active: false };
  }
  if (m < SCHOOL_START) {
    var wait = (SCHOOL_START - m) * 60 - s;
    return { line1: "School in", line2: fmtCountdown(wait), active: false };
  }
  if (m >= SCHOOL_END) {
    return { line1: "SCHOOL DONE", line2: "", active: false };
  }
  var si = getCurrentSlot(m);
  if (si >= 0) {
    var slot = SLOTS[si];
    var rem = (slot.end - m) * 60 - s;
    if (slot.si < 0) {
      var name = (slot.lbl === "BRK") ? "BREAK" : "LUNCH";
      return { line1: name, line2: fmtCountdown(rem) + " left", active: true };
    }
    var subj = SUBJECTS[slot.si][sd];
    return { line1: subj, line2: fmtCountdown(rem) + " left", active: true };
  }
  var ni = getNextSlot(m);
  if (ni >= 0) {
    var nslot = SLOTS[ni];
    var wait2 = (nslot.start - m) * 60 - s;
    return { line1: "Next: " + nslot.lbl, line2: fmtCountdown(wait2), active: false };
  }
  return { line1: "SCHOOL DONE", line2: "", active: false };
}

// --- Build widget ---
var widget = new ListWidget();
widget.backgroundColor = C_BG;
widget.refreshAfterDate = new Date(Date.now() + 60000);
widget.setPadding(8, 8, 6, 8);

var now = getNow();
var sd  = schoolDay(now.jsDay);
var curSlot = -1;
if (sd >= 0 && now.mins >= SCHOOL_START && now.mins < SCHOOL_END) {
  curSlot = getCurrentSlot(now.mins);
}
var status = getStatus(now, sd);

// ---- TOP ROW: title + badge ----
var topRow = widget.addStack();
topRow.layoutHorizontally();
topRow.centerAlignContent();

var titleCol = topRow.addStack();
titleCol.layoutVertically();

var t1 = titleCol.addText("TIMETABLE");
t1.font = Font.boldSystemFont(12);
t1.textColor = C_DAY;

var dateObj = new Date();
var dayNames = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
var monNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
var dateStr = dayNames[dateObj.getDay()] + " " + dateObj.getDate() + " " + monNames[dateObj.getMonth()];
var t2 = titleCol.addText(dateStr);
t2.font = Font.systemFont(9);
t2.textColor = C_LABEL;

topRow.addSpacer();

var badge = topRow.addStack();
badge.layoutVertically();
badge.backgroundColor = status.active ? C_BADGE_ACT : C_BADGE_BG;
badge.cornerRadius = 6;
badge.setPadding(4, 8, 4, 8);

var bl1 = badge.addText(status.line1);
bl1.font = Font.boldSystemFont(9);
bl1.textColor = C_BADGE_TXT;
bl1.lineLimit = 1;
bl1.minimumScaleFactor = 0.7;

if (status.line2 !== "") {
  var bl2 = badge.addText(status.line2);
  bl2.font = Font.systemFont(8);
  bl2.textColor = C_LABEL;
  bl2.lineLimit = 1;
}

widget.addSpacer(4);

// ---- HEADER ROW: day names ----
var dayNames5 = ["MON", "TUE", "WED", "THU", "FRI"];

var hdr = widget.addStack();
hdr.layoutHorizontally();
hdr.backgroundColor = C_HEADER_BG;
hdr.cornerRadius = 4;
hdr.setPadding(3, 4, 3, 4);

// blank label col
var hblank = hdr.addStack();
var hblankT = hblank.addText("    ");
hblankT.font = Font.systemFont(7);

for (var d = 0; d < 5; d++) {
  hdr.addSpacer();
  var hcell = hdr.addStack();
  hcell.layoutVertically();
  hcell.centerAlignContent();
  var hdt = hcell.addText(dayNames5[d]);
  hdt.font = Font.boldSystemFont(9);
  hdt.textColor = (d === sd) ? C_TODAY_DAY : C_DAY;
  hdt.minimumScaleFactor = 0.6;
}

widget.addSpacer(2);

// ---- PERIOD ROWS ----
for (var slot = 0; slot < SLOTS.length; slot++) {
  var sl = SLOTS[slot];
  var isDiv = (sl.si < 0);
  var isActive = (curSlot === slot);

  var row = widget.addStack();
  row.layoutHorizontally();
  row.cornerRadius = 3;
  row.setPadding(isDiv ? 1 : 2, 4, isDiv ? 1 : 2, 4);

  if (isDiv) {
    row.backgroundColor = C_DIVIDER;
  } else if (isActive) {
    row.backgroundColor = C_ACTIVE_ROW;
  }

  // Label column (period name + start time)
  var lblCol = row.addStack();
  lblCol.layoutVertically();
  lblCol.centerAlignContent();

  var lblT = lblCol.addText(sl.lbl);
  lblT.font = Font.boldSystemFont(isDiv ? 6 : 7);
  lblT.textColor = isActive ? C_TODAY_DAY : (isDiv ? C_DIV_TXT : C_LABEL);
  lblT.minimumScaleFactor = 0.5;

  if (!isDiv) {
    var tStr = fmtTime(sl.start);
    var tT = lblCol.addText(tStr);
    tT.font = Font.systemFont(6);
    tT.textColor = C_TIME;
    tT.minimumScaleFactor = 0.5;
  }

  // Day columns
  for (var day = 0; day < 5; day++) {
    row.addSpacer();

    var cell = row.addStack();
    cell.layoutVertically();
    cell.centerAlignContent();
    cell.cornerRadius = 3;

    if (isDiv) {
      // Divider: show label in center col only, others blank
      cell.backgroundColor = C_DIVIDER;
      cell.setPadding(1, 4, 1, 4);
      if (day === 2) {
        var divLabel = (sl.lbl === "BRK") ? "- BREAK -" : "- LUNCH -";
        var dlt = cell.addText(divLabel);
        dlt.font = Font.systemFont(6);
        dlt.textColor = C_DIV_TXT;
        dlt.minimumScaleFactor = 0.5;
      } else {
        var dblank = cell.addText(" ");
        dblank.font = Font.systemFont(6);
        dblank.textColor = C_DIVIDER;
      }
    } else {
      var subj = SUBJECTS[sl.si][day];
      var bgHex = BG_HEX[subj] || BG_HEX["Free"];
      var fgHex = FG_HEX[subj] || FG_HEX["Free"];
      var abbr  = ABBREV[subj] || subj;

      var alpha = 0.55;
      if (day === sd && isActive) alpha = 1.0;
      else if (day === sd) alpha = 0.85;

      cell.backgroundColor = new Color(bgHex, alpha);
      cell.setPadding(2, 3, 2, 3);

      var fs = (day === sd && isActive) ? 8 : 7;
      var ct = cell.addText(abbr);
      ct.font = (isActive && day === sd) ? Font.boldSystemFont(fs) : Font.systemFont(fs);
      ct.textColor = new Color(fgHex, (day === sd) ? 1.0 : 0.75);
      ct.minimumScaleFactor = 0.5;
      ct.lineLimit = 1;
    }
  }

  if (slot < SLOTS.length - 1) widget.addSpacer(1);
}

// ---- BOTTOM NOTE for weekend/done ----
if (sd < 0 || now.mins >= SCHOOL_END) {
  widget.addSpacer(3);
  var note = widget.addText(sd < 0 ? "-- WEEKEND --" : "-- SCHOOL DONE --");
  note.font = Font.boldSystemFont(10);
  note.textColor = C_WEEKEND;
  note.centerAlignText();
}

// ---- Present ----
if (config.runsInWidget) {
  Script.setWidget(widget);
} else {
  widget.presentLarge();
}
Script.complete();
