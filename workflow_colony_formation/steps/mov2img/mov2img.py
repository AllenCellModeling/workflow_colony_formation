#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pathlib import Path

from ...utils import JupyterStep

from datastep import Step, log_run_params

###############################################################################

log = logging.getLogger(__name__)

###############################################################################


class Mov2Img(JupyterStep):
    def __init__(self, direct_upstream_tasks = ["null2mov"], **kwargs):
        super().__init__(direct_upstream_tasks=direct_upstream_tasks, **kwargs)

    @log_run_params
    def run(self, **kwargs):
        super().run(**kwargs)
