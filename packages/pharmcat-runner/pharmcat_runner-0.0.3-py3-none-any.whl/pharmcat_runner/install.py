import os
import shutil
import sys
import traceback
from tempfile import TemporaryDirectory

from .common import *
from .utils import curl, run_command, unpack_tar


def install_java(tempdir):
    curl(tempdir, JAVA_URL)
    unpack_tar(file=os.path.join(tempdir, os.path.basename(JAVA_URL)), dir_=BIN_DIR)


def install_python(tempdir):
    curl(tempdir, PYTHON_URL)
    unpack_tar(file=os.path.join(tempdir, os.path.basename(PYTHON_URL)), dir_=tempdir)
    python_dir = os.path.basename(PYTHON_URL).replace(".tgz", "")
    python_dir_current = os.path.join(tempdir, python_dir)
    run_command(
        f"cd {python_dir_current} && ./configure --prefix={os.path.join(BIN_DIR, 'python')}",
        shell=True,
    )
    run_command(f"cd {python_dir_current} && make", shell=True)
    run_command(f"cd {python_dir_current} && make altinstall", shell=True)


def install_pharmcat():
    dir_ = os.path.join(BIN_DIR, "preprocessor")
    curl(dir_, PHARMCAT_JAR_URL)
    os.rename(
        os.path.join(dir_, os.path.basename(PHARMCAT_JAR_URL)),
        os.path.join(dir_, "pharmcat.jar"),
    )


def download_reference_genome(tempdir):
    curl(dir_=tempdir, url=REFERENCE_GENOME_URL)
    unpack_tar(
        file=os.path.join(tempdir, os.path.basename(REFERENCE_GENOME_URL)),
        dir_=os.path.join(BIN_DIR, "preprocessor"),
    )


def install_preprocessor(tempdir):
    # TODO resolve pipenv/dependency issue on MAC; works on linux
    # version = re.findall(r"\d\.\d+", os.path.basename(PYTHON_URL))[0]
    # python_path = os.path.join(BIN_DIR, "python", "bin", f"python{version}")
    python_path = "python3"
    run_command([python_path, "-m", "pip", "install", "-U", "pipenv", "--user"])
    curl(tempdir, PHARMCAT_PREPROCESSOR_URL)
    unpack_tar(
        file=os.path.join(tempdir, os.path.basename(PHARMCAT_PREPROCESSOR_URL)),
        dir_=BIN_DIR,
    )
    run_command(
        f"cd {os.path.join(BIN_DIR, 'preprocessor')} && {python_path} -m pipenv install -r requirements.txt",
        shell=True,
    )


def set_env_vars():
    bash_profile = os.path.join(os.path.expanduser("~"), ".bash_profile")
    bash_profile_temp = os.path.join(os.path.expanduser("~"), ".bash_profile_temp")
    with open(bash_profile) as f_in:
        with open(bash_profile_temp, "w") as f_out:
            for line in f_in:
                if "JAVA_HOME" not in line:
                    f_out.write(line)
            for file in os.listdir(BIN_DIR):
                if "jdk" in file:
                    f_out.write(f'export JAVA_HOME="{os.path.join(BIN_DIR, file)}"\n')
    shutil.copy2(bash_profile_temp, bash_profile)
    os.remove(bash_profile_temp)


def validate_python_version():
    version_data = sys.version
    if int(version_data.split()[0].split(".")[1]) != 9:
        raise RuntimeError(f"Required Python v3.9, found v{version_data.split()[0]}")


def install(overwrite=False):
    try:
        os.mkdir(BIN_DIR)
    except FileExistsError:
        if overwrite:
            print("Removing old version of PharmCAT")
            shutil.rmtree(BIN_DIR)
            print("Succesfully removed old version of PharmCAT\n")
            os.mkdir(BIN_DIR)
        else:
            raise FileExistsError(
                "Previous installation of PharmCAT found. To install a new version, must supply --overwrite"
            )
    try:
        with TemporaryDirectory() as tempdir:
            print("***Installing PharmCAT and all required dependencies***")
            print("Please wait. This can take several minutes...")

            print("Installing java...")
            install_java(tempdir)
            print("Successfully installed java.")

            # print("Installing Python...")
            # install_python(tempdir)
            # print("Successfully installed Python.")
            validate_python_version()

            print("Installing Preprocessor and PharmCAT pipeline...")
            install_preprocessor(tempdir)
            print("Successfully installed preprocessor and PharmCAT pipeline.")

            print("Downloading reference genome...")
            download_reference_genome(tempdir)
            print("Succesfully downloaded reference genome.")

            print("Installing PharmCAT...")
            install_pharmcat()
            print("Succesfully installed PharmCAT.")

            set_env_vars()
            print("Succesfully set environment variables.")
            print("***Installation completed succesfully.***")
            print(
                "It is recommended to restart the environment/terminal for installation to finalize."
            )
    except Exception as e:
        print(f"Installation failed due to error:\n{traceback.format_exc()}")
        raise e
