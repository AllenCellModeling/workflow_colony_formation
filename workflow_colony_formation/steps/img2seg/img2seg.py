#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from ...utils import JupyterStep

from datastep import log_run_params

###############################################################################

log = logging.getLogger(__name__)

###############################################################################


class Img2Seg(JupyterStep):
    def __init__(self, direct_upstream_tasks=["mov2img"], **kwargs):
        super().__init__(direct_upstream_tasks=direct_upstream_tasks, **kwargs)

    @log_run_params
    def run(self, **kwargs):
        super().run(cell_timeout=60 * 60 * 24, **kwargs)
