from bokeh.plotting import curdoc 

############ bokeh utilities #############
def is_env_bokeh():
    """Determine wheather current environment is in Bokeh server"""
    return curdoc().session_context != None

def clear_bokeh_lines(lines):
    for line in lines:
        ds = line.data_source
        ds.data['x'].clear()
        ds.data['y'].clear()
        ds.trigger('data', ds.data, ds.data)
