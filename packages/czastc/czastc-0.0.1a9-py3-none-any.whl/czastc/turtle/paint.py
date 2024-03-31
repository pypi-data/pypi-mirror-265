"""
Some functions of turtle graphics.
"""
from turtle import Turtle
from typing import Tuple, Optional, Union
from math import pi, sin, tan
RGBInt = Union[list[int, int, int], Tuple[int, int, int]]
RGBIntList = Union[list[RGBInt], Tuple[RGBInt]]
ColorInt = Union[RGBIntList, RGBInt]
RGBFloat = Union[list[float, float, float], Tuple[float, float, float]]
RGBFloatList = Union[list[RGBFloat], Tuple[RGBFloat]]
ColorFloat = Union[RGBFloatList, RGBFloat]
Color = Union[RGBInt, RGBFloat]
ColorList = Union[list[Color], Tuple[Color], Color]
OptionalColor = Optional[ColorList]
def get_color_type(colors: Union[ColorInt, ColorFloat]) -> str:
    """
    Identifies the type of color data provided

    Args:
        colors (Union[ColorInt, ColorFloat]): A tuple or list 
            representing color values.

    Raises:
        TypeError: Raised if the color type is invalid.

    Returns:
        str: A string indicating the type of color data ("int", "float", 
            "int list", "float list")
    """
    if isinstance(colors[0], (list, tuple)):
        for color in colors:
            if all(isinstance(color_value, int) for color_value in color):
                result = "int list"
            elif all(isinstance(color_value, float) for color_value in color):
                result = "float list"
            else:
                raise TypeError("Invalid color type.")
    else:
        if all(isinstance(color_value, int) for color_value in colors):
            result = "int"
        elif all(isinstance(color_value, float) for color_value in colors):
            result = "float"
        else:
            raise TypeError("Invalid color type.")
    return result


def is_valid_rgb(colors: Union[ColorInt, ColorFloat]) -> bool:
    """
    Checks if the RGB color values are valid.

    Args:
        colors (Union[ColorInt, ColorFloat]): A tuple or list representing
            color values.

    Returns:
        bool: True if all the RGB values are valid, False otherwise.
    """
    color_type = get_color_type(colors)
    if color_type == "int" and len(colors) == 3:
        return all(0 <= color_value <= 255 for color_value in colors)
    if color_type == "float" and len(colors) == 3:
        return all(0.0 <= color_value <= 1.0 for color_value in colors)
    if color_type == "int float":
        for color in colors:
            if len(color) != 3:
                return False
            if not all(color_value < 0 <= 255 for color_value in colors):
                return False
    return True


def int_color(float_colors: ColorFloat) -> ColorInt:
    """
    Converts a floating point RGB color to an integer RGB color.

    Args:
        float_colors (ColorFloat): A tuple or list representing the RGB color 
            in floating point format.

    Raises:
        ValueError: Raised if the input does not represent a valid RGB color.

    Returns:
        ColorInt: A tuple or list representing the RGB color in integer format.
    """
    int_colors = []
    color_type = get_color_type(float_colors)
    if color_type == "float list":
        for rgb_color in float_colors:
            color = []
            for i in rgb_color:
                if 0 <= i <= 1:
                    color.append(int(i * 255))
                else:
                    raise ValueError("Invalid RGB color.")
            int_colors.append(color)
    elif color_type == "float":
        color = []
        for i in float_colors:
            if 0 <= i <= 1:
                color.append(int(i * 255))
            else:
                raise ValueError("Invalid RGB color.")
        int_colors = color[:]
    else:
        raise ValueError("Invalid RGB color.")
    return int_colors


def float_color(int_colors: ColorInt) -> ColorFloat:
    """
    Converts an integer RGB color to a floating point RGB color.

    Args:
        int_colors (ColorInt): A tuple or list representing the RGB 
            color in integer format.

    Raises:
        ValueError: If the input does not represent a valid RGB color.

    Returns:
        ColorInt: A tuple or list representing the RGB color in floating 
            point format.
    """
    float_colors = []
    color_type = get_color_type(int_colors)
    if color_type == "int list":
        for rgb_color in int_colors:
            color = []
            for i in rgb_color:
                if 0 <= i <= 255:
                    color.append(i / 255.0)
                else:
                    raise ValueError("Invalid RGB color.")
            float_colors.append(color)
    elif color_type == "int":
        color = []
        for i in int_colors:
            if 0 <= i <= 255:
                color.append(int(i / 255.0))
            else:
                raise ValueError("Invalid RGB color.")
        float_colors = color[:]
    else:
        raise ValueError("Invalid RGB color.")
    return float_colors


def set_color(turtle: Turtle,
              colors: Optional[ColorList] = None) -> bool:
    """
    Set the color for the turtle graphics.
    Default to black.

    Args:
        turtle (Turtle): The Turtle instance to be used for drawing.
        colors (Optional[ColorList]): A tuple or list representing 
            color values.

    Raises:
        ValueError: Raised if the input is not a valid RGB color list or RGB
            color tuple.

    Returns:
        bool: Returns True if the color is successfully set with a fill color, 
            False if no fill color is set.
    """
    if not colors:
        turtle.color([0, 0, 0])
        return False
    if len(colors) != 2:
        raise ValueError("Invalid RGB color list or RGB color tuple.")
    color_type = get_color_type(colors)
    if "int" in color_type:
        colors = float_color(colors)
    if "list" in color_type and len(colors) == 2:
        turtle.color(colors[0], colors[1])
        return True
    if "list" not in color_type:
        turtle.color(colors)
        return False
    return False


