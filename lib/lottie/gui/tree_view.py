from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from .. import objects


def lottie_theme_icon(lottie_object):
    if isinstance(lottie_object, objects.Animation):
        return "tool-animator"

    if isinstance(lottie_object, objects.Precomp):
        return "folder"

    if isinstance(lottie_object, objects.ShapeLayer):
        return "shapes"
    if isinstance(lottie_object, objects.TextLayer):
        return "draw-text"
    if isinstance(lottie_object, objects.PreCompLayer):
        return "emblem-symbolic-link"

    if isinstance(lottie_object, (objects.Rect, objects.SolidColorLayer)):
        return "draw-rectangle"
    if isinstance(lottie_object, objects.Ellipse):
        return "draw-ellipse"
    if isinstance(lottie_object, objects.Star):
        return "draw-star"
    if isinstance(lottie_object, objects.Path):
        return "draw-bezier-curves"
    if isinstance(lottie_object, (objects.Fill, objects.GradientFill)):
        return "format-fill-color"
    if isinstance(lottie_object, (objects.Stroke, objects.GradientStroke)):
        return "format-stroke-color"
    if isinstance(lottie_object, objects.Transform):
        return "transform-scale"
    if isinstance(lottie_object, objects.Group):
        return "object-group"

    return None


def lottie_to_tree(tree_parent, lottie_object):
    prop_to_tree(tree_parent, None, lottie_object)


def lottie_object_to_tree(item, lottie_object, propname, textcol):
    if propname == "color" and isinstance(lottie_object, objects.MultiDimensional) and not lottie_object.animated:
        item.setBackground(textcol, QBrush(QColor.fromRgbF(*lottie_object.value)))
    else:
        text = str(lottie_object)
        if text != propname or textcol == 0:
            item.setText(textcol, text)

    icon = lottie_theme_icon(lottie_object)
    if icon:
        item.setIcon(0, QIcon.fromTheme(icon))

    for prop in lottie_object._props:
        propitem = prop_to_tree(item, prop.name, prop.get(lottie_object))
        propitem.setToolTip(0, prop.lottie)


def prop_to_tree(tree_parent, propname, propval):
    item = QtWidgets.QTreeWidgetItem(tree_parent)

    first_column = 0
    if propname:
        item.setText(0, propname)
        first_column = 1

    if isinstance(propval, objects.LottieObject):
        lottie_object_to_tree(item, propval, propname, first_column)
    elif isinstance(propval, list):
        for subval in propval:
            prop_to_tree(item, type(subval).__name__, subval)
    elif propval is None:
        item.setText(first_column, "")
    elif isinstance(propval, bool):
        item.setCheckState(first_column, Qt.CheckState.Checked if propval else Qt.CheckState.Unchecked)
        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
    else:
        item.setText(first_column, str(propval))

    return item
