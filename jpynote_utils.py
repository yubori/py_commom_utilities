def get_environment():
    # from https://qiita.com/implicit_none/items/a7aa06ba442bb84ba5ca
    try:
        env = get_ipython().__class__.__name__
        if env == 'ZMQInteractiveShell':
            return 'Jupyter'
        elif env == 'TerminalInteractiveShell':
            return 'IPython'
        else:
            return 'OtherShell'
    except NameError:
        return 'Interpreter'
    
def is_env_notebook():
    """Determine wheather current environment is in Jupyter Notebook"""
    return get_environment() == 'Jupyter'

