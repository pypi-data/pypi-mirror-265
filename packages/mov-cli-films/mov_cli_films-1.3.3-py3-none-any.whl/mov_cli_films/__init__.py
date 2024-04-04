from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mov_cli.plugins import PluginHookData

from .vidsrcme import *
from .vidsrcto import *

plugin: PluginHookData = {
    "version": 1, 
    "scrapers": {
        "DEFAULT": VidSrcToScraper, 
        "vidsrcto": VidSrcToScraper,
        "vidsrcme": VidSrcMeScraper
    }
}

__version__ = "1.3.3"