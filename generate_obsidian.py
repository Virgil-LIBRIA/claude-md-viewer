#!/usr/bin/env python3
"""
generate_obsidian.py — Point Zero Glossary Kit Generator
Generates 88 Obsidian-ready .md notes + Notion CSV from glossaire_pz.json

Usage:
    python generate_obsidian.py
    python generate_obsidian.py --input glossaire_pz.json --output obsidian/
    python generate_obsidian.py --notion   (also generates Notion CSV)
    python generate_obsidian.py --validate (only checks JSON structure)
    python generate_obsidian.py --stats    (print corpus statistics)
"""

import json
import os
import csv
import re
import argparse
from pathlib import Path


# ─── Helpers ────────────────────────────────────────────────────────────────

def slug_to_title(slug: str, terms_map: dict) -> str:
    """Convert kebab-case slug to display name from terms index."""
    return terms_map.get(slug, slug.replace('-', ' ').title())


def safe_filename(terme: str) -> str:
    """Turn a term name into a safe .md filename."""
    name = terme.lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '-', name.strip())
    return name + '.md'


def tensor_to_str(tensor: dict) -> str:
    if not tensor:
        return '{}'
    pairs = ', '.join(f'{k}: {v}' for k, v in tensor.items())
    return '{' + pairs + '}'


# ─── Validators ─────────────────────────────────────────────────────────────

REQUIRED_FIELDS = ['id', 'terme', 'definition_courte']

def validate_terms(terms: list) -> list:
    """Return list of validation errors."""
    errors = []
    seen_ids = set()
    all_ids = {t['id'] for t in terms}

    for i, term in enumerate(terms):
        prefix = f"[{i}] {term.get('terme', '?')}"

        for field in REQUIRED_FIELDS:
            if field not in term or not term[field]:
                errors.append(f"{prefix} — missing required field: {field}")

        tid = term.get('id', '')
        if tid in seen_ids:
            errors.append(f"{prefix} — duplicate id: {tid}")
        seen_ids.add(tid)

        for rel in term.get('relations', []):
            if rel not in all_ids:
                errors.append(f"{prefix} — broken relation: '{rel}' not found")

    return errors


# ─── Obsidian generator ──────────────────────────────────────────────────────

def generate_obsidian_note(term: dict, terms_map: dict) -> str:
    """Generate a single Obsidian .md note from a term dict."""
    aliases = json.dumps(term.get('aliases', []), ensure_ascii=False)
    tensor = tensor_to_str(term.get('tensor', {}))

    relations = term.get('relations', [])
    relations_links = '\n'.join(
        f"- [[{slug_to_title(r, terms_map)}]]"
        for r in relations
    ) if relations else '_Aucune relation définie._'

    pilier = term.get('pilier', '')
    pilier_link = f'[[{pilier}]]' if pilier else '_Non classé_'

    definition_complete = term.get('definition', term.get('definition_courte', ''))

    note = f"""---
terme: {term['terme']}
pilier: {pilier}
categorie: {term.get('categorie', '')}
aliases: {aliases}
ile: {term.get('ile', '')}
tensor: {tensor}
relations_count: {len(relations)}
---

# {term['terme']}

**{term.get('definition_courte', '')}**

{definition_complete}

## Concepts liés

{relations_links}

## Pilier

{pilier_link}
"""
    return note


def generate_obsidian(terms: list, output_dir: str, terms_map: dict) -> int:
    """Write all Obsidian notes to output_dir. Returns count."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    count = 0

    for term in terms:
        content = generate_obsidian_note(term, terms_map)
        filename = safe_filename(term['terme'])
        filepath = Path(output_dir) / filename
        filepath.write_text(content, encoding='utf-8')
        count += 1

    print(f"✅ {count} notes Obsidian générées dans {output_dir}/")
    return count


# ─── Notion CSV generator ────────────────────────────────────────────────────

def generate_notion_csv(terms: list, output_path: str) -> None:
    """Export terms as a Notion-importable CSV."""
    fieldnames = [
        'terme', 'pilier', 'categorie', 'ile',
        'definition_courte', 'relations_count', 'aliases'
    ]
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for term in terms:
            writer.writerow({
                'terme': term.get('terme', ''),
                'pilier': term.get('pilier', ''),
                'categorie': term.get('categorie', ''),
                'ile': term.get('ile', ''),
                'definition_courte': term.get('definition_courte', ''),
                'relations_count': len(term.get('relations', [])),
                'aliases': ', '.join(term.get('aliases', [])),
            })

    print(f"✅ CSV Notion généré : {output_path}")


# ─── Stats ───────────────────────────────────────────────────────────────────

def print_stats(terms: list) -> None:
    total = len(terms)
    total_relations = sum(len(t.get('relations', [])) for t in terms)
    avg_relations = total_relations / total if total else 0

    piliers = {}
    for t in terms:
        p = t.get('pilier', 'N/A')
        piliers[p] = piliers.get(p, 0) + 1

    print(f"\n📊 Statistiques du corpus")
    print(f"   Termes totaux      : {total}")
    print(f"   Relations totales  : {total_relations}")
    print(f"   Moyenne relations  : {avg_relations:.1f} par terme")
    print(f"\n   Distribution par pilier:")
    for pilier, count in sorted(piliers.items(), key=lambda x: -x[1]):
        bar = '█' * (count // 1)
        print(f"   {pilier:<12} {count:>3}  {bar}")
    print()


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Generate Obsidian notes + Notion CSV from glossaire_pz.json'
    )
    parser.add_argument('--input',    default='glossaire_pz.json', help='Source JSON file')
    parser.add_argument('--output',   default='obsidian/',         help='Obsidian output directory')
    parser.add_argument('--notion',   action='store_true',         help='Also generate Notion CSV')
    parser.add_argument('--validate', action='store_true',         help='Only validate JSON, no output')
    parser.add_argument('--stats',    action='store_true',         help='Print corpus statistics')
    args = parser.parse_args()

    # Load JSON
    json_path = Path(args.input)
    if not json_path.exists():
        print(f"❌ Fichier introuvable : {json_path}")
        print(f"   Place glossaire_pz.json dans le même dossier que ce script.")
        return

    with open(json_path, encoding='utf-8') as f:
        terms = json.load(f)

    print(f"📂 {len(terms)} termes chargés depuis {json_path}")

    # Build lookup map
    terms_map = {t['id']: t['terme'] for t in terms}

    # Validate
    errors = validate_terms(terms)
    if errors:
        print(f"\n⚠️  {len(errors)} erreur(s) de validation :")
        for err in errors:
            print(f"   {err}")
        if args.validate:
            return
        print("   (poursuite malgré les erreurs)\n")
    else:
        print("✅ Validation OK — aucune erreur")

    if args.validate:
        return

    # Stats
    if args.stats:
        print_stats(terms)

    # Generate Obsidian
    generate_obsidian(terms, args.output, terms_map)

    # Generate Notion CSV
    if args.notion:
        notion_path = Path('notion') / 'glossaire_pz.csv'
        generate_notion_csv(terms, str(notion_path))

    print("\n🎬 Done. Prêt pour Gumroad.")


if __name__ == '__main__':
    main()
