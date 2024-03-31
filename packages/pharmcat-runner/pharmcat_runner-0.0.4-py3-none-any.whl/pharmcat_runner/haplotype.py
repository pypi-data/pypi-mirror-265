import glob
import gzip
import os
import shutil
import warnings
from datetime import datetime
from tempfile import TemporaryDirectory

import pandas as pd

from .common import *
from .qc_metrics import QCMetrics
from .utils import (
    index_file,
    maybe_create_dir,
    run_command,
    get_files,
    blockgz_compress,
)


def _copy_outputs(dir_, glob_pattern, tempdir):
    os.mkdir(dir_)
    for file in glob.glob(os.path.join(tempdir, glob_pattern)):
        shutil.copy2(file, dir_)


def move_outputs(vcf_input=None, tempdir=None, output_dir=None):
    # VCF used in PharmCAT
    shutil.copy2(vcf_input, output_dir)

    data_to_copy = {
        "pharmcat_output": "*.json",  # PharmCAT jsons
        "pharmcat_warnings": "*warnings*",  # PharmCAT warnings
        "qc_metrics": "*.tsv",  # QC metrics
    }
    for dir_, glob_pattern in data_to_copy.items():
        dir_ = os.path.join(output_dir, dir_)
        _copy_outputs(dir_=dir_, glob_pattern=glob_pattern, tempdir=tempdir)


def run_pharmcat(vcf_input, tempdir):
    preprocessor_path = os.path.join(BIN_DIR, "preprocessor")
    # python_path = os.path.join(BIN_DIR, "python", "bin", "python3.9")
    python_path = "python3"
    pharmcat_pipeline_path = os.path.join(preprocessor_path, "pharmcat_pipeline")
    num_threads = os.cpu_count() - 1 if os.cpu_count() != 1 else 1
    run_command(
        f"cd {preprocessor_path} && {python_path} -m pipenv run python {pharmcat_pipeline_path} {vcf_input} --missing-to-ref -o {tempdir} -matcher --research-mode cyp2d6 -cp {num_threads}",
        shell=True,
    )


@index_file
def annotate_id(file):
    # Need to annotate the ID field with something more informative because
    # of QC steps with PLINK. If not, can get rows that have the same affy snp
    # id and no clear way to differentiate them
    output_file = file.replace(".vcf", "_annotateid.vcf")
    run_command(
        [
            "bcftools",
            "annotate",
            "-I",
            "%ID\_%CHROM\_%POS\_%REF\_%ALT",
            "-Oz",
            "-o",
            output_file,
            file,
        ]
    )
    return output_file


@index_file
def sort_vcf(file, output):
    # Only one where .gz needs to be adjusted because it's the first step
    if ".gz" in output:
        sorted_file = output.replace(".vcf", "_sorted.vcf")
    else:
        sorted_file = output.replace(".vcf", "_sorted.vcf.gz")
    run_command(["bcftools", "sort", "-Oz", "-o", sorted_file, file])
    return sorted_file


@index_file
def fix_ugt1a1_indels(file):
    # UGT1A1 ref and alt alleles are not correct for the indels
    # Confirmed with email from Carsten 3/28/2024
    # Will be fixed in r10 release of Pscan
    output_file = file.replace(".vcf", "_ugt1a1fixed.vcf")
    output_file_nogz = output_file.replace(".gz", "")

    # Fix the indel
    with gzip.open(file, "rt") as f_in, open(output_file_nogz, "w") as f_out_nogz:
        for line in f_in:
            if "233760235" in line:
                new = f"TAT\tT,TATAT"
                old = f"TATAT\tT,TAT"
                line = line.replace(old, new)
            f_out_nogz.write(line)

    # Compress the output
    # Can't use python gzip to do block gzip compression
    output_file = blockgz_compress(input_file=output_file_nogz, output_file=output_file)

    return output_file


@index_file
def fix_chromosome_labels(file):
    fixed_file = file.replace(".vcf", "_chrfixed.vcf")
    run_command(
        [
            "bcftools",
            "annotate",
            "--rename-chr",
            CHR_CONV_PATH,
            "-Oz",
            "-o",
            fixed_file,
            file,
        ]
    )
    return fixed_file


@index_file
def split_multiallelic(file):
    # Needed because this can throw pharmcat off
    split_file = file.replace(".vcf", "_split.vcf")
    run_command(
        [
            "bcftools",
            "norm",
            "-m-any",
            "-c",
            "e",
            "-f",
            REFERENCE_PATH,
            "-Oz",
            "-o",
            split_file,
            file,
        ]
    )
    return split_file


@index_file
def filter_vcf_for_variants(file, tempdir=None, pharmcat_positions_file=None):
    # Selects only pharmcat variants
    # Including non pharmcat variants can cause issues with calling
    cleaned_file = os.path.join(tempdir, "pharmcat_variants_only.vcf.gz")

    # Can't use "--regions-overlap variant" because indels don't get captured correctly
    run_command(
        [
            "bcftools",
            "view",
            "--regions-file",
            pharmcat_positions_file,
            "-e",
            'POS==42126599 || ID=="AX-165885131"',
            "-Oz",
            "-o",
            cleaned_file,
            file,
        ]
    )
    return cleaned_file


