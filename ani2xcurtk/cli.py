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
from ani2xcurtk.version import __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def cli():
    """cli tool: .ani to xcursor conversion toolkit"""
    pass

@cli.command()
@click.argument('ARG')
@click.option(
    '--flag', '-f', is_flag=True,
    help='some flag option'
    )
@click.option(
    '--config', '-c', default="./ani2xcurtk.yml",
    type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True),
    metavar='<cfg>',
    help='Configuration File (default: ani2xcurtk.yml)'
    )
@click.option(
    '--fmt', '-f', default="defaultvalue", type=str,
    metavar='<fmt>',
    help='string option'
    )
@click.option(
    '--verbose', '-v', is_flag=True,
    help='output in verbose mode'
    )
def subcmd1(**kwargs):
    """sample subcmd"""
    a2xc.cmd(kwargs)
    pass

@cli.command()
@click.argument('ARG')
@click.option(
    '--message', '-m', multiple=True,
    help='some flag option'
    )
@click.option(
    '--config', '-c', default="./ani2xcurtk.yml",
    type=click.Path(exists=False, dir_okay=False, writable=True, resolve_path=True),
    metavar='<cfg>',
    help='Configuration File (default: ani2xcurtk.yml)'
    )
@click.option(
    '--choice', '-c', type=click.Choice(['choice1', 'choice2']),
    help='choice option'
    )
@click.option(
    '--verbose', '-v', count=True,
    help='output in verbose mode'
    )
def subcmd2(**kwargs):
    """sample subcmd"""
    #a2xc.cmd2(kwargs)
    print(kwargs)
    pass

# Entry point
def main():
    """Main script."""
    cli()

if __name__ == '__main__':
    main()
