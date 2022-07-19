import streamlit as st
from matplotlib.colors import LinearSegmentedColormap

import validate
import utils


def get(color, value, *, alpha=1):
    """
    Return the HEX value for a specific color and value
    """
    assert validate.is_color_name(color)
    assert validate.is_color_value(value)
    assert validate.is_number(alpha, min_value=0, max_value=1)

    colors = utils.read_csv(utils.path("colors", "colors.csv"), index_col=0)
    alpha_hex = hex(round(alpha * 255))[2:].upper().rjust(2, "0")
    return f"{colors.loc[value, color]}{alpha_hex}"


def technology(technology_name):
    """
    Get the color for a specific technology
    """
    assert validate.is_technology(technology_name)

    if technology_name == "pv":
        return get("amber", 400)
    if technology_name == "onshore":
        return get("sky", 400)
    if technology_name == "offshore":
        return get("teal", 700)
    if technology_name == "lion":
        return get("rose", 500)
    if technology_name == "hydrogen":
        return get("indigo", 600)


def list():
    """
    Return a list of all available colors
    """
    colors = utils.read_csv(utils.path("colors", "colors.csv"), index_col=0)
    return colors.columns.tolist()


def colormap(color1, color2=None, *, alpha=1):
    """
    Return a colormap based on one or two colors
    """
    assert validate.is_color_name(color1)
    assert validate.is_color_name(color2, required=False)
    assert validate.is_number(alpha, min_value=0, max_value=1)

    # Create a list with colors and a name for the colormap
    if color2 is None:
        name = f"model:{color1}"
        color_list = [get(color1, value, alpha=alpha) for value in range(100, 1000, 100)]
    else:
        name = f"model:{color1}-{color2}"
        color_list1 = [get(color1, value, alpha=alpha) for value in range(900, 0, -100)]
        color_list2 = [get(color2, value, alpha=alpha) for value in range(100, 1000, 100)]
        color_list = color_list1 + color_list2

    # Return the colormap
    colormap = LinearSegmentedColormap.from_list(name, color_list)
    return colormap
