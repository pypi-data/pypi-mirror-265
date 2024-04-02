import os as _os

import neaty
import neaty.neaty


def _envbool(name, default):
    """
    Read boolean from environment variable *name* or from *default*.

    Expect environment variable to be 'true' or 'false', return
    respective boolean.  Raise ValueError if the value is different.
    If the variable is unset, use *default* as default value.
    """
    value = _os.environ.get(name, default)
    if value == 'true':
        return True
    elif value == 'false':
        return False
    else:
        raise ValueError("invalid value: %s=%s" % (name, value))


_logger = neaty.make_logger(
    debug=_envbool('NEATY_DEBUG', 'false'),
    verbose=_envbool('NEATY_VERBOSE', 'false'),
    ltype=_os.environ.get('NEATY', 'plain'),
)


debug = _logger.debug
debugv = _logger.debugv
die = _logger.die
update_mode = _logger.update_mode
ltype = _logger.ltype
mode = _logger.mode
mkusage = _logger.mkusage
think = _logger.think
thinkv = _logger.thinkv
warn = _logger.warn
warnv = _logger.warnv


__all__ = [
    'debug',
    'debugv',
    'die',
    'mkusage',
    'mode',
    'think',
    'thinkv',
    'warn',
    'warnv',
]
