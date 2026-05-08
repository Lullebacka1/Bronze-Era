import fs from "fs";
import path from "path";

const root = path.resolve(".");

const tagMap = new Map(Object.entries({
  ALASIYA: "ALASI",
  AMURRU: "AMURU",
  ASSYRIA: "ASYRI",
  BALEARES: "BALES",
  BERITOS: "BERIT",
  BYBLOS: "BYBLO",
  CARTEI: "CARTI",
  EL_ARGAR: "ARGAR",
  ELYMIAN: "ELYMI",
  HABIRU: "HABIR",
  HAJASA: "HAJAS",
  HAPALLA: "HAPAL",
  IAPYGIA: "IAPYG",
  KASSITES: "KASSI",
  KUWALBASSA: "KUWAL",
  MALAKA: "MALAK",
  MITANNI: "MITAN",
  NURAGIC: "NURAG",
  PARTHA: "PARTH",
  SICANI: "SICAN",
  SICELS: "SICEL",
  TARDESSOS: "TARTS",
  TRIPOLI: "TRPOL",
  UGARIT: "UGART",
  WILUSA: "WILUS",
}));

const files = [
  "main_menu/setup/start/10_countries.txt",
  "in_game/setup/countries/_default.txt",
  "in_game/setup/location_painter/00_location_painter.txt",
  "main_menu/localization/english/Bronze_country_names_l_english.yml",
  "tools/generate_bronze_culture_overhaul.mjs",
  "tools/apply_bronze_country_culture_status.mjs",
  "tools/bronze_country_culture_status_report.txt",
];

function readText(rel) {
  return fs.readFileSync(path.join(root, rel), "utf8").replace(/\r\n/g, "\n").replace(/\r/g, "\n");
}

function writeText(rel, text) {
  const normalized = text.replace(/\r+\n/g, "\n").replace(/\r/g, "\n").replace(/\n/g, "\r\n");
  fs.writeFileSync(path.join(root, rel), normalized, "utf8");
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

let replacements = 0;
for (const rel of files) {
  const file = path.join(root, rel);
  if (!fs.existsSync(file)) continue;
  let text = readText(rel);
  for (const [oldTag, newTag] of tagMap) {
    const re = new RegExp(`(?<![A-Za-z0-9_])${escapeRegExp(oldTag)}(?![A-Za-z0-9_])`, "g");
    text = text.replace(re, () => {
      replacements++;
      return newTag;
    });
    const keyedRe = new RegExp(`(?<![A-Za-z0-9_])${escapeRegExp(oldTag)}(?=_)`, "g");
    text = text.replace(keyedRe, () => {
      replacements++;
      return newTag;
    });
  }
  writeText(rel, text);
}

console.log(`Shortened ${tagMap.size} country tags with ${replacements} replacements.`);
