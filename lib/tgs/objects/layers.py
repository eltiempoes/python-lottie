from .base import TgsObject, TgsProp, PseudoBool
from .effects import load_effect
from .helpers import Transform
from .shapes import load_shape
from .enums import BlendMode


def load_layer(lottiedict):
    layers = {
        0: PreCompLayer,
        1: SolidLayer,
        2: ImageLayer,
        3: NullLayer,
        4: ShapeLayer,
        5: TextLayer,
    }
    return layers[lottiedict["ty"]].load(lottiedict)


class NullLayer(TgsObject): # TODO check
    _props = [
        TgsProp("type", "ty", float, False),
        TgsProp("transform", "ks", Transform, False),
        TgsProp("auto_orient", "ao", PseudoBool, False),
        TgsProp("threedimensional", "ddd", PseudoBool, False),
        TgsProp("index", "ind", float, False),
        TgsProp("css_class", "cl", str, False),
        TgsProp("layer_html_id", "ln", str, False),
        TgsProp("in_point", "ip", float, False),
        TgsProp("out_point", "op", float, False),
        TgsProp("start_time", "st", float, False),
        TgsProp("name", "nm", str, False),
        TgsProp("effects", "ef", load_effect, True),
        TgsProp("stretch", "sr", float, False),
        TgsProp("parent", "parent", float, False),
    ]

    def __init__(self):
        # Type of layer: Null.
        self.type = 3
        # Transform properties
        self.transform = Transform()
        # Auto-Orient along path AE property.
        self.auto_orient = False
        # 3d layer flag
        self.threedimensional = False
        # Layer index in AE. Used for parenting and expressions.
        self.index = 0
        # Parsed layer name used as html class on SVG/HTML renderer
        self.css_class = ""
        # Parsed layer name used as html id on SVG/HTML renderer
        self.layer_html_id = ""
        # In Point of layer. Sets the initial frame of the layer.
        self.in_point = 0
        # Out Point of layer. Sets the final frame of the layer.
        self.out_point = 0
        # Start Time of layer. Sets the start time of the layer.
        self.start_time = 0
        # After Effects Layer Name. Used for expressions.
        self.name = None
        # List of Effects
        self.effects = [] # IndexEffect
        # Layer Time Stretching
        self.stretch = 0
        # Layer Parent. Uses ind of parent.
        self.parent = None


class TextLayer(TgsObject): # TODO check
    _props = [
        TgsProp("type", "ty", float, False),
        TgsProp("transform", "ks", Transform, False),
        TgsProp("auto_orient", "ao", PseudoBool, False),
        TgsProp("blend_mode", "bm", float, False),
        TgsProp("threedimensional", "ddd", PseudoBool, False),
        TgsProp("index", "ind", float, False),
        TgsProp("css_class", "cl", str, False),
        TgsProp("layer_html_id", "ln", str, False),
        TgsProp("in_point", "ip", float, False),
        TgsProp("out_point", "op", float, False),
        TgsProp("start_time", "st", float, False),
        TgsProp("name", "nm", float, False),
        #TgsProp("has_masks", "hasMask", float, False),
        #TgsProp("masks_properties", "masksProperties", Mask, True),
        TgsProp("effects", "ef", PseudoBool, False),
        TgsProp("stretch", "sr", float, False),
        TgsProp("parent", "parent", float, False),
        TgsProp("text_data", "t", float, False),
    ]

    def __init__(self):
        # Type of layer: Text.
        self.type = 0
        # Transform properties
        self.transform = Transform()
        # Auto-Orient along path AE property.
        self.auto_orient = False
        # Blend Mode
        self.blend_mode = BlendMode.default()
        # 3d layer flag
        self.threedimensional = False
        # Layer index in AE. Used for parenting and expressions.
        self.index = 0
        # Parsed layer name used as html class on SVG/HTML renderer
        self.css_class = ""
        # Parsed layer name used as html id on SVG/HTML renderer
        self.layer_html_id = ""
        # In Point of layer. Sets the initial frame of the layer.
        self.in_point = 0
        # Out Point of layer. Sets the final frame of the layer.
        self.out_point = 0
        # Start Time of layer. Sets the start time of the layer.
        self.start_time = 0
        # After Effects Layer Name. Used for expressions.
        self.name = 0
        # Boolean when layer has a mask. Will be deprecated in favor of checking masksProperties.
        self.has_masks = 0
        # List of Masks
        self.masks_properties = [] # Mask
        # Auto-Orient along path AE property.
        self.effects = False
        # Layer Time Stretching
        self.stretch = 0
        # Layer Parent. Uses ind of parent.
        self.parent = None
        # Text Data
        self.text_data = None


