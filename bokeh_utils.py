from bokeh.plotting import curdoc
import platform
import signal


def is_env_bokeh():
    """Determine whether current environment is in Bokeh server"""
    return curdoc().session_context is not None


def clear_bokeh_line(line, update=True):
    ds = line.data_source
    ds.data['x'].clear()
    ds.data['y'].clear()
    if update:
        ds.trigger('data', ds.data, ds.data)


def update_selector(selector, options, default_value=None):
    options.sort()
    value_backup = selector.value
    selector.options = options
    if len(options) == 0:
        selector.value = ""
    else:
        if value_backup in options and (default_value is None or value_backup != default_value):
            selector.value = value_backup
        else:
            selector.value = options[0]


def set_on_session_destroyed(on_session_destroyed):
    """Register an on_destloy callback for both of bokeh and system

    This func registers an on_destloy callback for both of bokeh and system.
    For system, the callback is registered for SIGTERM, SIGINT, and SIGHUP except Windows.

    Parameters
    ----------
    on_session_destroyed: function
        A callback function that has no argument.
    """

    curdoc().on_session_destroyed(lambda session_context: on_session_destroyed())

    def signal_handler(s, f, dfl_handler):
        on_session_destroyed()
        if dfl_handler is not None:
            dfl_handler()

    def is_ignore_hanlder(h):
        return h == signal.SIG_DFL or h == signal.SIG_IGN or h is None

    def set_handler(sig):
        dfl_handler = signal.getsignal(sig)

        if is_ignore_hanlder(dfl_handler):
            dfl_handler = None

        signal.signal(sig, lambda s, f: signal_handler(s, f, dfl_handler))

    signals = [signal.SIGTERM, signal.SIGINT]
    if platform.system() != 'Windows':
        signals.append(signal.SIGHUP)

    for sig in signals:
        set_handler(sig)