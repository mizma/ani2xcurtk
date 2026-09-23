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


from pathlib import Path
import shutil
import subprocess
import sys
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


def extract(target=None, config=None, output=None, generate_extra=False, verbose=0):
    pout("extract png!", Verbose=verbose, level=Level.DEBUG)
    pout(f"target = {target}", Verbose=verbose, level=Level.DEBUG)
    pout("config = ", Verbose=verbose, level=Level.DEBUG)
    pout(pformat(config, depth=3, indent=4), verbose, Level.DEBUG)
    pout(f"output = {output}", Verbose=verbose, level=Level.DEBUG)
    pout(f"generate_extra = {generate_extra}", Verbose=verbose, level=Level.DEBUG)
    pout(f"Verbose = {verbose}", Verbose=verbose, level=Level.DEBUG)
    # Check that target, config and output are not None, otherwise sys.exit(1) with pout level=Level.ERROR
    if target is None:
        pout("target is required", Verbose=verbose, level=Level.ERROR)
        sys.exit(1)

    if config is None:
        pout("config is required", Verbose=verbose, level=Level.ERROR)
        sys.exit(1)

    if output is None:
        pout("output is required", Verbose=verbose, level=Level.ERROR)
        sys.exit(1)

    target = Path(target)
    output = Path(output)

    if not target.is_dir():
        pout(
            f"target directory does not exist: {target}",
            Verbose=verbose,
            level=Level.ERROR,
        )
        sys.exit(1)

    # Create the output directory if not present (path should be already expanded by the caller)
    output.mkdir(parents=True, exist_ok=True)

    # Get list of .ani/.cur files in target directory
    cursor_files = sorted(
        path
        for path in target.iterdir()
        if path.is_file() and path.suffix.lower() in (".ani", ".cur")
    )

    # Replace spaces in cursor filenames with underscores.
    for cursor_file in cursor_files:
        if " " not in cursor_file.name:
            continue

        new_name = cursor_file.name.replace(" ", "_")
        new_path = cursor_file.with_name(new_name)

        pout(
            f"Renaming {cursor_file.name} -> {new_name}",
            Verbose=verbose,
            level=Level.DEBUG,
        )

        cursor_file.rename(new_path)

    # Refresh the list after renaming.
    cursor_files = sorted(
        path
        for path in target.iterdir()
        if path.is_file() and path.suffix.lower() in (".ani", ".cur")
    )
    # For each .ani/.cur files found as <cursorname>.(ani|cur), run
    #   `mkdir {output}/<cursorname> -p`
    #   `win2xcur {target}/<cursorname>.(ani|cur) -o {output}/<cursorname>`
    for cursor_file in cursor_files:
        cursor_name = cursor_file.stem
        cursor_output = output / cursor_name

        pout(
            f"Extracting {cursor_file.name} -> {cursor_output}",
            Verbose=verbose,
            level=Level.INFO,
        )

        cursor_output.mkdir(parents=True, exist_ok=True)

        subprocess.run(
            [
                "win2xcur",
                str(cursor_file),
                "-o",
                str(cursor_output),
            ],
            check=True,
        )

        # For each output directory, also run
        #   `mkdir {output}/<cursorname>/pngs/`
        #   `xcur2png -d {output}/<cursorname>/pngs/ {output}/<cursorname>/<cursorname>`
        #   `rm {output}/<cursorname>/<cursorname>`
        png_output = cursor_output / "pngs"
        png_output.mkdir(parents=True, exist_ok=True)

        xcur_file = cursor_output / cursor_name

        subprocess.run(
            [
                "xcur2png",
                "-d",
                str(png_output),
                str(xcur_file),
            ],
            cwd=cursor_output,
            check=True,
        )

        if xcur_file.exists():
            xcur_file.unlink()

        # xcur2png generates <cursor_name>.conf with absolute PNG paths.
        # Convert the PNG paths to paths relative to the .conf file.
        conf_file = cursor_output / f"{cursor_name}.conf"

        if conf_file.exists():
            lines = conf_file.read_text().splitlines()

            new_lines = []

            for line in lines:
                if line.startswith("#") or not line.strip():
                    new_lines.append(line)
                    continue

                fields = line.split()

                # Format:
                # size xhot yhot path delay
                if len(fields) >= 5:
                    png_path = Path(fields[3])
                    fields[3] = png_path.relative_to(cursor_output).as_posix()

                new_lines.append("\t".join(fields))

            conf_file.write_text("\n".join(new_lines) + "\n")

    if not generate_extra:
        return

    # Generate Extras defined in "Generate" key in config
    # for each key in "Generate", check if that original cursor directory exists at {output}/<cursorname>
    # If it exists, Iterate over the items and copy {output}/<cursorname> to {output}/<keyname>
    #   i.e. copy {output}/01-normal to {output}/01-normal-mirrored
    # if the item is set to mirror, run `magick mogrify -flip {output}/<keyname>/pngs/*.png`
    generate = config.get("generate", [])

    output_dirs = {
        path.name.casefold(): path for path in output.iterdir() if path.is_dir()
    }

    for generate_group in generate:
        if not isinstance(generate_group, dict):
            pout(f"skip {generate_group}", verbose, Level.DEBUG)
            continue
        pout(f"process {generate_group}", verbose, Level.DEBUG)

        for original_name, extras in generate_group.items():
            original_dir = output_dirs.get(original_name.casefold())

            if original_dir is None:
                pout(
                    f"Skipping extra generation: source does not exist: {output / original_name}",
                    Verbose=verbose,
                    level=Level.DEBUG,
                )
                continue

            for extra_group in extras:
                for extra_name, operation in extra_group.items():
                    extra_dir = output / extra_name

                    pout(
                        f"Generating {extra_name} from {original_dir.name} "
                        f"({operation})",
                        Verbose=verbose,
                        level=Level.DEBUG,
                    )

                    if extra_dir.exists():
                        shutil.rmtree(extra_dir)

                    shutil.copytree(original_dir, extra_dir)

                    # xcur2png generates:
                    #
                    #   <original_name>/<original_name>.conf
                    #
                    # Rename it to:
                    #
                    #   <extra_name>/<extra_name>.conf
                    #
                    # and update the PNG paths inside it.
                    original_conf = extra_dir / f"{original_dir.name}.conf"
                    extra_conf = extra_dir / f"{extra_name}.conf"

                    if original_conf.exists():
                        original_conf.rename(extra_conf)
                    else:
                        pout(
                            f"Expected config file does not exist: {original_conf}",
                            Verbose=verbose,
                            level=Level.ERROR,
                        )

                    operation = operation.casefold()
                    if operation == "mirror":
                        for png_file in (extra_dir / "pngs").glob("*.png"):
                            subprocess.run(
                                [
                                    "magick",
                                    "mogrify",
                                    "-flop",
                                    str(png_file),
                                ],
                                check=True,
                            )

                    elif operation != "copy":
                        pout(
                            f"Unknown Generate operation {operation!r} "
                            f"for {extra_name!r}",
                            Verbose=verbose,
                            level=Level.ERROR,
                        )

    # Sample config in yaml
    # generate:
    #   - "01-normal":
    #     - "01-normal-mirrored": "mirror"
    #   - "11-Vertical Resize":
    #     - "11-Vertical Resize-top": "copy"
    #     - "11-Vertical Resize-bottom": "copy"
    #   - "12-Horizontal Resize":
    #     - "12-Horizontal Resize-left": "copy"
    #     - "12-Horizontal Resize-right": "copy"
    #   - "13-Diagonal Resize 1":
    #     - "13-Diagonal Resize 1-top": "copy"
    #     - "13-Diagonal Resize 1-bottom": "copy"
    #   - "14-Diagonal Resize 2":
    #     - "14-Diagonal Resize 2-top": "copy"
    #     - "14-Diagonal Resize 2-bottom": "copy"
