from PySide2 import QtWidgets, QtGui

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
    item = QtWidgets.QTreeWidgetItem(tree_parent)
    item.setText(0, getattr(lottie_object, "name", "") or type(lottie_object).__name__)

    icon = lottie_theme_icon(lottie_object)
    if icon:
        item.setIcon(0, QtGui.QIcon.fromTheme(icon))

    if isinstance(lottie_object, objects.Composition):
        for layer in lottie_object.layers:
            lottie_to_tree(item, layer)
    if isinstance(lottie_object, objects.Animation):
        for layer in lottie_object.assets:
            lottie_to_tree(item, layer)
    if isinstance(lottie_object, objects.Layer):
        for layer in lottie_object.children:
            lottie_to_tree(item, layer)
    if isinstance(lottie_object, (objects.ShapeLayer, objects.Group)):
        for layer in lottie_object.shapes:
            lottie_to_tree(item, layer)
