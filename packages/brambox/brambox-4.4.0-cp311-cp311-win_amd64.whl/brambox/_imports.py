#
#   Brambox optional dependencies
#   Copyright EAVISE
#
import logging

__all__ = [
    'pygeos',
    'pgpd',
]
log = logging.getLogger(__name__)

try:
    import pgpd
    import pygeos
except ModuleNotFoundError:
    log.warning('PyGEOS is not installed and thus segmentation related functionality will not work')
    pygeos = None
    pgpd = None
