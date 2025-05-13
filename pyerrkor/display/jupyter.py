from IPython.display import display, HTML


def display_jupyter_error(name, message):
    # display(HTML(f'<span style="color:magenta;">{name}</span>: {message}'))
    display(HTML(f'<span style="color:red;">{name}</span>: {message}'))
