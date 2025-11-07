#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import ast
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
import nbformat
from nbformat import validate
from tqdm import tqdm  # ✅ Progress bar

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
        # Commentaire complet sur une seule ligne
        return parts[1], False
    elif len(parts) == 2:
        # Début ou fin de commentaire
        return parts[1] if line.startswith(delimiter) else parts[0], True
    return "", True

def parse_python_to_cells(content: str) -> List[Dict[str, Any]]:
    """Parse le code Python et crée des cellules Jupyter professionnelles."""
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
                if multiline_content:
                    md_content = '\n'.join(multiline_content)
                    cells.append(nbformat.v4.new_markdown_cell(md_content))
                in_multiline_comment = False
                multiline_content = []
                current_cell_type = 'code'
            continue
        
        # Début d'un commentaire multiligne
        if is_multiline_comment_start(line):
            in_multiline_comment = True
            comment_part, still_in_comment = extract_multiline_comment(line)
            if comment_part:
                multiline_content.append(comment_part)
            if not still_in_comment:
                if multiline_content:
                    md_content = '\n'.join(multiline_content)
                    cells.append(nbformat.v4.new_markdown_cell(md_content))
                in_multiline_comment = False
                multiline_content = []
            continue
        
        # Commentaires simples
        if is_comment_line(line):
            if current_cell_type == 'code' and current_cell_lines:
                code_content = '\n'.join(current_cell_lines)
                cells.append(nbformat.v4.new_code_cell(code_content))
                current_cell_lines = []
            
            current_cell_type = 'markdown'
            md_line = re.sub(r'^#\s*', '', line).rstrip()
            if md_line:
                current_cell_lines.append(md_line)
        else:
            if current_cell_type == 'markdown' and current_cell_lines:
                md_content = '\n'.join(current_cell_lines)
                cells.append(nbformat.v4.new_markdown_cell(md_content))
                current_cell_lines = []
            
            current_cell_type = 'code'
            current_cell_lines.append(line)
    
    # Dernière cellule
    if current_cell_lines:
        if current_cell_type == 'code':
            code_content = '\n'.join(current_cell_lines)
            cells.append(nbformat.v4.new_code_cell(code_content))
        else:
            md_content = '\n'.join(current_cell_lines)
            cells.append(nbformat.v4.new_markdown_cell(md_content))
    
    # Nettoyage des cellules vides
    cells = [cell for cell in cells if cell['source'].strip()]
    return cells

def create_jupyter_notebook(cells: List[Dict[str, Any]]) -> nbformat.NotebookNode:
    """Crée un vrai notebook Jupyter avec toutes les métadonnées."""
    notebook = nbformat.v4.new_notebook()
    notebook['cells'] = cells
    
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
            'codemirror_mode': {'name': 'ipython', 'version': 3},
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
        content = py_path.read_text(encoding='utf-8')
        cells = parse_python_to_cells(content)
        
        if not cells:
            print(f"⚠️  Fichier vide ou sans contenu convertible: {py_path.name}")
            return False
        
        notebook = create_jupyter_notebook(cells)
        
        # ✅ Validation du notebook généré
        validate(notebook)
        
        notebook_name = py_path.stem + ".ipynb"
        notebook_path = output_dir / notebook_name
        
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(notebook, f, version=4)
        
        code_cells = sum(1 for cell in cells if cell['cell_type'] == 'code')
        md_cells = sum(1 for cell in cells if cell['cell_type'] == 'markdown')
        
        print(f"✅ {py_path.name} → {notebook_name} ({code_cells}⧵{md_cells})")
        return True
        
    except Exception as e:
        print(f"❌ Erreur avec {py_path.name}: {str(e)}")
        return False

def main():
    """Conversion principale."""
    base_dir = Path("/home/datascientest/cde/")
    notebooks_dir = base_dir / "notebooks"
    source_dirs = [base_dir / "scripts", base_dir / "api"]  # ✅ /scripts + /api
    
    print("🎯 CONVERSION VERS DE VRAIS NOTEBOOKS JUPYTER")
    print("=" * 60)
    print(f"📁 Sources: {[str(d) for d in source_dirs]}")
    print(f"📁 Destination: {notebooks_dir}")
    print("=" * 60)
    
    # Vérifier les dossiers source
    all_py_files = []
    for src_dir in source_dirs:
        if not src_dir.exists():
            print(f"⚠️  Dossier inexistant: {src_dir}")
            continue
        py_files = list(src_dir.rglob("*.py"))
        py_files = [f for f in py_files if f.name != "__init__.py"]
        all_py_files.extend(py_files)
    
    if not all_py_files:
        print("❌ Aucun fichier Python trouvé dans les répertoires spécifiés.")
        return 1
    
    notebooks_dir.mkdir(exist_ok=True)
    
    print(f"📊 {len(all_py_files)} fichiers Python trouvés")
    print("-" * 60)
    
    success_count = 0
    
    # ✅ Progress bar sur tous les fichiers
    for py_file in tqdm(all_py_files, desc="Conversion", unit="fichier"):
        if convert_python_file_to_notebook(py_file, notebooks_dir):
            success_count += 1
    
    print("=" * 60)
    print("🎉 CONVERSION TERMINÉE!")
    print(f"✅ {success_count} fichiers convertis avec succès")
    print(f"❌ {len(all_py_files) - success_count} échecs")
    print(f"📁 Notebooks disponibles dans: {notebooks_dir}")
    
    nb_files = list(notebooks_dir.glob("*.ipynb"))
    if nb_files:
        print(f"\n📋 {len(nb_files)} notebooks créés:")
        for nb_file in nb_files:
            print(f"   • {nb_file.name}")
    
    return 0

if __name__ == "__main__":
    exit(main())
