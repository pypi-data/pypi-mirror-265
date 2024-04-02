from . version import __version__

# patch to keep phoenix moduke importable under old path
from . import siemenscsa, siemensphoenix
siemenscsa.phoenix = siemensphoenix.phoenix

__all__ = ['siemenscsa', 'siemensoog', 'seriesio', 'siemensphoenix']
