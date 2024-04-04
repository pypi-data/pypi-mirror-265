import os
import sys

PHARMCAT_JAR_URL = "https://github.com/PharmGKB/PharmCAT/releases/download/v2.11.0/pharmcat-2.11.0-all.jar"
PHARMCAT_PREPROCESSOR_URL = "https://github.com/PharmGKB/PharmCAT/releases/download/v2.11.0/pharmcat-preprocessor-2.11.0.tar.gz"
JAVA_URL = "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.4.1%2B1/OpenJDK17U-jdk_x64_linux_hotspot_17.0.4.1_1.tar.gz"
PYTHON_URL = "https://www.python.org/ftp/python/3.9.15/Python-3.9.15.tgz"
REFERENCE_GENOME_URL = (
    "https://zenodo.org/record/7288118/files/GRCh38_reference_fasta.tar"
)
BIN_DIR = os.path.join(os.path.expanduser("~"), "pharmcat_bin")
HTS_LIB_REQUIRED_VERSION = 1.18

lib_path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "lib")

REFERENCE_PATH = os.path.join(BIN_DIR, "preprocessor", "reference.fna.bgz")
CHR_CONV_PATH = os.path.join(lib_path, "chr_name_conv.txt")
DIP_TO_PHEN_PATH = os.path.join(lib_path, "dip_to_phen.tsv")
DPYD_ALLELE_FXN_PATH = os.path.join(lib_path, "dpyd_allele_function.json")
CYP2D6_ALLELE_FXN_PATH = os.path.join(
    lib_path,
    "cyp2d6_allele_function.json",
)
CYP2D6_CNV_POSITIONS_PATH = os.path.join(lib_path, "cyp2d6_cnv_positions.tsv")

# https://www.asciiart.eu/text-to-ascii-art
# Big with PlusBox
MANIFEST_HEADER = """
+--------------------------------------------------------+
| _____  _                           _____       _______ |
||  __ \| |                         / ____|   /\|__   __||
|| |__) | |__   __ _ _ __ _ __ ___ | |       /  \  | |   |
||  ___/| '_ \ / _` | '__| '_ ` _ \| |      / /\ \ | |   |
|| |    | | | | (_| | |  | | | | | | |____ / ____ \| |   |
||_|___ |_| |_|\__,_|_|  |_| |_| |_|\_____/_/    \_\_|   |
||  __ \                                                 |
|| |__) |   _ _ __  _ __   ___ _ __                      |
||  _  / | | | '_ \| '_ \ / _ \ '__|                     |
|| | \ \ |_| | | | | | | |  __/ |                        |
||_|  \_\__,_|_| |_|_| |_|\___|_|                        |
+--------------------------------------------------------+""".strip()
