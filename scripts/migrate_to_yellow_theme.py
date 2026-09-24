"""
Script de migration de la charte graphique : Passage d'Orange à Jaune Premium / Or d'Exception.
Préserve l'identité de marque propre du service 'Orange Money' pour les paiements.
"""
import os
import re

TEMPLATES_DIR = 'templates'
CSS_FILE = 'static/css/main.css'

HEX_REPLACEMENTS = [
    ('#f97316', '#eab308'),
    ('#ea580c', '#ca8a04'),
    ('#c2410c', '#a16207'),
    ('#fb923c', '#facc15'),
    ('#fdba74', '#fde047'),
    ('#fed7aa', '#fef08a'),
    ('#ffedd5', '#fef9c3'),
    ('#fff7ed', '#fefce8'),
    ('249 115 22', '234 179 8'),
    ('234 88 12', '202 138 4'),
    ('194 65 12', '161 98 7'),
]

TAILWIND_PATTERNS = [
    (r'(\b|[:\-_/])orange-50\b', r'\1amber-50'),
    (r'(\b|[:\-_/])orange-100\b', r'\1amber-100'),
    (r'(\b|[:\-_/])orange-200\b', r'\1amber-200'),
    (r'(\b|[:\-_/])orange-300\b', r'\1amber-300'),
    (r'(\b|[:\-_/])orange-400\b', r'\1amber-400'),
    (r'(\b|[:\-_/])orange-500\b', r'\1amber-500'),
    (r'(\b|[:\-_/])orange-600\b', r'\1amber-600'),
    (r'(\b|[:\-_/])orange-700\b', r'\1amber-700'),
    (r'(\b|[:\-_/])orange-800\b', r'\1amber-800'),
    (r'(\b|[:\-_/])orange-900\b', r'\1amber-900'),
    (r'(\b|[:\-_/])orange-950\b', r'\1amber-950'),
    (r'(\b|[:\-_/])orange\b(?=\s|["\'`\}])', r'\1amber-500'),
]

CUSTOM_PATTERNS = [
    ('shadow-glow-orange', 'shadow-glow-yellow'),
    ('gradient-border-orange', 'gradient-border-yellow'),
    ('selection:bg-orange-500 selection:text-white', 'selection:bg-amber-400 selection:text-neutral-900'),
]

def migrate_content(content):
    # 1. Protéger les références à Orange Money
    markers = [
        ('orange_money', '___SAFE_OM_LOWER___'),
        ('Orange Money', '___SAFE_OM_TITLE___'),
        ('ORANGE MONEY', '___SAFE_OM_UPPER___'),
        ('orange money', '___SAFE_OM_SPACE_LOWER___'),
        ('Orange money', '___SAFE_OM_CAP_LOWER___'),
    ]
    for orig, marker in markers:
        content = content.replace(orig, marker)
    
    # 2. Remplacer les codes hexadécimaux
    for old_hex, new_hex in HEX_REPLACEMENTS:
        content = content.replace(old_hex, new_hex)
        content = content.replace(old_hex.upper(), new_hex)
    
    # 3. Remplacer les classes Tailwind
    for pattern, repl in TAILWIND_PATTERNS:
        content = re.sub(pattern, repl, content)
        
    for old_str, new_str in CUSTOM_PATTERNS:
        content = content.replace(old_str, new_str)
        
    # 4. Rétablir Orange Money
    for orig, marker in markers:
        content = content.replace(marker, orig)
        
    return content

def run_migration():
    modified_files = []
    
    # Scanner les templates
    for root, _, files in os.walk(TEMPLATES_DIR):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    orig = f.read()
                new_content = migrate_content(orig)
                if new_content != orig:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    modified_files.append(file_path)
                    print(f"Modifié : {file_path}")

    # CSS
    if os.path.exists(CSS_FILE):
        with open(CSS_FILE, 'r', encoding='utf-8') as f:
            orig = f.read()
        new_content = migrate_content(orig)
        if new_content != orig:
            with open(CSS_FILE, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified_files.append(CSS_FILE)
            print(f"Modifié : {CSS_FILE}")
            
    print(f"\nMigration terminée avec succès sur {len(modified_files)} fichiers.")

if __name__ == '__main__':
    run_migration()
