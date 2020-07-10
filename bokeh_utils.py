from bokeh.plotting import curdoc
import signal


def is_env_bokeh():
    """Determine wheather current environment is in Bokeh server"""
    return curdoc().session_context != None


def clear_bokeh_lines(lines, update=True):
    for line in lines:
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
        if value_backup in options and (default_value is not None and value_backup != default_value):
            selector.value = value_backup
        else:
            selector.value = options[0]


def set_on_session_destroyed(on_session_destroyed):
    curdoc().on_session_destroyed(lambda session_context: on_session_destroyed())

    sig_t_handler = signal.getsignal(signal.SIGTERM)
    sig_i_handler = signal.getsignal(signal.SIGINT)
    sig_h_handler = signal.getsignal(signal.SIGHUP)

    def is_ignore_hanlder(h):
        return h == signal.SIG_DFL or h == signal.SIG_IGN or h is None

    if is_ignore_hanlder(sig_t_handler):
        sig_t_handler = None
    if is_ignore_hanlder(sig_i_handler):
        sig_i_handler = None
    if is_ignore_hanlder(sig_h_handler):
        sig_h_handler = None

    def signal_handler(s, f, dfl_handler):
        on_session_destroyed()
        if dfl_handler is not None:
            dfl_handler()

    # Set signal handlers
    signal.signal(signal.SIGTERM, lambda s, f: signal_handler(s, f, sig_t_handler))
    signal.signal(signal.SIGINT, lambda s, f: signal_handler(s, f, sig_i_handler))
    signal.signal(signal.SIGHUP, lambda s, f: signal_handler(s, f, sig_h_handler))

