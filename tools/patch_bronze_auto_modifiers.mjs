import fs from "fs";
import path from "path";

const root = path.resolve(".");
const vanillaRoot =
  process.env.EU5_GAME_ROOT ||
  "D:/SteamLibrary/steamapps/common/Europa Universalis V/game";

const sourceDir = path.join(vanillaRoot, "in_game/common/auto_modifiers");
const targetDir = path.join(root, "in_game/common/auto_modifiers");

const removals = {
  "country.txt": [
    "scaled_gov_power_monthly_nahualt_reform_progress",
  ],
  "byzantium.txt": [
    "byz_religion_catholic",
    "byz_religion_orthodox",
    "byz_ruler_religion_orthodox",
    "byz_ruler_religion_catholic",
    "byz_heir_religion_orthodox",
    "byz_heir_religion_catholic",
    "byz_consort_religion_orthodox",
    "byz_consort_religion_catholic",
  ],
};

function normalize(text) {
  return text.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
}

function writeText(file, text) {
  const normalized = normalize(text).replace(/\n/g, "\r\n");
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, normalized, "utf8");
}

function findBlockEnd(text, openIndex) {
  let depth = 0;
  for (let i = openIndex; i < text.length; i++) {
    if (text[i] === "{") depth++;
    else if (text[i] === "}") {
      depth--;
      if (depth === 0) return i;
    }
  }
  return -1;
}

function removeDefinition(text, id) {
  const re = new RegExp(`(^|\\n)([ \\t]*)${id}\\s*=\\s*\\{`, "m");
  const match = re.exec(text);
  if (!match) return { text, removed: false };
  const lineStart = match.index + match[1].length;
  const open = text.indexOf("{", lineStart);
  const close = findBlockEnd(text, open);
  if (open < 0 || close < 0) {
    throw new Error(`Could not find full block for ${id}`);
  }
  let end = close + 1;
  while (end < text.length && /[ \t]/.test(text[end])) end++;
  if (text[end] === "\n") end++;
  return {
    text: `${text.slice(0, lineStart)}# Bronze Era: removed ${id}; it referenced a vanilla religion removed by the total conversion.\n${text.slice(end)}`,
    removed: true,
  };
}

let report = "Bronze Era auto modifier patch report\n";
report += "=====================================\n\n";

for (const [fileName, ids] of Object.entries(removals)) {
  const source = path.join(sourceDir, fileName);
  const target = path.join(targetDir, fileName);
  let text = normalize(fs.readFileSync(source, "utf8"));
  report += `${fileName}\n`;
  for (const id of ids) {
    const result = removeDefinition(text, id);
    text = result.text;
    report += `- ${id}: ${result.removed ? "removed" : "not found"}\n`;
  }
  writeText(target, text);
  report += "\n";
}

writeText(path.join(root, "tools/bronze_auto_modifier_patch_report.txt"), report);
console.log("Patched Bronze Era auto modifiers.");
