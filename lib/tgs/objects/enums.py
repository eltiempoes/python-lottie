from .base import TgsEnum


class TestBased(TgsEnum):
    Characters = 1
    CharacterExcludingSpaces = 2
    Words = 3
    Lines = 4

    @classmethod
    def default(cls):
        return cls.Characters


class TextShape(TgsEnum):
    Square = 1
    RampUp = 2
    RampDown = 3
    Triangle = 4
    Round = 5
    Smooth = 6

    @classmethod
    def default(cls):
        return cls.Square


class TextGrouping(TgsEnum):
    Characters = 1
    Word = 2
    Line = 3
    All = 4

    @classmethod
    def default(cls):
        return cls.Characters


class BlendMode(TgsEnum):
    Normal = 0
    Multiply = 1
    Screen = 2
    Overlay = 3
    Darken = 4
    Lighten = 5
    ColorDodge = 6
    ColorBurn = 7
    HardLight = 8
    SoftLight = 9
    Difference = 10
    Exclusion = 11
    Hue = 12
    Saturation = 13
    Color = 14
    Luminosity = 15

    @classmethod
    def default(cls):
        return cls.Normal
