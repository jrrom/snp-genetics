import argparse
import csv
import os
import numpy as np
from pathlib import Path
from src.snp_functions import snp_single, snp_double
from src.snp_spark import snp_spark

def structure(entry_path):
    with open(entry_path, "r", encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter="\t");
        # We skip the header row
        next(reader)
        # We skip the 0th header row, and the first 10 columns
        # Personal note: np.array(...) drills down
        complete = np.array([row[11:] for row in reader])

        return complete.T

def output(entry_output_path, final_list: np.ndarray):
    with open(entry_output_path, mode="w", encoding="UTF-8") as file:
        print(f"Writing to file {entry_output_path}...\n")
        np.savetxt(file, final_list, encoding="UTF-8", fmt="%d", delimiter="\t")

if __name__ == "__main__":
    print()
    
    # ====== Parse Arguments ======
    parser = argparse.ArgumentParser(
        prog="Genetic Analysis",
        description="Find the SNP of the given data"
    )
    parser.add_argument("directory", type=Path)
    parser.add_argument("-t", "--type", choices=["single", "double"], required=True)
    parser.add_argument("-s", "--spark", action=argparse.BooleanOptionalAction, default=False)
    
    args = parser.parse_args()
    directory: Path = args.directory
    output_path: Path = directory / "output"
    spark_path: Path  = directory / "spark"

    # ====== Select function type ======
    snp_functions = {
        "single": snp_single,
        "double": snp_double
    }
    snp_function = snp_functions[args.type]

    # ====== Create output directory if it does not exist ======
    if not output_path.is_dir():
        os.mkdir(output_path)

    # ====== Create final list for each file given ======
    if args.spark:
        valid_files = [
            str(entry) for entry in directory.iterdir() 
            if entry.is_file() and entry.stat().st_size > 0
        ]
        spark_input_string = ",".join(valid_files)
        
        snp_spark(spark_input_string, str(spark_path), snp_function)
        exit(0)

    for entry in os.listdir(directory):
        if entry == "output" or "spark" in entry: continue
        entry_path = directory / entry
        
        if os.path.getsize(entry_path) == 0:
            print(f"\033[91mWarning:\033[0m File {entry} is empty, skipping...\n")
            continue

        linelist = structure(entry_path)
            
        final_list  = snp_function(linelist)
        output(output_path / entry, final_list)