def get_side_length(side: int, radius: Union[int, float],
                    radius_type: str) -> int:
    """
    Calculate the side length of a regular polygon given its radius.

    Args:
        side (int): The number of sides of the regular polygon.
        radius (Union[int, float]): The radius of the regular polygon.
        radius_type (str): The type of radius provided. It can be "r" 
            for circumradius, or "a" for apothem.

    Raises:
        ValueError: Raised if the radius type is invalid

    Returns:
        int: The side length of the regular polygon.
    """
    if radius_type.lower() == "r":
        return int(radius * sin(pi / side) * 2)
    if radius_type.lower() == "a":
        return int(radius * tan(pi / side) * 2)
    if radius_type.lower() not in ["r", "a"]:
        raise ValueError("Invalid radius type.")
    return radius


def polygon(turtle: Turtle, side: int, length: Union[int, float],
            color: OptionalColor = None,
            radius_type: Optional[str] = None) -> None:
    """
    This function draws a polygon with the specified number of sides, 
        side length, border color and optionally fill color.
    Using the porvided Turtle instance for drawing.
    Set whether to fill based on the provision of fill_color.
    If fill_color is provided, then fill.

    Args:
        turtle (Turtle): The Turtle instance to be used for drawing.
        side (int): The number of sides of the polygon. 
            If side is 0, a circle will be drawn.
        length (int): The side length or the radius of the polygon.
        color (Optional[RGB]): The border color of the polygon in RGB 
            format. Default to black.
        radius_type (str): The type of radius provided. It can be "r" 
            for circumradius, or "a" for apothem.
    
    Raises:
        TypeError:
            Raised if side number is not an integer or a float 
                point number.
            Raised if radius is not an integer or a float 
                point number.
        ValueError:
            Raised if side number is not greater than 3.
    """
    if radius_type:
        side_length = get_side_length(side, length, radius_type)
    else:
        side_length = int(length)
    if not color:
        color = []
    if not isinstance(side, int):
        raise TypeError("Number of sides must be an integer.")
    if side < 3:
        raise ValueError("Number of sides must be greater than 3.")
    if side_length <= 0:
        raise ValueError("Side length must be greater than 0.")
    fill_color = set_color(turtle, color)
    angle = 180 - (side - 2) * 180 / side
    if fill_color:
        turtle.begin_fill()
        for _ in range(side):
            turtle.forward(side_length)
            turtle.left(angle)
        turtle.end_fill()
    else:
        for _ in range(side):
            turtle.forward(side_length)
            turtle.left(angle)


def generate_gradient_colors(step: int, color_list: ColorList,
                             weights: Optional[list[float]] = None
                             ) -> ColorList:
    """
    Generates a list of gradient colors transitioning through
        specified colors at given weights.
    This function creates a gradient color list based on a list of
        input colors and corresponding weights.
    Each color in the output list is a tuple of three floats
        representing the red, green, and blue channels,
        with each channel value ranging from 0.0 to 1.0.
    The transition between colors is linear, based on the
        relative weights and the total number of steps specified.
    Args:
        step (int): The total number of gradient steps to generate.
        color_list (ColorList): A list of colors to include in the 
            gradient.
        weights (list[float]): A list of relative positions for each 
            color in the gradient, with values ranging from 0.0 to 1.0.
            Must be the same length as `color_list` and sorted in 
            ascending order.
    Returns:
        A list of tuples representing the gradient colors, with each
            color transitioning smoothly from the
            start to the end color based on the specified weights.
    Raises:
        ValueError:
            Raised if color_list and weights have different lengths.
            Raised if the list contains less than two colors.
            Raised if the weights are not sorted in ascending order.
    """
    if len(color_list) < 2:
        error = "At least two colors are required for a gradient."
        raise ValueError(error)
    if not weights:
        weights = [i / (len(color_list) - 1)
                   for i in range(len(color_list))]
    else:
        if len(color_list) != len(weights):
            error = "The length of color_list and \
weights must be the same."
            raise ValueError(error)
        if sorted(weights) != weights:
            error = "Weights must be sorted in ascending order."
            raise ValueError(error)
    gradient_colors = []
    proportional_steps = [round((weights[i + 1]
                                 - weights[i]) * (step - 1))
                                 for i in range(len(weights) - 1)]
    total_proportional_steps = sum(proportional_steps)
    while total_proportional_steps < step - 1:
        proportional_steps[-1] += 1
        total_proportional_steps += 1
    while total_proportional_steps > step - 1:
        proportional_steps[-1] -= 1
        total_proportional_steps -= 1
    current_index = 0
    for i in range(len(color_list) - 1):
        start_color = color_list[i]
        end_color = color_list[i + 1]
        steps_for_this_segment = proportional_steps[i]
        for s in range(steps_for_this_segment):
            if current_index >= step - 1:
                break
            interpolated_color = [
                start_color[j] + ((s / max(1, steps_for_this_segment))
                                  * (end_color[j] - start_color[j]))
                                  for j in range(3)]
            gradient_colors.append(interpolated_color)
            current_index += 1
    if len(gradient_colors) < step:
        gradient_colors.append(color_list[-1])
    return float_color(gradient_colors)