@index_file
def merge_vcfs(files, tempdir):
    files_to_merge = os.path.join(tempdir, "files_to_merge.txt")
    with open(files_to_merge, "w") as f:
        for file in files:
            f.write(file + "\n")

    merged_file = os.path.join(tempdir, "merged.vcf.gz")
    run_command(
        [
            "bcftools",
            "merge",
            "--file-list",
            files_to_merge,
            "-i",
            "-",
            "-m",
            "none",
            "-Oz",
            "-o",
            merged_file,
        ]
    )
    return merged_file


@index_file
def filter_certain_chromosomes(file, reg=True):
    # Need to split out chromsomes that wouldn't be in reference sequence
    # Includes MT and any alternate contigs
    chrs = pd.read_table(CHR_CONV_PATH, header=None, sep=" ")[1]
    if reg:
        output_file = file.replace(".vcf", "_reg_only.vcf")
        chrs = chrs.loc[lambda x: ~x.str.contains("MT|alt", regex=True)]
    else:
        output_file = file.replace(".vcf", "_nonreg_only.vcf")
        chrs = chrs.loc[lambda x: x.str.contains("MT|alt", regex=True)]

    run_command(
        ["bcftools", "view", "-r", ",".join(chrs), "-Oz", "-o", output_file, file]
    )
    return output_file


@index_file
def combine_vcfs(tempdir, *files):
    output_file = os.path.join(tempdir, "aligned_file.vcf.gz")
    run_command(["bcftools", "concat", "-a", "-Oz", "-o", output_file] + list(files))
    return output_file


def get_pharmcat_positions(tempdir=None):
    # Multiallelic variants mess up indels
    # Need to split these up so that they are captured correctly

    pharmcat_variants_orig_file = os.path.join(
        BIN_DIR, "preprocessor", "pharmcat_positions.vcf"
    )
    pharmcat_variants_split_file = os.path.join(tempdir, "pharmcat_positions_split.vcf")
    pharmcat_positions_file = os.path.join(tempdir, "pharmcat_positions.tsv.gz")

    # Splits multiallelic and left normalizes pharmcat variants
    run_command(
        f"bcftools norm -m -both -c e -f {REFERENCE_PATH} {pharmcat_variants_orig_file} > {pharmcat_variants_split_file} && bcftools query -f'%CHROM\t%POS\t%REF,%ALT\n' {pharmcat_variants_split_file} | bgzip -c > {pharmcat_positions_file} && tabix -s1 -b2 -e2 {pharmcat_positions_file}",
        shell=True,
    )

    return pharmcat_positions_file


def write_manifest(
    output_dir=None,
    num_files=None,
    vcf_input=None,
    variant_call_rate=None,
    sample_call_rate=None,
    hwe=None,
):
    for file in os.listdir(BIN_DIR):
        if "jdk" in file:
            jdk_version = file.replace("jdk-", "")
    user = os.path.basename(os.path.expanduser("~"))
    today = datetime.today().strftime("%B %d, %Y")
    bcftools_version = (
        run_command(["bcftools", "--version"], capture_output=True)
        .split("\n")[0]
        .split(" ")[-1]
        .strip()
    )
    num_samples = run_command(
        f"bcftools query -l {vcf_input} | wc -l", capture_output=True, shell=True
    ).strip()
    plink_version = run_command(["plink", "--version"], capture_output=True).split()[1]
    with open(os.path.join(BIN_DIR, "preprocessor", "preprocessor", "common.py")) as f:
        for line in f:
            if "PHARMCAT_VERSION" in line:
                pharmcat_version = line.split("= ")[-1].strip().strip("'")
    with open(os.path.join(output_dir, "manifest.txt"), "w") as f:
        f.write(MANIFEST_HEADER + "\n")
        f.write(f"User: {user}\n")
        f.write(f"Date: {today}\n")
        f.write(f"PharmCAT version: {pharmcat_version}\n")
        f.write(f"Python version: {sys.version.split()[0]}\n")
        f.write(f"JDK version: {jdk_version}\n")
        f.write(f"Bcftools version: {bcftools_version}\n")
        f.write(f"PLINK version: {plink_version}\n")
        f.write(f"Number of input VCF files: {num_files}\n")
        f.write(f"Number of samples: {num_samples}\n")
        f.write(f"Variant call rate cutoff: {variant_call_rate}\n")
        f.write(f"Sample call rate cutoff: {sample_call_rate}\n")
        f.write(f"Hardy Weinburg Equilibrium cutoff: {hwe}\n")
        f.write(f"VCF input to PharmCAT: {os.path.basename(vcf_input)}\n")


def _get_files(dir_):
    files = get_files(dir_)
    clean_files = []
    for file in files:
        if file.endswith(".vcf") or file.endswith(".vcf.gz"):
            new_path = os.path.join(dir_, file)
            clean_files.append(new_path)
    return clean_files


