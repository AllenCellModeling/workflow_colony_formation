#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import types
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import cloudpickle

from datastep import Step


class JupyterStep(Step):
    """Modify the existing step class to automatically run a notebook"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, nb_name=None, cell_timeout=60 * 60, remove_config=True, **kwargs):
        """Run the notebook

        Paramters
        ---------
        nb_name: str or Path (name of step)
            name of the notebook, assumed to be in same directory as step
        cell_timeout: int (3600)
            number of seconds to allow each cell to execut
        remove_config: bool (True)
            don't keep serialized version of this class that provides info 
            to the notebook
        """
        # Find path and name of notebook
        nb_path = Path(__file__).parent.parent / "steps" / self.step_name
        if nb_name is None:
            nb_name = self.name
        if not nb_name.endswith(".ipynb"):
            nb_name = nb_name + ".ipynb"
        # Write out pickled self for notebook config
        self.args = kwargs
        self.interactive = False  # to inform notebooks
        config_path = nb_path / "config.pkl"
        with open(config_path, "wb") as file:
            cloudpickle.dump(self, file)
        # Run notebook
        with open(nb_path / nb_name) as file:
            nb = nbformat.read(file, as_version=4)
            executer = ExecutePreprocessor(timeout=cell_timeout, kernel_name="python3")
            executer.preprocess(nb, {"metadata": {"path": str(nb_path)}})
        # Reload pickled self from config
        with open(config_path, "rb") as file:
            self = cloudpickle.load(file)
        self.manifest.to_csv(
            self.step_local_staging_dir / Path("manifest.csv"), index=False
        )
        if remove_config:
            config_path.unlink()
        return


def load_step_config(step_name, upstream_names=[], config_path=None):
    """Load the configuration from a config.pkl or create a namespace to store the same"""
    # Try to load step config, use defaults if not found
    if config_path is None:
        config_path = Path("config.pkl")
    if config_path.exists():
        with open(config_path, "rb") as file:
            config = cloudpickle.load(file)
    else:
        config = types.SimpleNamespace()
        config.interactive = True
        config.step_local_staging_dir = Path("local_staging/" + step_name)
        config.direct_upstream_tasks = upstream_names

    return config


def dump_step_config(config, config_path=None):
    """Write out step config to be re-used by JupyterStep"""
    if config_path is None:
        config_path = Path("config.pkl")
    if config_path.exists():
        with open(config_path, "wb") as file:
            cloudpickle.dump(config, file)