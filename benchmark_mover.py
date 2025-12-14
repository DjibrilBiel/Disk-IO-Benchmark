#!/usr/bin/env python3
"""
File Mover Benchmark (Compatible amb Windows)
=============================================
Mou arxius mesurant el temps i neteja la memòria cau (Standby List/Working Set)
utilitzant les API natives de Windows.
"""

import os
import shutil
import time
import csv
import argparse
import platform
import ctypes
from pathlib import Path

def clean_windows_cache():
    """
    Neteja realment la memòria cau de Windows.
    Prioritat:
        1. EmptyStandbyList.exe  (Sysinternals)
        2. API real NtSetSystemInformation
    """

    print("Intentant netejar la memòria cau del sistema...")

    # 1) Intentar EmptyStandbyList.exe (millor opció)
    standby_tool = shutil.which("EmptyStandbyList.exe")
    if standby_tool:
        print("  -> Netejant Standby List amb EmptyStandbyList.exe...")
        os.system(f'"{standby_tool}" standbylist')
        time.sleep(1)
        print("  -> Standby List buidada.")
        return True

    # 2) API real: NtSetSystemInformation
    try:
        print("  -> Usant API NtSetSystemInformation...")

        SystemMemoryListInformation = 0x50
        MemoryPurgeStandbyList = 4

        class SYSTEM_MEMORY_LIST_COMMAND(ctypes.Structure):
            _fields_ = [("Command", ctypes.c_int)]

        cmd = SYSTEM_MEMORY_LIST_COMMAND()
        cmd.Command = MemoryPurgeStandbyList

        ntstatus = ctypes.windll.ntdll.NtSetSystemInformation(
            SystemMemoryListInformation,
            ctypes.byref(cmd),
            ctypes.sizeof(cmd)
        )

        if ntstatus == 0:
            print("  -> Standby List netejada correctament.")
            return True
        else:
            print(f"  -> Error NtSetSystemInformation: {hex(ntstatus)}")
            print("     (Probablement falta executar com a administrador)")
            return False

    except Exception as e:
        print(f"  -> Error en netejar la memòria cau: {e}")
        return False

# ---------------------------------------------

def get_file_size_mb(file_path):
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)

def drop_system_caches():
    """Neteja la memòria cau depenent del SO."""
    system = platform.system()
    print("Intentant netejar la memòria cau del sistema...")
    
    if system == "Windows":
        clean_windows_cache()
        return

    elif system == "Linux":
        try:
            os.system("sync")
            if os.geteuid() == 0:
                os.system("echo 3 > /proc/sys/vm/drop_caches")
            else:
                os.system("sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'")
            print("  -> Memòria cau de Linux netejada.")
        except Exception as e:
            print(f"  -> Error a Linux: {e}")

def move_file_with_timing(src_path, dst_path):
    start_time = time.time()
    shutil.copy(str(src_path), str(dst_path))
    
    # A Windows no hi ha os.sync(), però podem intentar flush manual si obríssim l'arxiu.
    # shutil.move tanca l'arxiu, així que confiem que el SO gestioni el buffer d'escriptura.
    # Una pausa petita ajuda a estabilitzar la mètrica I/O a Windows.
    end_time = time.time()
    return end_time - start_time

def run_mover(source_dir, dest_dir, disk_type, csv_output, clear_cache):
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    
    if csv_output == '':
        csv_output = f"resultat_{disk_type}.csv"
    
    
    if not source_path.exists():
        print(f"Error: El directori origen '{source_dir}' no existeix.")
        return

    dest_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Netejant directori destí: {dest_path}")
    for item in dest_path.iterdir():
        try:
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception as e:
            print(f"  No s'ha pogut esborrar {item}: {e}")
    print("Directori destí net.")
    
    files = [f for f in source_path.iterdir() if f.is_file() and f.name.endswith('.dat')]
    
    if not files:
        print("No s'han trobat arxius .dat.")
        return

    # --- NETEJA INICIAL ---
    if clear_cache:
        print("-" * 60)
        drop_system_caches()
        time.sleep(2) # Pausa perquè Windows s'estabilitzi
    # ------------------------

    # (Nota: El codi original sobreescriu csv_exists sense utilitzar-lo després, mantinc lògica original)
    csv_exists = os.path.exists(csv_output)
    results = []
    
    print("-" * 60)
    print(f"Iniciant benchmark (Disc: {disk_type})")
    
    for i, src_file in enumerate(files):
        file_name = src_file.name
        dst_file = dest_path / file_name
        actual_size_mb = get_file_size_mb(src_file)
        
        print(f"[{i+1}/{len(files)}] Movent: {file_name} ({actual_size_mb:.2f} MB)...", end='', flush=True)
        
        time_taken = move_file_with_timing(src_file, dst_file)
        
        speed_mbs = actual_size_mb / time_taken if time_taken > 0 else 0
        print(f" Llest en {time_taken:.2f}s ({speed_mbs:.2f} MB/s)")
        
        result = {
            'filename': file_name,
            'size_mb': actual_size_mb,
            'disk_type': disk_type,
            'time_seconds': time_taken
        }
        results.append(result)
        
        time.sleep(1)

    print(f"Netejant CSV existent: {csv_output}")
    with open(csv_output, 'w', newline='') as csvfile:
        fieldnames = ['filename', 'size_mb', 'disk_type', 'time_seconds']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    with open(csv_output, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['filename', 'size_mb', 'disk_type', 'time_seconds'])
        writer.writerows(results)

    
    print("-" * 60)
    print(f"Benchmark completat. Resultats a {csv_output}")

def main():
    parser = argparse.ArgumentParser(description='Benchmark Mover Windows')
    parser.add_argument('-s', '--source-dir', type=str, required=True, help='Directori origen')
    parser.add_argument('-d', '--dest-dir', type=str, required=True, help='Directori destí')
    parser.add_argument('-t', '--disk-type', type=str, required=True, help='Tipus de disc')
    parser.add_argument('-o', '--output', type=str, default='', help='CSV sortida')
    parser.add_argument('--no-cache', action='store_true', help='Neteja la memòria cau (Executar com ADMIN)')
    
    args = parser.parse_args()
    run_mover(args.source_dir, args.dest_dir, args.disk_type, args.output, args.no_cache)

if __name__ == '__main__':
    main()