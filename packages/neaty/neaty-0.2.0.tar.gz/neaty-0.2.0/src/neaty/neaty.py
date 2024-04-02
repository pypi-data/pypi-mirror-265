import sys
import inspect


class _LoggerMode:

    def __init__(self, verbose, debug):
        self.verbose = verbose
        self.debug = debug

    def clone(self, **kwargs):
        out = {
            'debug': self.debug,
            'verbose': self.verbose,
        }
        out.update(kwargs)
        return self.__class__(**out)


class Logger:
    """
    Base class for all loggers.

    It's not recommended to instantiate this class directly.

    See module docstring for details.
    """

    ltype = '_base_'

    _printers = [
        '_debug',
        '_die',
        '_mkusage',
        '_think',
        '_warn',
    ]

    _pubapi = [
        'debug',
        'debugv',
        'die',
        'mkusage',
        'think',
        'thinkv',
        'warn',
        'warnv',
    ]

    def __init__(self, mode):
        self.mode = mode

    def _stackfix(self, word):

        def is_printers(f):
            return f[3] in self._printers

        def is_pubapi(f):
            return f[3] in self._pubapi

        def is_us(f):
            return f[3] == '_stackfix'

        frames = inspect.stack()
        focus = frames.pop(0)
        assert is_us(focus)
        focus = frames.pop(0)
        assert is_printers(focus)
        focus = frames.pop(0)
        assert is_pubapi(focus)
        focus = frames.pop()

        def fnname(F):
            return F[3] + '():'

        if len(frames) == 0:
            prefix = focus[1].split('/')[-1] + ':'
        elif len(frames) < 3:
            prefix = ''.join([fnname(f) for f in frames])
        else:
            prefix = ''.join([fnname(frames[0]), '..', fnname(frames[-1])])
        return word + ':' + prefix

    def debug(self, msg):
        """
        Emit debug message *msg*, if debug mode is on.

        Debug messages are prefixed with a brief in-line call stack
        information.
        """
        if not self.mode.debug:
            return
        self._debug(msg)

    def debugv(self, vname, vcont):
        """
        Emit debug message showing value *vcont* of variable named *vname*

        Shorthand for debug('%s=%r' % (vname, vcont)); a bit more suitable
        when you want to show value of a variable.
        """
        if not self.mode.debug:
            return
        self._debug('%s=%r' % (vname, vcont))

    def die(self, msg, exit=False):
        """
        Emit warning message *msg* and possibly exit current process.

        If *exit* is on, after emitting the message process will exit with 3.
        """
        self._die(msg)
        if exit:
            sys.exit(3)

    def update_mode(self, debug=None, verbose=None):
        """
        Update state of this logger.
        """
        self.mode = self.mode.clone(debug=debug, verbose=verbose)

    def mkusage(self, msg, exit=False):
        """
        Emit usage message *msg* and possibly exit current process.

        If *exit* is on, after emitting the message process will exit with 2.
        """
        self._mkusage(msg)
        if exit:
            sys.exit(2)

    def think(self, msg):
        """
        Emit message *msg* if verbose mode is on.
        """
        if not self.mode.verbose:
            return
        self._think(msg)

    def thinkv(self, vname, vcont):
        """
        Emit message showing value *vcont* of variable named *vname*

        Shorthand for think('%s=%r' % (vname, vcont)); a bit more suitable
        when you want to show value of a variable.
        """
        if not self.mode.verbose:
            return
        self._think('%s=%r' % (vname, vcont))

    def warn(self, msg):
        """
        Emit message *msg*.
        """
        self._warn(msg)

    def warnv(self, vname, vcont):
        """
        Emit warning message showing value *vcont* of variable named *vname*

        Shorthand for warn('%s=%r' % (vname, vcont)); a bit more suitable
        when you want to show value of a variable.
        """
        self._warn('%s=%r' % (vname, vcont))


