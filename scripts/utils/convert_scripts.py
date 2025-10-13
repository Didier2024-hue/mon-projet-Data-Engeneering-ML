#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import ast
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
import nbformat

def is_comment_line(line: str) -> bool:
    """Détermine si une ligne est un commentaire."""
    stripped = line.strip()
    return stripped.startswith('#') and not stripped.startswith('#!')

def is_multiline_comment_start(line: str) -> bool:
    """Détecte le début d'un commentaire multiligne."""
    return '"""' in line or "'''" in line

def extract_multiline_comment(line: str) -> Tuple[str, bool]:
    """Extrait le contenu d'un commentaire multiligne."""
    if '"""' in line:
        delimiter = '"""'
    else:
        delimiter = "'''"
    
    parts = line.split(delimiter)
    if len(parts) >= 3:
        # Commentaire complet sur une ligne
        return parts[1], False
    elif len(parts) == 2:
        # Début ou fin de commentaire
        return parts[1] if line.startswith(delimiter) else parts[0], True
    return "", True

def parse_python_to_cells(content: str) -> List[Dict[str, Any]]:
    """
    Parse le code Python et crée des cellules Jupyter professionnelles.
    """
    lines = content.split('\n')
    cells = []
    current_cell_lines = []
    current_cell_type = 'code'
    in_multiline_comment = False
    multiline_content = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Gestion des commentaires multilignes
        if in_multiline_comment:
            comment_part, still_in_comment = extract_multiline_comment(line)
            if comment_part:
                multiline_content.append(comment_part)
            
            if not still_in_comment:
                # Fin du commentaire multiligne
                if multiline_content:
                    md_content = '\n'.join(multiline_content)
                    cells.append(nbformat.v4.new_markdown_cell(md_content))
                in_multiline_comment = False
                multiline_content = []
                current_cell_type = 'code'
            continue
        
        # Début de commentaire multiligne
        if is_multiline_comment_start(line):
            in_multiline_comment = True
            comment_part, still_in_comment = extract_multiline_comment(line)
            if comment_part:
                multiline_content.append(comment_part)
            if not still_in_comment:
                # Commentaire sur une seule ligne
                if multiline_content:
                    md_content = '\n'.join(multiline_content)
                    cells.append(nbformat.v4.new_markdown_cell(md_content))
                in_multiline_comment = False
                multiline_content = []
            continue
        
        # Commentaires simples
        if is_comment_line(line):
            if current_cell_type == 'code' and current_cell_lines:
                # Terminer la cellule code précédente
                code_content = '\n'.join(current_cell_lines)
                cells.append(nbformat.v4.new_code_cell(code_content))
                current_cell_lines = []
            
            current_cell_type = 'markdown'
            md_line = re.sub(r'^#\s*', '', line).rstrip()
            if md_line:  # Ne pas ajouter de lignes vides
                current_cell_lines.append(md_line)
        
        # Code Python
        else:
            if current_cell_type == 'markdown' and current_cell_lines:
                # Terminer la cellule markdown précédente
                md_content = '\n'.join(current_cell_lines)
                cells.append(nbformat.v4.new_markdown_cell(md_content))
                current_cell_lines = []
            
            current_cell_type = 'code'
            current_cell_lines.append(line)
    
    # Ajouter la dernière cellule
    if current_cell_lines:
        if current_cell_type == 'code':
            code_content = '\n'.join(current_cell_lines)
            cells.append(nbformat.v4.new_code_cell(code_content))
        else:
            md_content = '\n'.join(current_cell_lines)
            cells.append(nbformat.v4.new_markdown_cell(md_content))
    
    # Nettoyer les cellules vides
    cells = [cell for cell in cells if cell['source'].strip()]
    
    return cells

def create_jupyter_notebook(cells: List[Dict[str, Any]]) -> nbformat.NotebookNode:
    """Crée un vrai notebook Jupyter avec toutes les métadonnées."""
    notebook = nbformat.v4.new_notebook()
    notebook['cells'] = cells
    
    # Métadonnées complètes
    notebook['metadata'] = {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'name': 'python',
            'version': '3.9.0',
            'mimetype': 'text/x-python',
            'codemirror_mode': {
                'name': 'ipython',
                'version': 3
            },
            'pygments_lexer': 'ipython3',
            'nbconvert_exporter': 'python',
            'file_extension': '.py'
        }
    }
    
    return notebook

def convert_python_file_to_notebook(py_path: Path, output_dir: Path) -> bool:
    """Convertit un fichier Python en notebook Jupyter professionnel."""
    try:
        print(f"🔄 Conversion de: {py_path.name}")
        
        # Lire le contenu
        content = py_path.read_text(encoding='utf-8')
        
        # Parser en cellules
        cells = parse_python_to_cells(content)
        
        if not cells:
            print(f"⚠️  Fichier vide ou sans contenu convertible: {py_path.name}")
            return False
        
        # Créer le notebook
        notebook = create_jupyter_notebook(cells)
        
        # Nom du fichier de sortie
        notebook_name = py_path.stem + ".ipynb"
        notebook_path = output_dir / notebook_name
        
        # Écrire le notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(notebook, f, version=4)
        
        # Statistiques
        code_cells = sum(1 for cell in cells if cell['cell_type'] == 'code')
        md_cells = sum(1 for cell in cells if cell['cell_type'] == 'markdown')
        
        print(f"✅ {py_path.name} → {notebook_name} ({code_cells}⧵{md_cells})")
        return True
        
    except Exception as e:
        print(f"❌ Erreur avec {py_path.name}: {str(e)}")
        return False

def main():
    """Conversion principale."""
    scripts_dir = Path("/home/datascientest/cde/scripts/")
    notebooks_dir = Path("/home/datascientest/cde/notebooks/")
    
    print("🎯 CONVERSION VERS DE VRAIS NOTEBOOKS JUPYTER")
    print("=" * 60)
    print(f"📁 Source: {scripts_dir}")
    print(f"📁 Destination: {notebooks_dir}")
    print("=" * 60)
    
    # Vérifications
    if not scripts_dir.exists():
        print("❌ Le dossier scripts n'existe pas!")
        return 1
    
    notebooks_dir.mkdir(exist_ok=True)
    
    # Trouver les fichiers Python
    py_files = list(scripts_dir.rglob("*.py"))
    py_files = [f for f in py_files if f.name != "__init__.py"]
    
    print(f"📊 {len(py_files)} fichiers Python trouvés")
    print("-" * 60)
    
    # Conversion
    success_count = 0
    for py_file in py_files:
        if convert_python_file_to_notebook(py_file, notebooks_dir):
            success_count += 1
    
    # Rapport final
    print("=" * 60)
    print(f"🎉 CONVERSION TERMINÉE!")
    print(f"✅ {success_count} fichiers convertis avec succès")
    print(f"❌ {len(py_files) - success_count} échecs")
    print(f"📁 Notebooks disponibles dans: {notebooks_dir}")
    
    # Vérification
    nb_files = list(notebooks_dir.glob("*.ipynb"))
    if nb_files:
        print(f"\n📋 {len(nb_files)} notebooks créés:")
        for nb_file in nb_files:
            print(f"   • {nb_file.name}")
    
    return 0

if __name__ == "__main__":
    exit(main())
