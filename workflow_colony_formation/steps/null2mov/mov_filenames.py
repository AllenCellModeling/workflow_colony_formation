#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

FNS = [
    "/allen/aics/assay-dev/MicroscopyData/Irina/2017/20170711/20170711_I01_001.czi",
]


def fns():
    """Return a list of mov filenames to copy to staging"""
    return [Path(fn) for fn in FNS]
