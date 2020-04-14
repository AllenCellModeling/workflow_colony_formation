#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from datastep import Step


class JupyterStep(Step):
    """Modify the existing step class to automatically run a notebook"""

    def __init__(self, **kwargs):
        # Run Step init
        super().__init__(**kwargs)

    def run(self, nb_name=None, **kwargs):
        """Run the notebook"""
        # TODO Needs to write config out to pkl for access by notebook
        self.args = kwargs
        config = self.__dict__
        nbpath = Path(__file__).parent.parent / 'steps' / self.step_name
        nbfn = self.name + ".ipynb"
        with open(nbpath / nbfn) as f:
            nb = nbformat.read(f, as_version=4)
        executer = ExecutePreprocessor(timeout=60*60, kernel_name='python3')
        executer.preprocess(nb, {'metadata': {'path': str(nbpath)}})
        self.__dict__.update(config)
        self.manifest.to_csv(
            self.step_local_staging_dir / Path("manifest.csv"), index=False
        )
        return
