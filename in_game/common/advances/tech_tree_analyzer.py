import re
import json
import csv
from collections import Counter, defaultdict
from pathlib import Path


# ------------------------------------------------------------
# 1. READ AND CLEAN THE COMMENTED SOURCE FILE
# ------------------------------------------------------------

def clean_file(path):
    """
    Remove the leading '#' used to comment out the original file.
    The actual indentation and structure are retained.
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned = []

    for line in lines:
        line = line.rstrip("\n")
        line = re.sub(r"^\s*#\s?", "", line)
        cleaned.append(line)

    return "\n".join(cleaned)


# ------------------------------------------------------------
# 2. EXTRACT TOP-LEVEL TECH BLOCKS
# ------------------------------------------------------------

def extract_techs(text):
    """
    Find top-level NAME = { ... } blocks.

    A brace counter is used instead of a giant regex so nested
    structures such as potential = { OR = { ... } } work correctly.
    """
    techs = []
    lines = text.splitlines()

    current_name = None
    current_lines = []
    brace_depth = 0

    for line in lines:
        stripped = line.strip()

        if current_name is None:
            match = re.match(r"^([A-Za-z0-9_]+)\s*=\s*\{", stripped)

            if match:
                current_name = match.group(1)
                current_lines = [line]
                brace_depth = line.count("{") - line.count("}")
            continue

        current_lines.append(line)

        brace_depth += line.count("{")
        brace_depth -= line.count("}")

        if brace_depth == 0:
            techs.append({
                "name": current_name,
                "text": "\n".join(current_lines)
            })

            current_name = None
            current_lines = []
            brace_depth = 0

    return techs


# ------------------------------------------------------------
# 3. EXTRACT TOP-LEVEL STATEMENTS FROM EACH TECH
# ------------------------------------------------------------

def parse_top_level_statements(tech_text):
    """
    Parse statements immediately inside a tech block.

    Returns entries such as:
        ("age", "age_2_renaissance", None)
        ("land_morale", "0.25", None)
        ("potential", None, "{...}")
        ("ai_weight", None, "{...}")

    Nested blocks are preserved as blocks rather than being flattened.
    """
    lines = tech_text.splitlines()

    # Ignore the first line: tech_name = {
    if not lines:
        return []

    body = lines[1:]

    statements = []
    i = 0

    while i < len(body):
        line = body[i].strip()

        if not line or line == "}":
            i += 1
            continue

        # Simple assignment.
        match = re.match(r"^([A-Za-z0-9_]+)\s*=\s*(.+)$", line)

        if not match:
            i += 1
            continue

        key = match.group(1)
        rhs = match.group(2).strip()

        # Block assignment: key = {
        if rhs == "{":
            block_lines = []
            depth = 1
            i += 1

            while i < len(body) and depth > 0:
                current = body[i]

                depth += current.count("{")
                depth -= current.count("}")

                if depth > 0:
                    block_lines.append(current)

                i += 1

            statements.append({
                "key": key,
                "value": None,
                "block": "\n".join(block_lines)
            })

        else:
            statements.append({
                "key": key,
                "value": rhs,
                "block": None
            })
            i += 1

    return statements


# ------------------------------------------------------------
# 4. EFFECT CATEGORIES
# ------------------------------------------------------------

CATEGORIES = {
    "military": {
        "land_morale",
        "military_tactics",
        "army_maintenance_efficiency",
        "regiment_recruit_speed",
        "regiment_reinforcement_speed",
        "supply_depot_capacity",
        "army_initiative",
        "land_morale_recovery",
        "correct_box_chance",
    },

    "naval": {
        "naval_morale",
        "naval_range",
        "naval_initiative",
        "navy_initiative",
        "navy_repair_efficiency",
        "ship_repair_at_sea",
        "ship_repair_at_sea_to_max_strength",
        "blockade_efficiency",
        "global_maritime_presence_modifier",
    },

    "trade": {
        "trade_range",
        "merchant_power_from_maritime",
        "can_sell_bonds",
        "bank_interest",
        "total_loan_capacity_modifier",
        "colonial_range",
    },

    "economy": {
        "global_stone_output_modifier",
        "global_max_rgo_size_modifier",
        "global_max_rgo_size_modifier_in_non_rural",
        "global_monthly_food_modifier",
        "global_rgo_build_time",
        "global_construction_speed",
        "minting_inflation_threshold",
        "global_pop_promotion_speed_modifier",
        "megalopolis_upgrade_cost_modifier",
        "city_upgrade_cost_modifier",
        "town_upgrade_cost_modifier",
    },

    "government": {
        "government_reform_slots",
        "government_size",
        "global_crown_estate_power",
        "revoke_privilege_cost_modifier",
        "grant_privilege_cost_modifier",
        "change_policy_cost_modifier",
        "crown_power_advance_renaissance",
    },

    "diplomacy": {
        "diplomatic_range_modifier",
        "improve_relation_impact",
        "subject_loyalty",
        "subject_opinions",
        "diplomatic_annexation_efficiency",
        "war_no_cb_cost_modifier",
        "power_projection",
    },

    "society": {
        "cultures_capacity",
        "global_nobles_max_literacy",
        "global_burghers_max_literacy",
        "global_clergy_max_literacy",
        "global_pop_promotion_speed_modifier",
        "global_life_expectancy",
        "global_disease_resistance",
        "cultural_influence_modifier",
        "cultural_tradition_modifier",
    },

    "infrastructure": {
        "aqueduct_system_max_level",
        "starting_technology_level",
        "chancery_cap_level",
    },

    "administration": {
        "embrace_institution_cost_modifier",
        "diplomatic_annexation_efficiency",
        "spy_network_construction",
        "change_policy_cost_modifier",
    },
}


UNLOCK_PREFIXES = (
    "unlock_",
)

CONDITION_KEYS = {
    "allow",
    "potential",
}

STRUCTURAL_KEYS = {
    "age",
    "icon",
    "depth",
    "ai_weight",
    "ai_preference_tags",
}

PREREQUISITE_KEYS = {
    "requires",
}


# ------------------------------------------------------------
# 5. CLASSIFY INDIVIDUAL EFFECTS
# ------------------------------------------------------------

def classify_effect(key):
    if key.startswith(UNLOCK_PREFIXES):
        return "unlock"

    if key in CONDITION_KEYS:
        return "condition"

    if key in PREREQUISITE_KEYS:
        return "prerequisite"

    if key in STRUCTURAL_KEYS:
        return "structural"

    for category, effects in CATEGORIES.items():
        if key in effects:
            return category

    # Useful fallback based on names.
    lowered = key.lower()

    if any(word in lowered for word in ("army", "regiment", "land_morale", "military", "combat")):
        return "military"

    if any(word in lowered for word in ("naval", "navy", "ship", "blockade", "maritime")):
        return "naval"

    if any(word in lowered for word in ("trade", "merchant", "loan", "bond")):
        return "trade"

    if any(word in lowered for word in ("diplomatic", "subject", "relation", "opinion", "annexation")):
        return "diplomacy"

    if any(word in lowered for word in ("government", "privilege", "crown", "policy")):
        return "government"

    if any(word in lowered for word in ("food", "rgo", "construction", "output", "promotion", "cost")):
        return "economy"

    return "uncategorized"


# ------------------------------------------------------------
# 6. DETERMINE WHETHER A TECH IS A SIMPLE BONUS TECH
# ------------------------------------------------------------

def classify_tech(tech):
    """
    Classify the overall nature of the technology.

    This is deliberately conservative:
      bonus_only       = only direct effects, no unlocks/conditions
      unlock           = contains an unlock
      conditional      = has allow/potential
      mixed            = multiple kinds of meaningful effects
      structural_only  = no meaningful gameplay effect detected
    """

    statements = tech["statements"]

    meaningful = []
    has_unlock = False
    has_condition = False
    has_requires = False

    for statement in statements:
        key = statement["key"]
        category = classify_effect(key)

        if category == "structural":
            continue

        if category == "prerequisite":
            has_requires = True
            continue

        if category == "condition":
            has_condition = True
            continue

        meaningful.append(category)

        if category == "unlock":
            has_unlock = True

    unique_meaningful = set(meaningful)

    if has_condition and has_unlock:
        return "conditional + unlock"

    if has_condition:
        return "conditional"

    if has_unlock:
        if len(unique_meaningful) == 1:
            return "unlock"
        return "unlock + bonus"

    if not meaningful:
        return "no classified effect"

    if len(unique_meaningful) == 1:
        return "bonus only"

    return "mixed bonus"


# ------------------------------------------------------------
# 7. ANALYZE EACH TECH
# ------------------------------------------------------------

def analyze_tech(raw_tech):
    statements = parse_top_level_statements(raw_tech["text"])

    requires = []
    conditions = []
    effects = []

    for statement in statements:
        key = statement["key"]
        category = classify_effect(key)

        if category == "prerequisite":
            requires.append(statement["value"])
        elif category == "condition":
            conditions.append({
                "type": key,
                "content": statement["block"]
            })
        elif category not in {"structural"}:
            effects.append({
                "key": key,
                "value": statement["value"],
                "category": category,
                "block": statement["block"]
            })

    tech = {
        "name": raw_tech["name"],
        "requires": requires,
        "conditions": conditions,
        "effects": effects,
        "categories": sorted(set(e["category"] for e in effects)),
        "classification": None,
    }

    tech["classification"] = classify_tech({
        "name": raw_tech["name"],
        "statements": statements
    })

    return tech


# ------------------------------------------------------------
# 8. STATISTICAL SUMMARY
# ------------------------------------------------------------

def build_summary(techs):
    total = len(techs)

    def pct(count):
        return round((count / total * 100), 1) if total else 0.0

    category_counts = Counter()
    effect_counts = Counter()
    effect_category = {}
    classification_counts = Counter()

    requires_count = 0
    condition_count = 0

    for tech in techs:
        classification_counts[tech["classification"]] += 1

        if tech["requires"]:
            requires_count += 1

        if tech["conditions"]:
            condition_count += 1

        for category in tech["categories"]:
            category_counts[category] += 1

        for effect in tech["effects"]:
            key = effect["key"]
            effect_counts[key] += 1
            effect_category[key] = effect["category"]

    return {
        "total_techs": total,

        "tech_classifications": [
            {
                "name": name,
                "count": count,
                "proportion": pct(count)
            }
            for name, count in classification_counts.most_common()
        ],

        "categories": [
            {
                "name": name,
                "count": count,
                "proportion": pct(count)
            }
            for name, count in category_counts.most_common()
        ],

        "access": {
            "with_requires": {
                "count": requires_count,
                "proportion": pct(requires_count)
            },
            "with_conditions": {
                "count": condition_count,
                "proportion": pct(condition_count)
            }
        },

        "effects": [
            {
                "name": name,
                "category": effect_category[name],
                "count": count,
                "proportion": pct(count)
            }
            for name, count in effect_counts.most_common()
        ]
    }


# ------------------------------------------------------------
# 9. PRINT HUMAN-READABLE REPORT
# ------------------------------------------------------------

def print_report(summary):
    total = summary["total_techs"]

    def line(name, count, proportion):
        print(f"{name:45} {count:3} / {total:<3} ({proportion:5.1f}%)")

    print("\n" + "=" * 70)
    print("TECHNOLOGY TREE ANALYSIS")
    print("=" * 70)

    print(f"\nTOTAL TECHNOLOGIES: {total}")

    print("\nTECH CLASSIFICATIONS")
    print("-" * 70)

    for item in summary["tech_classifications"]:
        line(item["name"], item["count"], item["proportion"])

    print("\nEFFECT CATEGORIES")
    print("-" * 70)

    for item in summary["categories"]:
        line(item["name"], item["count"], item["proportion"])

    print("\nACCESS / PREREQUISITES")
    print("-" * 70)

    access = summary["access"]

    for name, item in access.items():
        readable = name.replace("_", " ")
        line(readable, item["count"], item["proportion"])

    print("\nINDIVIDUAL EFFECTS")
    print("-" * 70)

    for item in summary["effects"]:
        label = f"{item['name']} [{item['category']}]"
        line(label, item["count"], item["proportion"])

    print("\n" + "=" * 70)


# ------------------------------------------------------------
# 10. SAVE MACHINE-READABLE OUTPUT
# ------------------------------------------------------------

def save_json(summary, techs, path):
    data = {
        "summary": summary,
        "technologies": techs
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_csv(techs, path):
    rows = []

    for tech in techs:
        for effect in tech["effects"]:
            rows.append({
                "tech": tech["name"],
                "classification": tech["classification"],
                "category": effect["category"],
                "effect": effect["key"],
                "value": effect["value"] or "",
                "has_requires": bool(tech["requires"]),
                "has_condition": bool(tech["conditions"]),
            })

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "tech",
                "classification",
                "category",
                "effect",
                "value",
                "has_requires",
                "has_condition",
            ]
        )

        writer.writeheader()
        writer.writerows(rows)


# ------------------------------------------------------------
# 11. MAIN PROGRAM
# ------------------------------------------------------------

def main():
    # Ask for the tech-tree filename.
    # The file is expected to be in the same directory as this script.
    filename = input("Enter the tech tree filename: ").strip()

    if not filename:
        print("No filename provided.")
        input("Press Enter to exit...")
        return

    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / filename

    if not input_path.is_file():
        print(f"File not found: {input_path}")
        input("Press Enter to exit...")
        return

    try:
        # Read the selected file as plain text regardless of its extension.
        text = clean_file(input_path)

        raw_techs = extract_techs(text)

        techs = [
            analyze_tech(tech)
            for tech in raw_techs
        ]

        summary = build_summary(techs)

        print_report(summary)

        # Save output beside the script.
        output_base = input_path.stem
        output_json = script_dir / f"{output_base}_analysis.json"
        output_csv = script_dir / f"{output_base}_effects.csv"

        save_json(summary, techs, output_json)
        save_csv(techs, output_csv)

        print(f"\nDetailed JSON saved to: {output_json}")
        print(f"Effect CSV saved to:   {output_csv}")

    except Exception as error:
        print("\nAN ERROR OCCURRED:")
        print(f"{type(error).__name__}: {error}")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()