class ShapeLayer(TgsObject):
    _props = [
        TgsProp("type", "ty", float, False),
        TgsProp("transform", "ks", Transform, False),
        TgsProp("auto_orient", "ao", PseudoBool, False),
        TgsProp("blend_mode", "bm", float, False),
        TgsProp("threedimensional", "ddd", PseudoBool, False),
        TgsProp("index", "ind", float, False),
        #TgsProp("css_class", "cl", str, False),
        #TgsProp("layer_html_id", "ln", str, False),
        TgsProp("in_point", "ip", float, False),
        TgsProp("out_point", "op", float, False),
        TgsProp("start_time", "st", float, False),
        TgsProp("name", "nm", str, False),
        #TgsProp("has_masks", "hasMask", float, False),
        #TgsProp("masks_properties", "masksProperties", Mask, True),
        TgsProp("effects", "ef", load_effect, True),
        TgsProp("stretch", "sr", float, False),
        TgsProp("parent", "parent", float, False),
        TgsProp("shapes", "shapes", load_shape, True),
    ]

    def __init__(self):
        # Type of layer: Shape.
        self.type = 4
        # Transform properties
        self.transform = Transform()
        # Auto-Orient along path AE property.
        self.auto_orient = False
        # Blend Mode
        self.blend_mode = BlendMode.default()
        # 3d layer flag
        self.threedimensional = False
        # Layer index in AE. Used for parenting and expressions.
        self.index = None
        ## Parsed layer name used as html class on SVG/HTML renderer
        #self.css_class = ""
        ## Parsed layer name used as html id on SVG/HTML renderer
        #self.layer_html_id = ""
        # In Point of layer. Sets the initial frame of the layer.
        self.in_point = None
        # Out Point of layer. Sets the final frame of the layer.
        self.out_point = None
        # Start Time of layer. Sets the start time of the layer.
        self.start_time = 0
        # After Effects Layer Name. Used for expressions.
        self.name = None
        # Boolean when layer has a mask. Will be deprecated in favor of checking masksProperties.
        self.has_masks = 0
        # List of Masks
        self.masks_properties = [] # Mask
        # List of Effects
        self.effects = None # IndexEffect
        # Layer Time Stretching
        self.stretch = 1
        # Layer Parent. Uses ind of parent.
        self.parent = None
        # Shape list of items
        self.shapes = [] # Shape, Rect, Ellipse, Star, Fill, GFill, GStroke, Stroke, Merge, Trim, Group, RoundedCorners, Repeater

    def add_shape(self, shape):
            self.shapes.append(shape)
            return shape

class ImageLayer(TgsObject): # TODO check
    _props = [
        TgsProp("type", "ty", float, False),
        TgsProp("transform", "ks", Transform, False),
        TgsProp("auto_orient", "ao", PseudoBool, False),
        TgsProp("blend_mode", "bm", float, False),
        TgsProp("threedimensional", "ddd", PseudoBool, False),
        TgsProp("index", "ind", float, False),
        TgsProp("css_class", "cl", str, False),
        TgsProp("layer_html_id", "ln", str, False),
        TgsProp("in_point", "ip", float, False),
        TgsProp("out_point", "op", float, False),
        TgsProp("start_time", "st", float, False),
        TgsProp("name", "nm", float, False),
        #TgsProp("has_masks", "hasMask", float, False),
        #TgsProp("masks_properties", "masksProperties", Mask, True),
        TgsProp("effects", "ef", load_effect, True),
        TgsProp("stretch", "sr", float, False),
        TgsProp("parent", "parent", float, False),
        TgsProp("reference_id", "refId", str, False),
    ]

    def __init__(self):
        # Type of layer: Image.
        self.type = 2
        # Transform properties
        self.transform = Transform()
        # Auto-Orient along path AE property.
        self.auto_orient = False
        # Blend Mode
        self.blend_mode = BlendMode.default()
        # 3d layer flag
        self.threedimensional = False
        # Layer index in AE. Used for parenting and expressions.
        self.index = 0
        # Parsed layer name used as html class on SVG/HTML renderer
        self.css_class = ""
        # Parsed layer name used as html id on SVG/HTML renderer
        self.layer_html_id = ""
        # In Point of layer. Sets the initial frame of the layer.
        self.in_point = 0
        # Out Point of layer. Sets the final frame of the layer.
        self.out_point = 0
        # Start Time of layer. Sets the start time of the layer.
        self.start_time = 0
        # After Effects Layer Name. Used for expressions.
        self.name = 0
        # Boolean when layer has a mask. Will be deprecated in favor of checking masksProperties.
        self.has_masks = 0
        # List of Masks
        self.masks_properties = [] # Mask
        # List of Effects
        self.effects = [] # IndexEffect
        # Layer Time Stretching
        self.stretch = 0
        # Layer Parent. Uses ind of parent.
        self.parent = None
        # id pointing to the source image defined on 'assets' object
        self.reference_id = ""


