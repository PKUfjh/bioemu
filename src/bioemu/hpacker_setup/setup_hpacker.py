import logging
import os
import subprocess

HPACKER_INSTALL_SCRIPT = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "setup_sidechain_relax.sh"
)
HPACKER_DEFAULT_ENVNAME = "hpacker"
HPACKER_DEFAULT_REPO_DIR = os.path.join(os.path.expanduser("~"), ".hpacker")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def ensure_hpacker_install(
    envname: str = HPACKER_DEFAULT_ENVNAME, repo_dir: str = HPACKER_DEFAULT_REPO_DIR
) -> None:
    """
    Ensures hpacker and its dependencies are installed under conda environment
    named `envname`
    """
    _conda_not_installed_errmsg = "conda required to install hpacker environment"
    conda_root = os.getenv("CONDA_ROOT", None)
    if conda_root is None:
        # Attempt $CONDA_PREFIX_1 or $CONDA_PREFIX, depending
        # on whether the `base` environment is activated.
        default_env_name = os.getenv("CONDA_DEFAULT_ENV", None)
        assert default_env_name is not None, _conda_not_installed_errmsg
        conda_prefix_env_name = "CONDA_PREFIX" if default_env_name == "base" else "CONDA_PREFIX_1"
        conda_root = os.getenv(conda_prefix_env_name, None)
    assert conda_root is not None, _conda_not_installed_errmsg
    conda_envs = os.listdir(os.path.join(conda_root, "envs"))

    if envname not in conda_envs:
        logger.info("Setting up hpacker dependencies...")
        _install = subprocess.run(
            ["bash", HPACKER_INSTALL_SCRIPT, envname, repo_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        assert (
            _install.returncode == 0
        ), f"Something went wrong during hpacker setup: {_install.stdout.decode()}"
