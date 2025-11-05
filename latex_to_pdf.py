#!/usr/bin/env python3
"""
Convert LaTeX files to PDF using pdflatex or xelatex
"""

import subprocess
import sys
import os
import argparse
import shutil


def check_latex_engine(engine):
    """Check if the specified LaTeX engine is available"""
    return shutil.which(engine) is not None


def compile_latex(tex_file, engine='pdflatex', output_dir=None):
    """Compile LaTeX file to PDF"""
    if not os.path.exists(tex_file):
        print(f"Error: File '{tex_file}' not found")
        return False
    
    if not check_latex_engine(engine):
        print(f"Error: '{engine}' not found. Please install a LaTeX distribution.")
        return False
    
    # Set output directory
    if output_dir:
        output_args = ['-output-directory', output_dir]
    else:
        output_args = []
    
    # Compile command
    cmd = [engine, '-interaction=nonstopmode'] + output_args + [tex_file]
    
    try:
        # Run LaTeX engine (usually needs to run twice for references)
        for i in range(2):
            print(f"Running {engine} (pass {i+1}/2)...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Error during compilation (pass {i+1}):")
                print(result.stdout)
                print(result.stderr)
                return False
        
        print(f"Successfully compiled {tex_file}")
        
        # Get PDF filename
        pdf_file = os.path.splitext(tex_file)[0] + '.pdf'
        if output_dir:
            pdf_file = os.path.join(output_dir, os.path.basename(pdf_file))
        
        print(f"PDF created: {pdf_file}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Convert LaTeX to PDF')
    parser.add_argument('tex_file', help='Input LaTeX file')
    parser.add_argument('-e', '--engine', default='pdflatex', 
                        choices=['pdflatex', 'xelatex', 'lualatex'],
                        help='LaTeX engine to use (default: pdflatex)')
    parser.add_argument('-o', '--output-dir', help='Output directory for PDF')
    
    args = parser.parse_args()
    
    success = compile_latex(args.tex_file, args.engine, args.output_dir)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()