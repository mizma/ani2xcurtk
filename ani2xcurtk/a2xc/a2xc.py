#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BSD 2-Clause License
#
# Copyright (c) 2025 mizma <omoikane@path-works.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from enum import IntEnum


import yaml
import os
import sys
from pathlib import Path
from pprint import pformat
from . import extract_png
from . import pack_xcur
import click


class Level(IntEnum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


def pout(msg=None, Verbose=0, level=Level.INFO, newline=True):
    """stdout support method
    All Error, Critical and Info are printed out.
    while Warning and Debug are printed only with verbosity setting.
    INFO -- Intended for standard output. output to STDOUT
    DEBUG -- Intended for debug output. Shown only in verbosity>=2 output to STDOUT
    WARNING -- Intended to show detailed warning. Shown only in verbosity>=1.  output to STDERR
    ERROR -- Intended to show error.  output to STDERR
    CRITICAL -- Intended to show critical error. output to STDERR

    Keyword Arguments:
        msg (string) -- message to print (default: {None})
        Verbose (Int) -- Set True to print DEBUG message (default: {0})
        level (Level) -- Set message level for coloring (default: {Level.INFO})
        newline (bool) -- set to False if trailing new line is not needed (default: {True})
    """
    error = False
    if level in {Level.NOTSET, Level.DEBUG}:
        # blah
        if Verbose < 2:
            return
        fg = "magenta"
    elif level == Level.INFO:
        fg = "green"
    elif level == Level.WARNING:
        if Verbose < 1:
            return
        fg = "yellow"
        error = True
    elif level in {Level.ERROR, Level.CRITICAL}:
        fg = "red"
        error = True
    else:
        fg = "white"
    click.echo(click.style(str(msg), fg=fg), nl=newline, err=error)


def createConf(conf, verbose):
    """Generate default configuratino at path specified in conf

    Args:
        conf (string): Path to generate default configuration file to.
        verbose (int): Verbosity level
    """
    try:
        with click.open_file(conf, "w", "utf-8") as fd:
            fd.writelines(
                [
                    "sizes:\n",
                    "  - 40\n",
                    "  - 48\n",
                    "  - 56\n",
                    "  - 64\n",
                    "generate:\n",
                    '  - "01-Normal":\n',
                    '    - "01-Normal-mirrored": "mirror"\n',
                    '  - "11-Vertical_Resize":\n',
                    '    - "11-Vertical_Resize-top": "copy"\n',
                    '    - "11-Vertical_Resize-bottom": "copy"\n',
                    '  - "12-Horizontal_Resize":\n',
                    '    - "12-Horizontal_Resize-left": "copy"\n',
                    '    - "12-Horizontal_Resize-right": "copy"\n',
                    '  - "13-Diagonal_Resize_1":\n',
                    '    - "13-Diagonal_Resize_1-top": "copy"\n',
                    '    - "13-Diagonal_Resize_1-bottom": "copy"\n',
                    '  - "14-Diagonal_Resize_2":\n',
                    '    - "14-Diagonal_Resize_2-top": "copy"\n',
                    '    - "14-Diagonal_Resize_2-bottom": "copy"\n',
                    "mappings:\n",
                    '  - "01-Normal":\n',
                    '    - "arrow"\n',
                    '    - "default"\n',
                    '    - "left_ptr"\n',
                    '    - "top_left_arrow"\n',
                    '  - "02-Link":\n',
                    '    - "alias"\n',
                    '    - "dnd-link"\n',
                    '    - "hand"\n',
                    '    - "hand1"\n',
                    '    - "hand2"\n',
                    '    - "link"\n',
                    '    - "openhand"\n',
                    '    - "pointer"\n',
                    '    - "pointing_hand"\n',
                    '    - "3085a0e285430894940527032f8b26df"\n',
                    '    - "640fb0e74195791501fd1ed57b41487f"\n',
                    '    - "9d800788f1b08800ae810202380a0822"\n',
                    '    - "a2a266d0498c3104214a47bd64ab0fc8"\n',
                    '    - "b66166c04f8c3109214a4fbd64a50fc8"\n',
                    '    - "e29285e634086352946a0e7090d73106"\n',
                    '  - "03-Loading":\n',
                    '    - "half-busy"\n',
                    '    - "left_ptr_watch"\n',
                    '    - "progress"\n',
                    '    - "wait"\n',
                    '    - "watch"\n',
                    '    - "00000000000000020006000e7e9ffc3f"\n',
                    '    - "08e8e1c95fe2fc01f976f1e063a24ccd"\n',
                    '    - "3ecb610c1bf2410f44200f48c40d3599"\n',
                    '  - "04-Help":\n',
                    '    - "dnd-ask"\n',
                    '    - "help"\n',
                    '    - "left_ptr_help"\n',
                    '    - "question_arrow"\n',
                    '    - "whats_this"\n',
                    '    - "5c6cd98b3f3ebcb1f9c7f1c204630408"\n',
                    '    - "d9ce0ab605698f320427677b458ad60b"\n',
                    '  - "05-Text_Select":\n',
                    '    - "ibeam"\n',
                    '    - "text"\n',
                    '    - "xterm"\n',
                    '    - "vertical-text"\n',
                    '  - "06-Handwriting":\n',
                    '    - "draft"\n',
                    '    - "pencil"\n',
                    '  - "07-Precision":\n',
                    '    - "cell"\n',
                    '    - "color-picker"\n',
                    '    - "cross_reverse"\n',
                    '    - "cross"\n',
                    '    - "crosshair"\n',
                    '    - "diamond_cross"\n',
                    '    - "plus"\n',
                    '    - "size_all"\n',
                    '    - "tcross"\n',
                    '  - "08-Unavailable":\n',
                    '    - "circle"\n',
                    '    - "crossed_circle"\n',
                    '    - "dnd-no-drop"\n',
                    '    - "forbidden"\n',
                    '    - "not-allowed"\n',
                    '    - "no-drop"\n',
                    '    - "pirate"\n',
                    '    - "03b6e0fcb3499374a867c041f52298f0"\n',
                    '  - "09-Location_Select": null\n',
                    '  - "10-Person_Select": null\n',
                    '  - "11-Vertical_Resize":\n',
                    '    - "v_double_arrow"\n',
                    '    - "bottom_side"\n',
                    '    - "top_side"\n',
                    '    - "up-arrow"\n',
                    '    - "down-arrow"\n',
                    '    - "n-resize"\n',
                    '    - "ns-resize"\n',
                    '    - "row-resize"\n',
                    '    - "s-resize"\n',
                    '    - "sb_v_double_arrow"\n',
                    '    - "size_ver"\n',
                    '    - "split_v"\n',
                    '    - "sb_down_arrow"\n',
                    '    - "sb_up_arrow"\n',
                    '    - "00008160000006810000408080010102"\n',
                    '    - "2870a09082c103050810ffdffffe0204"\n',
                    '  - "12-Horizontal_Resize":\n',
                    '    - "col-resize"\n',
                    '    - "e-resize"\n',
                    '    - "ew-resize"\n',
                    '    - "h_double_arrow"\n',
                    '    - "left_side"\n',
                    '    - "left-arrow"\n',
                    '    - "right_side"\n',
                    '    - "right-arrow"\n',
                    '    - "sb_right_arrow"\n',
                    '    - "sb_left_arrow"\n',
                    '    - "sb_h_double_arrow"\n',
                    '    - "size_hor"\n',
                    '    - "split_h"\n',
                    '    - "w-resize"\n',
                    '    - "14fef782d02440884392942c11205230"\n',
                    '    - "028006030e0e7ebffc7f7070c0600140"\n',
                    '  - "13-Diagonal_Resize_1":\n',
                    '    - "bd_double_arrow"\n',
                    '    - "bottom_right_corner"\n',
                    '    - "lr_angle"\n',
                    '    - "nw-resize"\n',
                    '    - "nwse-resize"\n',
                    '    - "se-resize"\n',
                    '    - "size_fdiag"\n',
                    '    - "top_left_corner"\n',
                    '    - "ul_angle"\n',
                    '    - "c7088f0f3e6c8088236ef8e1e3e70000"\n',
                    '  - "14-Diagonal_Resize_2":\n',
                    '    - "fd_double_arrow"\n',
                    '    - "bottom_left_corner"\n',
                    '    - "ll_angle"\n',
                    '    - "ne-resize"\n',
                    '    - "nesw-resize"\n',
                    '    - "size_bdiag"\n',
                    '    - "sw-resize"\n',
                    '    - "top_right_corner"\n',
                    '    - "ur_angle"\n',
                    '    - "fcf1c3c7cd4491d801f1e1c78f100000"\n',
                    '  - "15-Move":\n',
                    '    - "all-scroll"\n',
                    '    - "closedhand"\n',
                    '    - "dnd-move"\n',
                    '    - "dnd-none"\n',
                    '    - "fleur"\n',
                    '    - "grab"\n',
                    '    - "grabbing"\n',
                    '    - "move"\n',
                    '    - "4498f0e0c1937ffe01fd06f973665830"\n',
                    '    - "9081237383d90e509aa00f00170e968f"\n',
                    '  - "16-Alternate_Select":\n',
                    '    - "center_ptr"\n',
                    '    - "right_ptr"\n',
                    '    - "draft_large"\n',
                    '    - "draft_small"\n',
                    "  # Following are for manual edit of existing images.\n",
                    "  # These will overwrite existing ones above.\n",
                    '  - "01-Normal-Mirrored": # auto-generated\n',
                    '    - "right_ptr"\n',
                    '    - "draft_large"\n',
                    '    - "draft_small"\n',
                    '  - "11-Vertical_Resize-top": # manually generate\n',
                    '    - "top_side"\n',
                    '    - "up-arrow"\n',
                    '    - "n-resize"\n',
                    '    - "sb_up_arrow"\n',
                    '  - "11-Vertical_Resize-bottom": # manually generate\n',
                    '    - "bottom_side"\n',
                    '    - "down-arrow"\n',
                    '    - "s-resize"\n',
                    '    - "sb_down_arrow"\n',
                    '  - "12-Horizontal_Resize-left": # manually generate\n',
                    '    - "left_side"\n',
                    '    - "left-arrow"\n',
                    '    - "sb_left_arrow"\n',
                    '    - "w-resize"\n',
                    '  - "12-Horizontal_Resize-right": # manually generate\n',
                    '    - "right_side"\n',
                    '    - "right-arrow"\n',
                    '    - "sb_right_arrow"\n',
                    '    - "e-resize"\n',
                    '  - "13-Diagonal_Resize_1-top": # manually generate\n',
                    '    - "top_left_corner"\n',
                    '    - "nw-resize"\n',
                    '    - "ul_angle"\n',
                    '  - "13-Diagonal_Resize_1-bottom": # manually generate\n',
                    '    - "bottom_right_corner"\n',
                    '    - "se-resize"\n',
                    '    - "lr_angle"\n',
                    '  - "14-Diagonal_Resize_2-top": # manually generate\n',
                    '    - "top_right_corner"\n',
                    '    - "ne-resize"\n',
                    '    - "ur_angle"\n',
                    '  - "14-Diagonal_Resize_2-bottom": # manually generate\n',
                    '    - "bottom_left_corner"\n',
                    '    - "sw-resize"\n',
                    '    - "ll_angle"\n',
                ]
            )
    except Exception as e:
        pout(f"could not create {conf}: {e}", verbose, Level.ERROR)


def getpng(kwargs):
    """.ani to xcursor conversion toolkit
    extract .png files from .ani/.cur files in the target directory.

    Args:
        kwargs (dict): command line arguments parsed by Click library
    """
    verbose = kwargs["verbose"]
    pout("Command line arguments:", verbose, Level.INFO)
    pout(pformat(kwargs, depth=3, indent=4), verbose, Level.INFO)

    if not os.path.exists(kwargs["config"]):
        createConf(kwargs["config"], verbose)
    try:
        with click.open_file(kwargs["config"], "r") as cnf:
            conf = yaml.safe_load(cnf)
    except Exception as e:
        pout(
            "could not open config file: {file}".format(file=kwargs["config"]),
            verbose,
            Level.ERROR,
        )
        sys.exit(1)

    pout("Read config file:", verbose, Level.INFO)
    pout(pformat(conf, depth=3, indent=4), verbose, Level.INFO)
    extract_png.extract(
        target=kwargs["target"],
        config=conf,
        output=kwargs["output"],
        generate_extra=kwargs["generate_extra"],
        verbose=verbose,
    )


def pack(kwargs):
    """.ani to xcursor conversion toolkit
    Package the .png files extracted by getpng into xcursor theme

    Args:
        kwargs (dict): command line arguments parsed by Click library
    """
    verbose = kwargs["verbose"]
    pout("Command line arguments:", verbose, Level.INFO)
    pout(pformat(kwargs, depth=3, indent=4), verbose, Level.INFO)

    if not os.path.exists(kwargs["config"]):
        createConf(kwargs["config"], verbose)
    try:
        with click.open_file(kwargs["config"], "r") as cnf:
            conf = yaml.safe_load(cnf)
    except Exception as e:
        pout(
            "could not open config file: {file}".format(file=kwargs["config"]),
            verbose,
            Level.ERROR,
        )
        sys.exit(1)

    pout("Read config file:", verbose, Level.INFO)
    pout(pformat(conf, depth=3, indent=4), verbose, Level.INFO)

    if kwargs["output"] == None:
        kwargs["output"] = Path(f"./{kwargs['name']}").resolve()

    pack_xcur.pack(
        target=kwargs["target"],
        config=conf,
        output=kwargs["output"],
        name=kwargs["name"],
        verbose=verbose,
    )


def conv(kwargs):
    """.ani to xcursor conversion toolkit
    Chain execution of getpng and pack.

    Args:
        kwargs (dict): command line arguments parsed by Click library
    """
    verbose = kwargs["verbose"]
    pout("Command line arguments:", verbose, Level.INFO)
    pout(pformat(kwargs, depth=3, indent=4), verbose, Level.INFO)

    if not os.path.exists(kwargs["config"]):
        createConf(kwargs["config"], verbose)
    try:
        with click.open_file(kwargs["config"], "r") as cnf:
            conf = yaml.safe_load(cnf)
    except Exception as e:
        pout(
            "could not open config file: {file}".format(file=kwargs["config"]),
            verbose,
            Level.ERROR,
        )
        sys.exit(1)

    pout("Read config file:", verbose, Level.INFO)
    pout(pformat(conf, depth=3, indent=4), verbose, Level.INFO)

    if kwargs["output"] == None:
        kwargs["output"] = Path(f"./{kwargs['name']}").resolve()

    extract_png.extract(
        target=kwargs["target"],
        config=conf,
        output=kwargs["pngout"],
        generate_extra=kwargs["generate_extra"],
        verbose=verbose,
    )
    pack_xcur.pack(
        target=kwargs["pngout"],
        config=conf,
        output=kwargs["output"],
        name=kwargs["name"],
        verbose=verbose,
    )
