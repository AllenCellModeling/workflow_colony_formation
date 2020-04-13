#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
from datastep import Step


class JupyterStep(Step):
    """Modify the existing step class to automatically run a notebook"""

    def __init__(self, **kwargs):
        # Run Step init
        super().__init__(kwargs)

    def run(self, nb_name=None, **kwargs):
        """Run the notebook"""
        self.args = kwargs
        config_pkl = pickle.dumps(self)
        nbfn = Path(__file__).parent / (self.name + ".ipynb")
        nb = nbformat.read(str(nbfn), 4)
        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                exec(cell["source"])
        self = pickle.loads(config)
        self.manifest.to_csv(
            self.step_local_staging_dir / Path("manifest.csv"), index=False
        )
        return