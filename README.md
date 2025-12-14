# PE Experiment discs

## Virtual Disk Performance Comparison Tools

This project provides tools for comparing the performance of different virtual disk types (VDI and VMDK) in Oracle VM by measuring file copy operations.

### Overview

The project consists of two main Python programs:

1. **file_copy_benchmark.py** - Creates files with random sizes and measures copy times
2. **analyze_results.py** - Analyzes the benchmark results and creates statistical plots

### Prerequisites

- Python 3.7 or higher
- Required Python packages (install via `pip install -r requirements.txt`):
  - pandas
  - numpy
  - matplotlib
  - scipy

### Installation

```bash
# Clone the repository
git clone https://github.com/Otger99/NetoCornetto.git
cd NetoCornetto

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Running the File Copy Benchmark

The benchmark program creates N files with random sizes between 32MB and 256MB, moves them from a source to destination folder, and records timing data.

#### Basic Usage

```bash
# Test VDI disk
python file_copy_benchmark.py -n 50 -s ./source_vdi -d ./dest_vdi -t VDI -o results_vdi.csv

# Test VMDK disk
python file_copy_benchmark.py -n 50 -s ./source_vmdk -d ./dest_vmdk -t VMDK -o results_vmdk.csv
```

#### Command-line Options

- `-n, --num-files`: Number of files to create and move (default: 10)
- `-s, --source-dir`: Source directory for file creation (default: ./source)
- `-d, --dest-dir`: Destination directory for file movement (default: ./destination)
- `-t, --disk-type`: Type of virtual disk (VDI or VMDK) - **required**
- `-o, --output`: Output CSV file path (default: resultado_{disk_type}.csv)
- `--seed`: Random seed for reproducibility (optional)

#### Example Output

The program creates a CSV file with the following columns:
- `filename`: Name of the file
- `size_mb`: Size of the file in megabytes
- `disk_type`: Type of disk (VDI or VMDK)
- `time_seconds`: Time taken to copy the file in seconds

### 2. Analyzing Results

After collecting data from both VDI and VMDK tests, use the analysis program to create statistical plots and verify linear regression assumptions.

#### Basic Usage

```bash
# Analyze both VDI and VMDK results
python analyze_results.py -i results_vdi.csv results_vmdk.csv -o plots

# Analyze a single result file
python analyze_results.py -i results_vdi.csv -o plots_vdi
```

#### Command-line Options

- `-i, --input`: Input CSV file(s) with benchmark results - **required**
- `-o, --output-dir`: Output directory for plots (default: ./plots)

#### Generated Plots

The analysis program creates four plots to verify statistical assumptions:

1. **linearity_plot.png** - Linearity Check
   - Shows file size vs. copy time relationship
   - Includes regression line to verify linear relationship

2. **homoscedasticity_plot.png** - Homoscedasticity Check
   - Plots residuals vs. fitted values
   - Verifies that variance is constant across the range

3. **independence_histogram.png** - Independence Check
   - Histogram of copy times
   - Verifies randomness and independence of observations

4. **normality_qqplot.png** - Normality Check
   - Q-Q plot of residuals
   - Verifies that residuals follow a normal distribution

### Statistical Analysis

The program performs linear regression analysis and checks the following assumptions:

- **Linearity**: The relationship between file size and copy time should be linear
- **Homoscedasticity**: The variance of residuals should be constant
- **Independence**: Observations should be independent and random
- **Normality**: Residuals should follow a normal distribution

These assumptions are necessary for valid interpretation of linear regression models (lm() in R).

## Example Workflow

```bash
# Step 1: Run benchmark on VDI disk (on VM with VDI disk)
python file_copy_benchmark.py -n 100 -t VDI -o results_vdi.csv

# Step 2: Run benchmark on VMDK disk (on VM with VMDK disk)
python file_copy_benchmark.py -n 100 -t VMDK -o results_vmdk.csv

# Step 3: Copy both CSV files to a single machine

# Step 4: Analyze the combined results
python analyze_results.py -i results_vdi.csv results_vmdk.csv -o plots

# Step 5: Review the generated plots and statistics
```

### Quick Demo

For a quick demonstration with smaller test files, you can run the included example script:

```bash
# This creates test data with smaller files for quick testing
./example_workflow.sh
```

**Note:** The example script uses small file sizes for demonstration purposes. For actual benchmarking, use the full size range (32-256 MB) as specified in the problem statement.

## Understanding the Results

### Linear Regression Model

The analysis fits a linear model: `Time = intercept + slope × Size`

This model can be used to:
- Predict copy times for different file sizes
- Compare performance between VDI and VMDK disks
- Identify which disk type performs better

### Statistical Tests

The program also performs:
- **Shapiro-Wilk test** for normality of residuals
- Calculates **R²** to measure goodness of fit

### Interpreting Plots

- **Linearity**: Points should roughly follow the regression line
- **Homoscedasticity**: Residuals should be randomly scattered around zero without patterns
- **Independence**: Histogram should show reasonable distribution
- **Normality**: Q-Q plot points should fall close to the diagonal line

## Notes

- The program creates files with random content using `os.urandom()` for realistic disk I/O
- File sizes are uniformly distributed between 32MB and 256MB using whole-megabyte increments to avoid rounding errors during file generation
- Timing measurements use Python's `time.time()` for precision
- The programs are modular and can be easily adapted for other disk types or experiments

## License

This project is provided as-is for educational and research purposes.
