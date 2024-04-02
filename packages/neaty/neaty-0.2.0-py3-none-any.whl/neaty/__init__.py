from .neaty import make_logger
from .neaty import Logger
from . import log
from ._meta import VERSION as __version__

__doc__ = """
Simple terminal logger.

It's not recommended to instantiate loggers directly.

If you want to control type and mode of logger, use neaty.make_logger()
factory.

If you want to just start logging, use 'neaty.log', which creates global logger
based on environment variables `NEATY`, `NEATY_DEBUG` and `NEATY_VERBOSE`.

As a simplest possible example, consider following script:

    #!/usr/bin/python3

    import neaty.log as LOG

    LOG.debug("...")
    LOG.think("umm")
    LOG.warn("hey!")

if the above script is called from the terminal:

    NEATY=color NEATY_VERBOSE=true NEATY_DEBUG=true \\
      ./script

it will print all three messages to stderr.  The messages will be automatically
colored if stderr is a TTY.

See methods of neaty.Logger to see what logging functions are available.
"""

__all__ = [
    'Logger',
    'log',
    'make_logger',
]
