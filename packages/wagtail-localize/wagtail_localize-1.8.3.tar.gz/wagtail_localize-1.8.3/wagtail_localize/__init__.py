from .version import get_version


# release must be one of alpha, beta, rc, or final
VERSION = (1, 8, 3, "final", 1)

__version__ = get_version(VERSION)