class HtmlLogger(Logger):
    """
    Logger which wraps messages to HTML.
    """

    ltype = 'html'

    def _pre(self, cname, msg):
        return "<pre class='%s'>%s</pre>" % (cname, msg)

    def _span(self, cname, msg):
        return "<span class='%s'>%s</span>" % (cname, msg)

    def _twrite(self, cname, msg):
        sys.stderr.write(self._pre(cname, msg) + '\n')

    def _debug(self, msg):
        stackfix = self._stackfix('debug')
        self._twrite('debug', self._span('caller', stackfix + msg))

    def _die(self, msg):
        self._twrite('fatal', msg)

    def _think(self, msg):
        self._twrite('think', msg)

    def _mkusage(self, msg):
        self._twrite('usage', msg)

    def _warn(self, msg):
        self._twrite('warning', msg)


class ColorLogger(Logger):
    """
    Logger that adds ANSI color codes to the output messages
    """

    ltype = 'color'

    codes = {
        'black': "\033[0;30m",
        'red': "\033[0;31m",
        'green': "\033[0;32m",
        'yellow': "\033[0;33m",
        'blue': "\033[0;34m",
        'magenta': "\033[0;35m",
        'cyan': "\033[0;36m",
        'white': "\033[0;37m",
        'lblack': "\033[1;30m",
        'lred': "\033[1;31m",
        'lgreen': "\033[1;32m",
        'lyellow': "\033[1;33m",
        'lblue': "\033[1;34m",
        'lmagenta': "\033[1;35m",
        'lcyan': "\033[1;36m",
        'lwhite': "\033[1;37m",
        'none': "\033[1;0m",
    }

    def _cwrap(self, color, msg):
        return self.codes[color] + str(msg) + self.codes['none']

    def _cwrite(self, color, msg):
        sys.stderr.write(self._cwrap(color, msg) + '\n')

    def _debug(self, msg):
        sys.stderr.write(
            self._cwrap('lblue', self._stackfix('debug'))
            + str(msg)
            + '\n')

    def _die(self, msg):
        self._cwrite('lred', msg)

    def _think(self, msg):
        self._cwrite('lblack', msg)

    def _mkusage(self, msg):
        self._cwrite('yellow', msg)

    def _warn(self, msg):
        self._cwrite('lred', msg)


class PlainLogger(Logger):
    """
    Plain text logger with no color codes.
    """

    ltype = 'plain'

    def _debug(self, msg):
        sys.stderr.write(
            '%s%s\n' % (self._stackfix('debug'), msg)
        )

    def _die(self, msg):
        sys.stderr.write('%s\n' % msg)

    def _think(self, msg):
        sys.stderr.write('%s\n' % msg)

    def _mkusage(self, msg):
        sys.stderr.write('%s\n' % msg)

    def _warn(self, msg):
        sys.stderr.write('%s\n' % msg)


def make_logger(ltype='plain', verbose=False, debug=False):
    """
    Create new logger of type *ltype*.

    *ltype* may be 'forcecolor', 'html', 'plain' or 'color'.  In the
    first three cases, logger will be of corresponding type: ColorLogger,
    HtmlLogger, PlainLogger, respectively.  If *ltype* is *color*, detection
    of terminal type will be performed, and logger will be ColorLogger if
    stderr is a TTY, and PlainLogger otherwise.
    """
    mode = _LoggerMode(debug=debug, verbose=verbose)
    if ltype == 'forcecolor':
        return ColorLogger(mode)
    elif ltype == 'color':
        if sys.stderr.isatty():
            return ColorLogger(mode)
        return PlainLogger(mode)
    elif ltype == 'html':
        return HtmlLogger(mode)
    elif ltype == 'plain':
        return PlainLogger(mode)
    else:
        fallback = PlainLogger(mode)
        fallback.warn("unknown logger type; falling back to 'plain': %s"
                      % ltype)
        return fallback


__all__ = [
    'ColorLogger',
    'HtmlLogger',
    'PlainLogger',
    'make_logger',
]
