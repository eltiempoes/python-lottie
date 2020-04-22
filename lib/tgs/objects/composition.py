from .base import TgsObject, Index, TgsProp
from .layers import Layer


## \ingroup Lottie
class Composition(TgsObject):
    """!
    Base class for layer holders
    """
    _props = [
        TgsProp("layers", "layers", Layer, True),
    ]

    def __init__(self):
        ## List of Composition Layers
        self.layers = [] # ShapeLayer, SolidLayer, CompLayer, ImageLayer, NullLayer, TextLayer

        self._index_gen = Index()

    def layer(self, index):
        for layer in self.layers:
            if layer.index == index:
                return layer
        raise IndexError("No layer %s" % index)

    def add_layer(self, layer: Layer):
        """!
        @brief Appends a layer to the composition
        \see insert_layer
        """
        return self.insert_layer(len(self.layers), layer)

    def insert_layer(self, index, layer: Layer):
        """!
        @brief Inserts a layer to the composition
        @note Layers added first will be rendered on top of later layers
        """
        self.layers.insert(index, layer)
        self.prepare_layer(layer)
        return layer

    def prepare_layer(self, layer: Layer):
        layer.composition = self
        if layer.index is None:
            layer.index = next(self._index_gen)
        self._on_prepare_layer(layer)

    def _on_prepare_layer(self, layer):
        raise NotImplementedError

    def clone(self):
        c = super().clone()
        c._index_gen._i = self._index_gen._i
        return c
