#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integrates catalog export, diagnose and compare into RegScale"""
from pathlib import Path

# standard python imports
import click
from rich.console import Console

from regscale.core.app.utils.catalog_utils.compare_catalog import display_menu as start_compare
from regscale.core.app.utils.catalog_utils.diagnostic_catalog import display_menu as start_diagnostic
from regscale.core.app.utils.catalog_utils.download_catalog import display_menu as start_download
from regscale.core.app.utils.catalog_utils.update_catalog_v2 import display_menu as start_update
from regscale.core.app.utils.catalog_utils.update_catalog_v2 import import_catalog


@click.group()
def catalog():
    """Export, diagnose, and compare catalog from RegScale.com/regulations."""


@catalog.command(name="import")
@click.option(
    "--catalog_path",
    prompt="Enter the path of the Catalog file to import",
    help="RegScale will load the Catalog",
    type=click.Path(exists=True),
    required=True,
)
def import_(catalog_path: str):
    """Import a catalog.json file into RegScale."""
    console = Console()
    res = import_catalog(Path(catalog_path))
    dat = res.json()
    if dat.get("success"):
        console.print(
            f"Catalog #{dat['catalogId']} imported successfully with {dat['importedItemCount']} " + "controls.",
            style="bold green",
        )
    else:
        console.print(res.json().get("message"), style="bold red")


@catalog.command(name="download")
def export():
    """Export catalog from RegScale.com/regulations."""
    start_download()


@catalog.command(name="diagnose")
def diagnostic():
    """Diagnose catalog and output metadata."""
    start_diagnostic()


@catalog.command(name="compare")
def compare():
    """Run diagnostic and compare catalogs while reporting differences."""
    start_compare()


@catalog.command(name="update")
def update():
    """[BETA] Update application instance catalog with new catalog data."""
    start_update()
