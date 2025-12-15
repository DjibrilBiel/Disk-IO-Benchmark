# Benchmark de Disc amb Arxius de Mida Aleatòria

Aquest projecte permet generar arxius aleatoris i executar un benchmark
de còpia entre directoris per mesurar el rendiment del disc.

## Requisits

- Python 3.7 o superior
- Paquets requerits (instal·la via `pip install -r requirements.txt`):
  - pandas
  - numpy
  - matplotlib
  - scipy

### Instal·lació de dependències

```bash
# Clona el repositori
git clone https://github.com/DjibrilBiel/Disk-IO-Benchmark.git
cd Disk-IO-Benchmark

# Instal·la dependències
pip install -r requirements.txt
```

## Eines incloses

### 1️⃣ Generador d’arxius (`file_generator.py`)

Crea arxius `.dat` amb mides aleatòries entre 32 MB i 256 MB.

#### Ús

```bash
python generate_files.py -n 50 -d ./carpeta_origen
```

**Paràmetres:**
- `-n, --num-files` → Nombre d’arxius a crear
- `-d, --dir` → Directori de sortida
- `--seed` → Llavor aleatòria (opcional)

---

### 2️⃣ Benchmark de còpia (`benchmark_mover.py`)

Copia els arxius generats i mesura el temps emprat, desant els resultats
en un fitxer CSV.

#### Ús

```bash
python benchmark_mover.py -s ./carpeta_origen -d ./carpeta_desti -t VDI --no-cache
```

**Paràmetres:**
- `-s, --source-dir` → Directori origen
- `-d, --dest-dir` → Directori destí
- `-t, --disk-type` → Tipus de disc (ex: VDI, VMDK)
- `-o, --output` → Fitxer CSV de sortida
- `--no-cache` → Neteja la memòria cau (requereix administrador)

## Resultats

Els resultats es guarden en un fitxer CSV amb la informació següent:
- Nom de l’arxiu
- Mida en MB
- Tipus de disc
- Temps de còpia en segons
