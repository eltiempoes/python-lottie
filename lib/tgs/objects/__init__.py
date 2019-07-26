"""!
Package with all the Lottie Python bindings
"""
from . import animation, base, effects, enums, helpers, layers, shapes, assets, easing
from .animation import Animation
from .layers import *
from .shapes import *
from .properties import Bezier

__all__ = [
    "animation", "base", "effects", "enums", "helpers", "layers", "shapes", "assets"
    "easing",
    "Animation",
    "NullLayer", "TextLayer", "ShapeLayer", "ImageLayer", "PreCompLayer", "SolidLayer",
    "Rect", "Fill", "Trim", "Repeater", "GFill", "Stroke", "Round", "Path",
    "TransformShape", "Group", "Star", "Ellipse", "Merge", "GStroke",
    "Bezier",
]
