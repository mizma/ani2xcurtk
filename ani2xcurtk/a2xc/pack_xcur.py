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

import re
import shutil
import subprocess
import sys
from PIL import Image
from pathlib import Path
from pprint import pformat
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


def pack(target="", config=None, output=None, name=None, verbose=0):
    pout("pack xcursor!", Verbose=verbose, level=Level.DEBUG)
    pout(f"target = {target}", Verbose=verbose, level=Level.DEBUG)
    pout("config = ", Verbose=verbose, level=Level.DEBUG)
    pout(pformat(config, depth=3, indent=4), verbose, Level.DEBUG)
    pout(f"output = {output}", Verbose=verbose, level=Level.DEBUG)
    pout(f"name = {name}", Verbose=verbose, level=Level.DEBUG)
    pout(f"Verbose = {verbose}", Verbose=verbose, level=Level.DEBUG)

    # Check that config and name are not None.
    if config is None:
        pout(
            "config is required",
            Verbose=verbose,
            level=Level.ERROR,
        )
        sys.exit(1)

    if name is None:
        pout(
            "name is required",
            Verbose=verbose,
            level=Level.ERROR,
        )
        sys.exit(1)

    target = Path(target)

    # If output is None, set to $cwd/{name}.
    if output is None:
        output = Path.cwd() / name
    else:
        output = Path(output)

    # Check that target exists.
    if not target.is_dir():
        pout(
            f"target directory does not exist: {target}",
            Verbose=verbose,
            level=Level.ERROR,
        )
        sys.exit(1)

    # Check if output is a directory and is empty.
    if output.exists():
        if not output.is_dir():
            pout(
                f"output exists but is not a directory: {output}",
                Verbose=verbose,
                level=Level.ERROR,
            )
            sys.exit(1)

        if any(output.iterdir()):
            pout(
                f"output directory is not empty: {output}",
                Verbose=verbose,
                level=Level.ERROR,
            )
            sys.exit(1)
    else:
        output.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Generate different sizes
    # ------------------------------------------------------------------

    sizes = config.get("sizes", [])

    if not isinstance(sizes, list):
        pout(
            "config['sizes'] must be a list",
            Verbose=verbose,
            level=Level.ERROR,
        )
        sys.exit(1)

    # Match the original PNG naming convention:
    #
    #   <png_name>_NNN.png
    #
    # while deliberately NOT matching generated files such as:
    #
    #   <png_name>_NNN_40.png
    #
    source_png_pattern = re.compile(r"^(.+)_([0-9]+)\.png$", re.IGNORECASE)

    cursor_dirs = sorted(path for path in target.iterdir() if path.is_dir())

    for cursor_dir in cursor_dirs:
        png_dir = cursor_dir / "pngs"

        if not png_dir.is_dir():
            pout(
                f"Skipping {cursor_dir.name}: pngs directory does not exist",
                Verbose=verbose,
                level=Level.DEBUG,
            )
            continue

        # Find only the original PNGs, not previously generated size PNGs.
        source_png_pattern = re.compile(
            r"^(.+)_([0-9]{3})\.png$",
            re.IGNORECASE,
        )

        generated_png_pattern = re.compile(
            r"^(.+)_([0-9]{3})_([0-9]+)\.png$",
            re.IGNORECASE,
        )

        source_pngs = sorted(
            path
            for path in png_dir.iterdir()
            if (
                path.is_file()
                and path.suffix.lower() == ".png"
                and source_png_pattern.match(path.name)
                and not generated_png_pattern.match(path.name)
            )
        )

        with click.progressbar(
            source_pngs, label=f"generating icon sizes for {cursor_dir}"
        ) as src_pngs:
            for png_file in src_pngs:
                match = source_png_pattern.match(png_file.name)

                if match is None:
                    continue

                png_name = match.group(1)
                frame_number = match.group(2)

                upscale_size = 128
                try:
                    with Image.open(png_file) as image:
                        original_size, _ = image.size
                        upscale_size = original_size * 4
                except Exception as e:
                    pout(
                        f"Could not open {png_file}, using {upscale_size} for intermediate size",
                        Verbose=verbose,
                        level=Level.DEBUG,
                    )

                for size in sizes:
                    generated_name = f"{png_name}_{frame_number}_{size}.png"
                    generated_file = png_dir / generated_name

                    if generated_file.exists():
                        pout(
                            f"Skipping existing {generated_file}",
                            Verbose=verbose,
                            level=Level.DEBUG,
                        )
                        continue

                    pout(
                        f"Generating {generated_file}",
                        Verbose=verbose,
                        level=Level.DEBUG,
                    )

                    subprocess.run(
                        [
                            "magick",
                            str(png_file),
                            "-filter",
                            "Point",
                            "-resize",
                            f"{upscale_size}x{upscale_size}",
                            "-filter",
                            "Catrom",
                            "-resize",
                            f"{size}x{size}",
                            str(generated_file),
                        ],
                        check=True,
                    )

    # ------------------------------------------------------------------
    # Update .conf files with generated size PNGs
    # ------------------------------------------------------------------

    for cursor_dir in cursor_dirs:
        conf_files = sorted(cursor_dir.glob("*.conf"))

        if not conf_files:
            pout(
                f"Skipping {cursor_dir.name}: no .conf file found",
                Verbose=verbose,
                level=Level.DEBUG,
            )
            continue

        for conf_file in conf_files:
            lines = conf_file.read_text().splitlines()

            entries = set()

            for line in lines:
                if not line.strip() or line.lstrip().startswith("#"):
                    continue

                fields = line.split()
                if len(fields) < 5:
                    continue

                size, xhot, yhot, png_path, delay = fields[:5]

                entries.add("\t".join([size, xhot, yhot, png_path, delay]))

                png_filename = Path(png_path).name
                match = source_png_pattern.match(png_filename)

                if match is None:
                    continue

                png_name, frame_number = match.groups()

                source_png = cursor_dir / png_path
                with Image.open(source_png) as image:
                    original_width, original_height = image.size

                original_xhot = int(xhot)
                original_yhot = int(yhot)

                for generated_size in sizes:
                    generated_filename = (
                        f"{png_name}_{frame_number}_{generated_size}.png"
                    )

                    new_xhot = int(
                        original_xhot
                        * (generated_size - 1)
                        / (original_width -1)
                    ) if original_width > 1 else 0

                    new_yhot = int(
                        original_yhot
                        * (generated_size - 1)
                        / (original_height -1)
                    ) if original_height > 1 else 0

                    entries.add(
                        "\t".join(
                            [
                                str(generated_size),
                                str(new_xhot),
                                str(new_yhot),
                                f"pngs/{generated_filename}",
                                delay,
                            ]
                        )
                    )

            # Sort generated entries by size, then frame number.
            sorted_entries = sorted(
                entries,
                key=lambda line: (
                    int(line.split()[0]),
                    line,
                ),
            )

            header = "#size\txhot\tyhot\tPath to PNG image\tdelay"

            conf_file.write_text("\n".join([header, *sorted_entries]) + "\n")

    # ------------------------------------------------------------------
    # Generate xcursor files
    # ------------------------------------------------------------------

    cursor_files = {}

    for cursor_dir in cursor_dirs:
        conf_files = sorted(cursor_dir.glob("*.conf"))

        for conf_file in conf_files:
            cursor_name = conf_file.stem
            cursor_file = cursor_dir / cursor_name

            pout(
                f"Generating xcursor {cursor_file}",
                Verbose=verbose,
                level=Level.DEBUG,
            )

            subprocess.run(
                [
                    "xcursorgen",
                    conf_file.name,
                    cursor_file.name,
                ],
                cwd=cursor_dir,
                check=True,
            )

            cursor_files[cursor_name.casefold()] = cursor_file

    # ------------------------------------------------------------------
    # Copy/symlink generated cursor files according to mappings
    #
    # Mappings are processed in YAML order. If a cursor name appears
    # multiple times, the later definition replaces the earlier one.
    # ------------------------------------------------------------------

    cursors_output = output / "cursors"
    cursors_output.mkdir(parents=True, exist_ok=True)

    mappings = config.get("mappings", [])

    for mapping_group in mappings:
        if not isinstance(mapping_group, dict):
            continue

        for cursor_name, mapping_names in mapping_group.items():
            source_cursor = cursor_files.get(cursor_name.casefold())

            if source_cursor is None:
                pout(
                    f"Skipping mapping for {cursor_name!r}: cursor does not exist",
                    Verbose=verbose,
                    level=Level.ERROR,
                )
                continue

            if not isinstance(mapping_names, list) or not mapping_names:
                pout(
                    f"Invalid mapping for {cursor_name!r}: expected a non-empty list",
                    Verbose=verbose,
                    level=Level.ERROR,
                )
                continue

            primary_name = mapping_names[0]
            primary_file = cursors_output / primary_name

            # Remove an existing mapping so that a later YAML definition
            # replaces an earlier one.
            if primary_file.is_symlink() or primary_file.exists():
                primary_file.unlink()

            shutil.copy2(source_cursor, primary_file)

            pout(
                f"Copying {source_cursor} -> {primary_file}",
                Verbose=verbose,
                level=Level.DEBUG,
            )

            # Remaining mappings are symbolic links to the primary file.
            for link_name in mapping_names[1:]:
                link_file = cursors_output / link_name

                # Remove an existing mapping so that a later YAML
                # definition replaces an earlier one.
                if link_file.is_symlink() or link_file.exists():
                    link_file.unlink()

                link_file.symlink_to(primary_file.name)

                pout(
                    f"Linking {link_file} -> {primary_file.name}",
                    Verbose=verbose,
                    level=Level.DEBUG,
                )

    # ------------------------------------------------------------------
    # Generate index.theme
    # ------------------------------------------------------------------

    comment = input("Comment (leave empty to omit): ")

    index_lines = [
        "[Icon Theme]",
        f"Name={name}",
    ]

    if comment:
        index_lines.append(f"Comment={comment}")

    index_lines.append("Inherits=breeze_cursors")

    (output / "index.theme").write_text("\n".join(index_lines) + "\n")