def move_all_files(files):
    debug_dir = os.path.join(os.getcwd(), "debug")
    maybe_create_dir(debug_dir, strict=True)
    for file in files:
        shutil.copy2(file, debug_dir)


def check_warnings(dir_):
    num_warnings = len(os.listdir(dir_))
    if num_warnings != 0:
        warnings.warn(
            f"PharmCAT returned {num_warnings} warnings when running. Review warnings at {dir_}"
        )


def run_qc(
    file=None, tempdir=None, hwe=None, variant_call_rate=None, sample_call_rate=None
):
    qc_metrics = QCMetrics(
        file=file,
        tempdir=tempdir,
        hwe=hwe,
        variant_call_rate=variant_call_rate,
        sample_call_rate=sample_call_rate,
    )
    if variant_call_rate or hwe:
        qc_metrics.variant_qc()
    if sample_call_rate:
        qc_metrics.sample_qc()
    return qc_metrics


def call_haplotypes(
    dir_=None,
    hwe=None,
    variant_call_rate=None,
    sample_call_rate=None,
    output_dir=None,
    debug=False,
):
    with TemporaryDirectory() as tempdir:
        try:
            pharmcat_positions_file = get_pharmcat_positions(tempdir=tempdir)

            files = _get_files(dir_)
            print("Prepping files for PharmCAT...")
            sorted_files = []
            for file in files:
                sorted_file = sort_vcf(
                    file, os.path.join(tempdir, os.path.basename(file))
                )
                sorted_files.append(sorted_file)
            merged_file = merge_vcfs(files=sorted_files, tempdir=tempdir)
            merged_file_ugt1a1_fixed = fix_ugt1a1_indels(file=merged_file)
            fixed_file = fix_chromosome_labels(merged_file_ugt1a1_fixed)

            reg_chr_only = filter_certain_chromosomes(file=fixed_file, reg=True)
            nonreg_chr_only = filter_certain_chromosomes(file=fixed_file, reg=False)
            split_file = split_multiallelic(file=reg_chr_only)
            alignment_fixed_file = combine_vcfs(tempdir, split_file, nonreg_chr_only)
            alignment_sorted = sort_vcf(
                alignment_fixed_file, os.path.join(tempdir, "alignment.vcf.gz")
            )
            pharmcat_variants_only_file = filter_vcf_for_variants(
                file=alignment_sorted,
                tempdir=tempdir,
                pharmcat_positions_file=pharmcat_positions_file,
            )
            annotate_id_file = annotate_id(file=pharmcat_variants_only_file)
            if any([hwe, variant_call_rate, sample_call_rate]):
                print("Running pre-PharmCAT QC...")
                qc_metrics = run_qc(
                    file=annotate_id_file,
                    tempdir=tempdir,
                    hwe=hwe,
                    variant_call_rate=variant_call_rate,
                    sample_call_rate=sample_call_rate,
                )
            try:
                vcf_input = qc_metrics.output_file
            except NameError:
                vcf_input = annotate_id_file
            print("Running PharmCAT...")
            if output_dir is None:
                output_dir = os.path.join(os.getcwd(), "results")
            else:
                if not output_dir.startswith("/"):
                    output_dir = os.path.join(os.getcwd(), output_dir)
            maybe_create_dir(output_dir)
            run_pharmcat(vcf_input=vcf_input, tempdir=tempdir)
            move_outputs(vcf_input=vcf_input, tempdir=tempdir, output_dir=output_dir)
            check_warnings(dir_=os.path.join(output_dir, "pharmcat_warnings"))
            write_manifest(
                output_dir=output_dir,
                num_files=len(files),
                vcf_input=vcf_input,
                variant_call_rate=variant_call_rate,
                sample_call_rate=sample_call_rate,
                hwe=hwe,
            )
            print("Succesfully ran PharmCAT.")
        finally:
            if debug:
                # This section needed here because accessing local scope
                files_needed = [
                    "sorted_files",
                    "merged_file",
                    "fixed_file",
                    "reg_chr_only",
                    "nonreg_chr_only",
                    "split_file",
                    "alignment_fixed_file",
                    "alignment_sorted",
                    "pharmcat_variants_only_file",
                    "annotate_id_file",
                    "pharmcat_positions_file",
                    "merged_file_ugt1a1_fixed",
                ]
                debug_files = []
                for file in files_needed:
                    try:
                        file_needed = locals()[file]
                    except KeyError:
                        pass
                    else:
                        if file_needed is None:
                            continue
                        if isinstance(file_needed, list):
                            debug_files = debug_files + file_needed
                        else:
                            debug_files.append(file_needed)
                try:
                    debug_files = debug_files + qc_metrics.files_created
                except NameError:
                    pass
                debug_files = (
                    debug_files
                    # QC metrics files
                    + glob.glob(os.path.join(tempdir, "*.tsv"))
                    + glob.glob(os.path.join(tempdir, "*miss"))
                    + glob.glob(os.path.join(tempdir, "*.hwe"))
                )

                move_all_files(debug_files)