class PreCompLayer(TgsObject): # TODO check
    _props = [
        TgsProp("type", "ty", float, False),
        TgsProp("transform", "ks", Transform, False),
        TgsProp("auto_orient", "ao", PseudoBool, False),
        TgsProp("blend_mode", "bm", float, False),
        TgsProp("threedimensional", "ddd", PseudoBool, False),
        TgsProp("index", "ind", float, False),
        TgsProp("css_class", "cl", str, False),
        TgsProp("layer_html_id", "ln", str, False),
        TgsProp("in_point", "ip", float, False),
        TgsProp("out_point", "op", float, False),
        TgsProp("start_time", "st", float, False),
        TgsProp("name", "nm", float, False),
        #TgsProp("has_masks", "hasMask", float, False),
        #TgsProp("masks_properties", "masksProperties", Mask, True),
        TgsProp("effects", "ef", load_effect, True),
        TgsProp("stretch", "sr", float, False),
        TgsProp("parent", "parent", float, False),
        TgsProp("reference_id", "refId", str, False),
        TgsProp("time_remapping", "tm", float, False),
    ]

    def __init__(self):
        # Type of layer: Precomp.
        self.type = 0
        # Transform properties
        self.transform = Transform()
        # Auto-Orient along path AE property.
        self.auto_orient = False
        # Blend Mode
        self.blend_mode = BlendMode.default()
        # 3d layer flag
        self.threedimensional = False
        # Layer index in AE. Used for parenting and expressions.
        self.index = 0
        # Parsed layer name used as html class on SVG/HTML renderer
        self.css_class = ""
        # Parsed layer name used as html id on SVG/HTML renderer
        self.layer_html_id = ""
        # In Point of layer. Sets the initial frame of the layer.
        self.in_point = 0
        # Out Point of layer. Sets the final frame of the layer.
        self.out_point = 0
        # Start Time of layer. Sets the start time of the layer.
        self.start_time = 0
        # After Effects Layer Name. Used for expressions.
        self.name = 0
        # Boolean when layer has a mask. Will be deprecated in favor of checking masksProperties.
        self.has_masks = 0
        # List of Masks
        self.masks_properties = [] # Mask
        # List of Effects
        self.effects = [] # IndexEffect
        # Layer Time Stretching
        self.stretch = 0
        # Layer Parent. Uses ind of parent.
        self.parent = None
        # id pointing to the source composition defined on 'assets' object
        self.reference_id = ""
        # Comp's Time remapping
        self.time_remapping = Value()


class SolidLayer(TgsObject): # TODO check
    _props = [
        TgsProp("type", "ty", float, False),
        TgsProp("transform", "ks", Transform, False),
        TgsProp("auto_orient", "ao", PseudoBool, False),
        TgsProp("blend_mode", "bm", float, False),
        TgsProp("threedimensional", "ddd", PseudoBool, False),
        TgsProp("index", "ind", float, False),
        TgsProp("css_class", "cl", str, False),
        TgsProp("layer_html_id", "ln", str, False),
        TgsProp("in_point", "ip", float, False),
        TgsProp("out_point", "op", float, False),
        TgsProp("start_time", "st", float, False),
        TgsProp("name", "nm", float, False),
        #TgsProp("has_masks", "hasMask", float, False),
        #TgsProp("masks_properties", "masksProperties", Mask, True),
        TgsProp("effects", "ef", PseudoBool, False),
        TgsProp("stretch", "sr", float, False),
        TgsProp("parent", "parent", float, False),
        TgsProp("solid_color", "sc", str, False),
        TgsProp("solid_height", "sh", float, False),
        TgsProp("solid_width", "sw", float, False),
    ]

    def __init__(self):
        # Type of layer: Solid.
        self.type = 0
        # Transform properties
        self.transform = Transform()
        # Auto-Orient along path AE property.
        self.auto_orient = False
        # Blend Mode
        self.blend_mode = BlendMode.default()
        # 3d layer flag
        self.threedimensional = False
        # Layer index in AE. Used for parenting and expressions.
        self.index = 0
        # Parsed layer name used as html class on SVG/HTML renderer
        self.css_class = ""
        # Parsed layer name used as html id on SVG/HTML renderer
        self.layer_html_id = ""
        # In Point of layer. Sets the initial frame of the layer.
        self.in_point = 0
        # Out Point of layer. Sets the final frame of the layer.
        self.out_point = 0
        # Start Time of layer. Sets the start time of the layer.
        self.start_time = 0
        # After Effects Layer Name. Used for expressions.
        self.name = 0
        # Boolean when layer has a mask. Will be deprecated in favor of checking masksProperties.
        self.has_masks = 0
        # List of Masks
        self.masks_properties = [] # Mask
        # Auto-Orient along path AE property.
        self.effects = False
        # Layer Time Stretching
        self.stretch = 0
        # Layer Parent. Uses ind of parent.
        self.parent = None
        # Color of the solid in hex
        self.solid_color = ""
        # Height of the solid.
        self.solid_height = 0
        # Width of the solid.
        self.solid_width = 0
