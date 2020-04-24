############ common utilities #############
def check_range(val_name, val, min_, max_):
    if val < min_ or max_ < val:
        raise ValueError("Invalid '{}': range is [{},{}] but {}".format(val_name, min_, max_, val))

