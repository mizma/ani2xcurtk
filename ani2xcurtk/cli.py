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

"""Main CLI Setup and Entrypoint."""

from __future__ import absolute_import, division, print_function

# Import the main click library
import click
# Import the sub-command implementations
from .a2xc import a2xc
# Import the version information
from ani2xcurtk._version import __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def cli():
    """cli tool: .ani to xcursor conversion toolkit"""
    pass

@cli.command()
@click.argument(
    'TARGET',
    type=click.Path(exists=True, dir_okay=True, writable=True, resolve_path=True),
    )
@click.option(
    '--output', '-o', default="./output",
    type=click.Path(exists=False, dir_okay=True, writable=True, resolve_path=True),
    metavar='<output>',
    help='Output Directory Path (default: ./output)'
    )
@click.option(
    '--config', '-c', default="./ani2xcurtk.yml",
    type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True),
    metavar='<cfg>',
    help='Configuration File (default: ani2xcurtk.yml)'
    )
@click.option(
    '--generate-extra', '-g', is_flag=True,
    help='Generates extra copies for manual editing'
    )
@click.option(
    '--verbose', '-v', count=True,
    help='output in verbose mode'
    )
def getpng(**kwargs):
    """Extract .cur or .ani files to .png files and the Xcursor theme configs."""
    a2xc.getpng(kwargs)

@cli.command()
@click.argument(
    'TARGET',
    type=click.Path(exists=True, dir_okay=True, writable=True, resolve_path=True),
    )
@click.option(
    '--output', '-o',
    type=click.Path(exists=False, dir_okay=True, writable=True, resolve_path=True),
    metavar='<output>',
    help='Output Directory Path (default: ./NAME)'
    )
@click.option(
    '--name', '-n',
    metavar='<name>',
    help='name of the cursor theme'
    )
@click.option(
    '--config', '-c', default="./ani2xcurtk.yml",
    type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True),
    metavar='<cfg>',
    help='Configuration File (default: ani2xcurtk.yml)'
    )
@click.option(
    '--verbose', '-v', count=True,
    help='output in verbose mode'
    )
def pack(**kwargs):
    """Package the .png files into Xcursor theme."""
    a2xc.pack(kwargs)

@cli.command()
@click.argument(
    'TARGET',
    type=click.Path(exists=True, dir_okay=True, writable=True, resolve_path=True),
    )
@click.option(
    '--pngout', '-p', default='./pngout',
    type=click.Path(exists=False, dir_okay=True, writable=True, resolve_path=True),
    metavar='<pngout>',
    help='Output Directory Path to place all converted png files (default: ./pngout)'
    )
@click.option(
    '--output', '-o',
    type=click.Path(exists=False, dir_okay=True, writable=True, resolve_path=True),
    metavar='<output>',
    help='Output Directory Path (default: ./NAME)'
    )
@click.option(
    '--name', '-n',
    metavar='<name>',
    help='name of the cursor theme'
    )
@click.option(
    '--config', '-c', default="./ani2xcurtk.yml",
    type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True),
    metavar='<cfg>',
    help='Configuration File (default: ani2xcurtk.yml)'
    )
@click.option(
    '--verbose', '-v', count=True,
    help='output in verbose mode'
    )
def conv(**kwargs):
    """Chains getpng and pack in one command. Will not create any extra copy folders for manual editing (-g option for getpng is not available)."""
    a2xc.conv(kwargs)


# Entry point
def main():
    """Main script."""
    cli()

if __name__ == '__main__':
    main()
