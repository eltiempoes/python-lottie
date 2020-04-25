"""!
Package with all the Lottie Python bindings
"""
from . import (
    animation, base, effects, enums, helpers, layers, shapes, assets, easing,
    text, bezier, composition
)
from .animation import Animation
from .layers import *
from .shapes import *
from .assets import Precomp
from .bezier import Bezier
from .composition import Composition

__all__ = [
    "animation", "base", "effects", "enums", "helpers", "layers", "shapes", "assets"
    "easing", "text", "bezier",
    "Animation",
    "NullLayer", "TextLayer", "ShapeLayer", "ImageLayer", "PreCompLayer", "SolidLayer",
    "Rect", "Fill", "Trim", "Repeater", "GFill", "Stroke", "RoundedCorners", "Path",
    "TransformShape", "Group", "Star", "Ellipse", "Merge", "GStroke",
    "Bezier", "Precomp", "Composition",
]
