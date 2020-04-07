#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pathlib import Path
import shutil
import pandas as pd

from .mov_filenames import fns

from datastep import Step, log_run_params

log = logging.getLogger(__name__)


class Null2Mov(Step):
    @log_run_params
    def run(self, **kwargs):
        """Copy time lapse movies of colony formation to local staging."""
        # Subdirectory for the time lapse movies
        movdir = self.step_local_staging_dir / Path("mov")
        movdir.mkdir(parents=True, exist_ok=True)

        # Copy images
        paths = fns()
        new_paths = []
        for old_path in paths:
            new_path = movdir / old_path.name
            shutil.copyfile(old_path, new_path)
            new_paths.append(new_path)

        # Save manifest as csv
        self.manifest = pd.DataFrame(dict(filepath=new_paths))
        self.manifest.to_csv(
            self.step_local_staging_dir / Path("manifest.csv"), index=False
        )
