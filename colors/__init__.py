import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd

import validate

# Read the colors file (don't use utils.read_csv since it might create a circular import)
all_colors = pd.read_csv("./colors/colors.csv", index_col=0)


def get(color_name, value, *, alpha=1, format="hex"):
    """
    Return the HEX value for a specific color name and value
    """
    assert validate.is_color_name(color_name)
    assert validate.is_color_value(value)
    assert validate.is_number(alpha, min_value=0, max_value=1)
    assert validate.is_color_format(format)

    # Get the color
    hex_color = all_colors.loc[value, color_name]

    if format == "hex":
        hex_alpha = hex(round(alpha * 255))[2:].upper().rjust(2, "0")
        return f"{hex_color}{hex_alpha}"
    elif format == "rgb":
        return f"rgb({int(hex_color[1:3], 16)}, {int(hex_color[3:5], 16)}, {int(hex_color[5:7], 16)})"
    elif format == "rgba":
        return f"rgba({int(hex_color[1:3], 16)}, {int(hex_color[3:5], 16)}, {int(hex_color[5:7], 16)}, {alpha})"


def primary(*, alpha=0.8):
    """
    Get the primary color
    """
    assert validate.is_number(alpha, min_value=0, max_value=1)

    return get("blue", 700, alpha=alpha)


def secondary(*, alpha=0.8):
    """
    Get the secondary color
    """
    assert validate.is_number(alpha, min_value=0, max_value=1)

    return get("green", 600, alpha=alpha)


def tertiary(*, alpha=0.8):
    """
    Get the tertiary color
    """
    assert validate.is_number(alpha, min_value=0, max_value=1)

    return get("gray", 500, alpha=alpha)


def technology_type(technology_type, *, alpha=0.8):
    """
    Get the color for a specific technology type
    """
    assert validate.is_technology_type(technology_type)
    assert validate.is_number(alpha, min_value=0, max_value=1)

    if technology_type == "production":
        return get("blue", 600, alpha=alpha)
    if technology_type == "storage":
        return get("red", 600, alpha=alpha)


def technology(technology_name, *, alpha=0.8):
    """
    Get the color for a specific technology
    """
    assert validate.is_technology(technology_name)
    assert validate.is_number(alpha, min_value=0, max_value=1)

    if technology_name == "pv":
        return get("amber", 400, alpha=alpha)
    if technology_name == "onshore":
        return get("sky", 400, alpha=alpha)
    if technology_name == "offshore":
        return get("teal", 700, alpha=alpha)
    if technology_name == "lion":
        return get("rose", 500, alpha=alpha)
    if technology_name == "hydrogen":
        return get("indigo", 600, alpha=alpha)


def random(color=None, value=None, alpha=0.8):
    """
    Get a random color
    """
    assert validate.is_color_name(color, required=False)
    assert validate.is_color_value(value, required=False)
    assert validate.is_number(alpha, min_value=0, max_value=1)

    # Get a random color and value if not defined
    if color is None:
        color = all_colors.columns[np.random.randint(0, len(all_colors.columns))]
    if value is None:
        value = all_colors.index[np.random.randint(0, len(all_colors.index))]

    # Get the color code
    return get(color, value, alpha=alpha)


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
