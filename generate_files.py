#!/usr/bin/env python3
"""
Eina Generadora d'Arxius
========================
Aquest programa crea N arxius amb mides aleatòries entre 32MB i 256MB
en un directori especificat.
"""

import os
import random
import argparse
from pathlib import Path
import shutil

# Constants de configuració
MIN_FILE_SIZE_MB = 32 * 1024 * 1024
MAX_FILE_SIZE_MB = 256 * 1024 * 1024

def create_random_file(file_path, size_mb):
    """Crea un arxiu amb contingut aleatori de la mida especificada."""
    size_bytes = int(size_mb)
    chunk_size = 1024 * 1024  # Trossos d'1 MB
    
    with open(file_path, 'wb') as f:
        remaining = size_bytes
        while remaining > 0:
            chunk = min(chunk_size, remaining)
            f.write(os.urandom(chunk))
            remaining -= chunk

def run_generator(num_files, output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Netejant directori destí: {output_path}")
    for item in output_path.iterdir():
        try:
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception as e:
            print(f"No s'ha pogut eliminar {item}: {e}")
    print("Directori destí netejat.\n")
    
    print(f"Generant {num_files} arxius a: {output_dir}")
    print("-" * 60)
    
    for i in range(num_files):
        file_size_mb = random.randint(MIN_FILE_SIZE_MB, MAX_FILE_SIZE_MB)
        # Nom genèric ja que el tipus de disc és indiferent aquí
        file_name = f"testfile_{(i+1):02d}.dat"
        file_path = output_path / file_name
        
        print(f"Creant arxiu {i+1}/{num_files}: {file_name} ({round(file_size_mb / 1024 / 1024, 2)} MB)...")
        create_random_file(file_path, file_size_mb)
        
    print("-" * 60)
    print("Generació completada.")

def main():
    parser = argparse.ArgumentParser(description="Eina per generar arxius de prova")
    
    parser.add_argument('-n', '--num-files', type=int, default=10, help="Nombre d'arxius a crear")
    parser.add_argument('-d', '--dir', type=str, default='./source', help='Directori on guardar els arxius')
    parser.add_argument('--seed', type=int, help='Llavor aleatòria (seed)')
    
    args = parser.parse_args()
    
    if args.seed is not None:
        random.seed(args.seed)
    
    run_generator(args.num_files, args.dir)

if __name__ == '__main__':
    main()