animation
=========

Animation
---------

### fr

 * Description: frame rate
 * Type: float

### ddd

 * Description: threedimensional
 * Type: bool but displayed as int

### h

 * Description: height
 * Type: int

### v

 * Description: version
 * Type: str

### ip

 * Description: in point
 * Type: float

### nm

 * Description: name
 * Type: str

### op

 * Description: out point
 * Type: float

### layers

 * Description: layers
 * Type: list of layer

### assets

 * Description: assets
 * Type: list of todo_func

### tgs

 * Description: tgs
 * Type: bool but displayed as int

### w

 * Description: width
 * Type: int



effects
=======

AngleEffect
-----------

### ix

 * Description: effect index
 * Type: float

### mn

 * Description: match name
 * Type: str

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: float

### v

 * Description: value
 * Type: Value



CheckBoxEffect
--------------

### ix

 * Description: effect index
 * Type: float

### mn

 * Description: match name
 * Type: str

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: float

### v

 * Description: value
 * Type: Value



ColorEffect
-----------

### ix

 * Description: effect index
 * Type: float

### mn

 * Description: match name
 * Type: str

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: float

### v

 * Description: value
 * Type: MultiDimensional



DropDownEffect
--------------

### ix

 * Description: effect index
 * Type: float

### mn

 * Description: match name
 * Type: str

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: float

### v

 * Description: value
 * Type: Value



FillEffect
----------

### ix

 * Description: effect index
 * Type: float

### mn

 * Description: match name
 * Type: str

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: float

### ef

 * Description: effects
 * Type: list of todo_func



GroupEffect
-----------

### ix

 * Description: effect index
 * Type: float

### mn

 * Description: match name
 * Type: str

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: float

### ef

 * Description: effects
 * Type: list of todo_func

### en

 * Description: enabled
 * Type: float



LayerEffect
-----------

### ix

 * Description: effect index
 * Type: float

### mn

 * Description: match name
 * Type: str

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: float

### v

 * Description: value
 * Type: Value



MultiDimensional
----------------

### k

 * Description: value
 * Type: list of float

### ix

 * Description: property index
 * Type: int

### a

 * Description: animated
 * Type: bool but displayed as int

### k

 * Description: keyframes
 * Type: list of OffsetKeyframe



PointEffect
-----------

### ix

 * Description: effect index
 * Type: float

### mn

 * Description: match name
 * Type: str

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: float

### v

 * Description: value
 * Type: list of MultiDimensional



ProLevelsEffect
---------------

### ix

 * Description: effect index
 * Type: float

### mn

 * Description: match name
 * Type: str

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: float

### ef

 * Description: effects
 * Type: list of todo_func



SliderEffect
------------

### ix

 * Description: effect index
 * Type: float

### mn

 * Description: match name
 * Type: str

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: float

### v

 * Description: value
 * Type: Value



StrokeEffect
------------

### ix

 * Description: effect index
 * Type: float

### mn

 * Description: match name
 * Type: str

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: float

### ef

 * Description: effects
 * Type: list of todo_func



TintEffect
----------

### ix

 * Description: effect index
 * Type: float

### mn

 * Description: match name
 * Type: str

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: float

### ef

 * Description: effects
 * Type: list of todo_func



TritoneEffect
-------------

### ix

 * Description: effect index
 * Type: float

### mn

 * Description: match name
 * Type: str

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: float

### ef

 * Description: effects
 * Type: list of todo_func



Value
-----

### k

 * Description: value
 * Type: float

### ix

 * Description: property index
 * Type: int

### a

 * Description: animated
 * Type: bool but displayed as int

### k

 * Description: keyframes
 * Type: list of OffsetKeyframe



enums
=====

BlendMode
---------

 * 0 = Normal
 * 1 = Multiply
 * 2 = Screen
 * 3 = Overlay
 * 4 = Darken
 * 5 = Lighten
 * 6 = ColorDodge
 * 7 = ColorBurn
 * 8 = HardLight
 * 9 = SoftLight
 * 10 = Difference
 * 11 = Exclusion
 * 12 = Hue
 * 13 = Saturation
 * 14 = Color
 * 15 = Luminosity


TestBased
---------

 * 1 = Characters
 * 2 = CharacterExcludingSpaces
 * 3 = Words
 * 4 = Lines


TextGrouping
------------

 * 1 = Characters
 * 2 = Word
 * 3 = Line
 * 4 = All


TextShape
---------

 * 1 = Square
 * 2 = RampUp
 * 3 = RampDown
 * 4 = Triangle
 * 5 = Round
 * 6 = Smooth


helpers
=======

Mask
----

### inv

 * Description: inverted
 * Type: float

### nm

 * Description: name
 * Type: str

### pt

 * Description: points
 * Type: todo_func

### o

 * Description: opacity
 * Type: todo_func

### mode

 * Description: mode
 * Type: str



MultiDimensional
----------------

### k

 * Description: value
 * Type: list of float

### ix

 * Description: property index
 * Type: int

### a

 * Description: animated
 * Type: bool but displayed as int

### k

 * Description: keyframes
 * Type: list of OffsetKeyframe



Transform
---------

### a

 * Description: anchor point
 * Type: MultiDimensional

### p

 * Description: position
 * Type: MultiDimensional

### s

 * Description: scale
 * Type: MultiDimensional

### r

 * Description: rotation
 * Type: Value

### o

 * Description: opacity
 * Type: Value

### sk

 * Description: skew
 * Type: Value

### sa

 * Description: skew axis
 * Type: Value



Value
-----

### k

 * Description: value
 * Type: float

### ix

 * Description: property index
 * Type: int

### a

 * Description: animated
 * Type: bool but displayed as int

### k

 * Description: keyframes
 * Type: list of OffsetKeyframe



layers
======

BlendMode
---------

 * 0 = Normal
 * 1 = Multiply
 * 2 = Screen
 * 3 = Overlay
 * 4 = Darken
 * 5 = Lighten
 * 6 = ColorDodge
 * 7 = ColorBurn
 * 8 = HardLight
 * 9 = SoftLight
 * 10 = Difference
 * 11 = Exclusion
 * 12 = Hue
 * 13 = Saturation
 * 14 = Color
 * 15 = Luminosity


ImageLayer
----------

### ty

 * Description: type
 * Type: float

### ks

 * Description: transform
 * Type: Transform

### ao

 * Description: auto orient
 * Type: bool but displayed as int

### bm

 * Description: blend mode
 * Type: float

### ddd

 * Description: threedimensional
 * Type: bool but displayed as int

### ind

 * Description: index
 * Type: int

### cl

 * Description: css class
 * Type: str

### ln

 * Description: layer html id
 * Type: str

### ip

 * Description: in point
 * Type: float

### op

 * Description: out point
 * Type: float

### st

 * Description: start time
 * Type: float

### nm

 * Description: name
 * Type: float

### ef

 * Description: effects
 * Type: list of todo_func

### sr

 * Description: stretch
 * Type: float

### parent

 * Description: parent
 * Type: int

### refId

 * Description: reference id
 * Type: str



NullLayer
---------

### ty

 * Description: type
 * Type: float

### ks

 * Description: transform
 * Type: Transform

### ao

 * Description: auto orient
 * Type: bool but displayed as int

### ddd

 * Description: threedimensional
 * Type: bool but displayed as int

### ind

 * Description: index
 * Type: int

### cl

 * Description: css class
 * Type: str

### ln

 * Description: layer html id
 * Type: str

### ip

 * Description: in point
 * Type: float

### op

 * Description: out point
 * Type: float

### st

 * Description: start time
 * Type: float

### nm

 * Description: name
 * Type: str

### ef

 * Description: effects
 * Type: list of todo_func

### sr

 * Description: stretch
 * Type: float

### parent

 * Description: parent
 * Type: int



PreCompLayer
------------

### ty

 * Description: type
 * Type: float

### ks

 * Description: transform
 * Type: Transform

### ao

 * Description: auto orient
 * Type: bool but displayed as int

### bm

 * Description: blend mode
 * Type: float

### ddd

 * Description: threedimensional
 * Type: bool but displayed as int

### ind

 * Description: index
 * Type: int

### cl

 * Description: css class
 * Type: str

### ln

 * Description: layer html id
 * Type: str

### ip

 * Description: in point
 * Type: float

### op

 * Description: out point
 * Type: float

### st

 * Description: start time
 * Type: float

### nm

 * Description: name
 * Type: float

### ef

 * Description: effects
 * Type: list of todo_func

### sr

 * Description: stretch
 * Type: float

### parent

 * Description: parent
 * Type: int

### refId

 * Description: reference id
 * Type: str

### tm

 * Description: time remapping
 * Type: float



ShapeLayer
----------

### ty

 * Description: type
 * Type: float

### ks

 * Description: transform
 * Type: Transform

### ao

 * Description: auto orient
 * Type: bool but displayed as int

### bm

 * Description: blend mode
 * Type: float

### ddd

 * Description: threedimensional
 * Type: bool but displayed as int

### ind

 * Description: index
 * Type: int

### ip

 * Description: in point
 * Type: float

### op

 * Description: out point
 * Type: float

### st

 * Description: start time
 * Type: float

### nm

 * Description: name
 * Type: str

### ef

 * Description: effects
 * Type: list of todo_func

### sr

 * Description: stretch
 * Type: float

### parent

 * Description: parent
 * Type: int

### shapes

 * Description: shapes
 * Type: list of shape



SolidLayer
----------

### ty

 * Description: type
 * Type: float

### ks

 * Description: transform
 * Type: Transform

### ao

 * Description: auto orient
 * Type: bool but displayed as int

### bm

 * Description: blend mode
 * Type: float

### ddd

 * Description: threedimensional
 * Type: bool but displayed as int

### ind

 * Description: index
 * Type: int

### cl

 * Description: css class
 * Type: str

### ln

 * Description: layer html id
 * Type: str

### ip

 * Description: in point
 * Type: float

### op

 * Description: out point
 * Type: float

### st

 * Description: start time
 * Type: float

### nm

 * Description: name
 * Type: float

### ef

 * Description: effects
 * Type: bool but displayed as int

### sr

 * Description: stretch
 * Type: float

### parent

 * Description: parent
 * Type: int

### sc

 * Description: solid color
 * Type: str

### sh

 * Description: solid height
 * Type: float

### sw

 * Description: solid width
 * Type: float



TextLayer
---------

### ty

 * Description: type
 * Type: float

### ks

 * Description: transform
 * Type: Transform

### ao

 * Description: auto orient
 * Type: bool but displayed as int

### bm

 * Description: blend mode
 * Type: float

### ddd

 * Description: threedimensional
 * Type: bool but displayed as int

### ind

 * Description: index
 * Type: int

### cl

 * Description: css class
 * Type: str

### ln

 * Description: layer html id
 * Type: str

### ip

 * Description: in point
 * Type: float

### op

 * Description: out point
 * Type: float

### st

 * Description: start time
 * Type: float

### nm

 * Description: name
 * Type: float

### ef

 * Description: effects
 * Type: bool but displayed as int

### sr

 * Description: stretch
 * Type: float

### parent

 * Description: parent
 * Type: int

### t

 * Description: text data
 * Type: float



Transform
---------

### a

 * Description: anchor point
 * Type: MultiDimensional

### p

 * Description: position
 * Type: MultiDimensional

### s

 * Description: scale
 * Type: MultiDimensional

### r

 * Description: rotation
 * Type: Value

### o

 * Description: opacity
 * Type: Value

### sk

 * Description: skew
 * Type: Value

### sa

 * Description: skew axis
 * Type: Value



properties
==========

Bezier
------

### c

 * Description: closed
 * Type: bool

### i

 * Description: in point
 * Type: list of list

### o

 * Description: out point
 * Type: list of list

### v

 * Description: vertices
 * Type: list of list



GradientColors
--------------

### k

 * Description: colors
 * Type: MultiDimensional

### p

 * Description: count
 * Type: int



KeyframeBezierPoint
-------------------

### x

 * Description: time
 * Type: %s or list of %s

### y

 * Description: value
 * Type: %s or list of %s



MultiDimensional
----------------

### k

 * Description: value
 * Type: list of float

### ix

 * Description: property index
 * Type: int

### a

 * Description: animated
 * Type: bool but displayed as int

### k

 * Description: keyframes
 * Type: list of OffsetKeyframe



OffsetKeyframe
--------------

### t

 * Description: time
 * Type: float

### i

 * Description: in value
 * Type: KeyframeBezierPoint

### o

 * Description: out value
 * Type: KeyframeBezierPoint

### ti

 * Description: in tan
 * Type: list of float

### to

 * Description: out tan
 * Type: list of float

### s

 * Description: start
 * Type: list of float

### e

 * Description: end
 * Type: list of float



ShapePropKeyframe
-----------------

### s

 * Description: start
 * Type: %s or list of %s

### e

 * Description: end
 * Type: %s or list of %s

### t

 * Description: time
 * Type: float

### i

 * Description: in value
 * Type: KeyframeBezierPoint

### o

 * Description: out value
 * Type: KeyframeBezierPoint



ShapeProperty
-------------

### k

 * Description: value
 * Type: Bezier

### ix

 * Description: property index
 * Type: float

### a

 * Description: animated
 * Type: bool but displayed as int

### k

 * Description: keyframes
 * Type: list of ShapePropKeyframe



Value
-----

### k

 * Description: value
 * Type: float

### ix

 * Description: property index
 * Type: int

### a

 * Description: animated
 * Type: bool but displayed as int

### k

 * Description: keyframes
 * Type: list of OffsetKeyframe



shapes
======

Composite
---------

 * 1 = Above
 * 2 = Below


Ellipse
-------

### nm

 * Description: name
 * Type: str

### d

 * Description: direction
 * Type: float

### ty

 * Description: type
 * Type: str

### p

 * Description: position
 * Type: MultiDimensional

### s

 * Description: size
 * Type: MultiDimensional



Fill
----

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: str

### o

 * Description: opacity
 * Type: Value

### c

 * Description: color
 * Type: MultiDimensional



GradientColors
--------------

### k

 * Description: colors
 * Type: MultiDimensional

### p

 * Description: count
 * Type: int



GradientFill
------------

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: str

### o

 * Description: opacity
 * Type: Value

### s

 * Description: start point
 * Type: MultiDimensional

### e

 * Description: end point
 * Type: MultiDimensional

### t

 * Description: gradient type
 * Type: GradientType

### h

 * Description: highlight length
 * Type: Value

### a

 * Description: highlight angle
 * Type: Value

### g

 * Description: colors
 * Type: GradientColors



GradientStroke
--------------

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: str

### o

 * Description: opacity
 * Type: Value

### s

 * Description: start point
 * Type: MultiDimensional

### e

 * Description: end point
 * Type: MultiDimensional

### t

 * Description: gradient type
 * Type: GradientType

### h

 * Description: highlight length
 * Type: Value

### a

 * Description: highlight angle
 * Type: Value

### g

 * Description: colors
 * Type: GradientColors

### w

 * Description: width
 * Type: Value

### lc

 * Description: line cap
 * Type: LineCap

### lj

 * Description: line join
 * Type: LineJoin

### ml

 * Description: miter limit
 * Type: float



GradientType
------------

 * 1 = Linear
 * 2 = Radial


Group
-----

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: str

### np

 * Description: number of properties
 * Type: float

### it

 * Description: shapes
 * Type: list of shape

### ix

 * Description: property index
 * Type: int



LineCap
-------

 * 1 = Butt
 * 2 = Round
 * 3 = Square


LineJoin
--------

 * 1 = Miter
 * 2 = Round
 * 3 = Bevel


Merge
-----

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: str

### mm

 * Description: merge mode
 * Type: float



MultiDimensional
----------------

### k

 * Description: value
 * Type: list of float

### ix

 * Description: property index
 * Type: int

### a

 * Description: animated
 * Type: bool but displayed as int

### k

 * Description: keyframes
 * Type: list of OffsetKeyframe



Rect
----

### nm

 * Description: name
 * Type: str

### d

 * Description: direction
 * Type: float

### ty

 * Description: type
 * Type: str

### p

 * Description: position
 * Type: MultiDimensional

### s

 * Description: size
 * Type: MultiDimensional

### r

 * Description: rounded
 * Type: Value



Repeater
--------

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: str

### c

 * Description: copies
 * Type: Value

### o

 * Description: offset
 * Type: Value

### m

 * Description: composite
 * Type: Composite

### tr

 * Description: transform
 * Type: Transform



Round
-----

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: str

### r

 * Description: radius
 * Type: Value



Shape
-----

### nm

 * Description: name
 * Type: str

### d

 * Description: direction
 * Type: float

### ty

 * Description: type
 * Type: str

### ks

 * Description: vertices
 * Type: ShapeProperty



ShapeProperty
-------------

### k

 * Description: value
 * Type: Bezier

### ix

 * Description: property index
 * Type: float

### a

 * Description: animated
 * Type: bool but displayed as int

### k

 * Description: keyframes
 * Type: list of ShapePropKeyframe



Star
----

### nm

 * Description: name
 * Type: str

### d

 * Description: direction
 * Type: float

### ty

 * Description: type
 * Type: str

### p

 * Description: position
 * Type: MultiDimensional

### ir

 * Description: inner radius
 * Type: Value

### is

 * Description: inner roundness
 * Type: Value

### or

 * Description: outer radius
 * Type: Value

### os

 * Description: outer roundness
 * Type: Value

### r

 * Description: rotation
 * Type: Value

### pt

 * Description: points
 * Type: Value

### sy

 * Description: star type
 * Type: StarType



StarType
--------

 * 1 = Star
 * 2 = Polygon


Stroke
------

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: str

### lc

 * Description: line cap
 * Type: LineCap

### lj

 * Description: line join
 * Type: LineJoin

### ml

 * Description: miter limit
 * Type: float

### o

 * Description: opacity
 * Type: Value

### w

 * Description: width
 * Type: Value

### c

 * Description: color
 * Type: MultiDimensional



Transform
---------

### a

 * Description: anchor point
 * Type: MultiDimensional

### p

 * Description: position
 * Type: MultiDimensional

### s

 * Description: scale
 * Type: MultiDimensional

### r

 * Description: rotation
 * Type: Value

### o

 * Description: opacity
 * Type: Value

### sk

 * Description: skew
 * Type: Value

### sa

 * Description: skew axis
 * Type: Value



TransformShape
--------------

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: str

### a

 * Description: anchor point
 * Type: MultiDimensional

### p

 * Description: position
 * Type: MultiDimensional

### s

 * Description: scale
 * Type: MultiDimensional

### r

 * Description: rotation
 * Type: Value

### o

 * Description: opacity
 * Type: Value

### sk

 * Description: skew
 * Type: Value

### sa

 * Description: skew axis
 * Type: Value



Trim
----

### nm

 * Description: name
 * Type: str

### ty

 * Description: type
 * Type: str

### s

 * Description: start
 * Type: Value

### e

 * Description: end
 * Type: Value

### o

 * Description: offset
 * Type: Value



Value
-----

### k

 * Description: value
 * Type: float

### ix

 * Description: property index
 * Type: int

### a

 * Description: animated
 * Type: bool but displayed as int

### k

 * Description: keyframes
 * Type: list of OffsetKeyframe



sources
=======

Chars
-----

### ch

 * Description: character
 * Type: str

### fFamily

 * Description: font family
 * Type: str

### size

 * Description: font size
 * Type: str

### style

 * Description: font style
 * Type: str

### w

 * Description: width
 * Type: float

### data

 * Description: character data
 * Type: float



Image
-----

### h

 * Description: height
 * Type: float

### w

 * Description: width
 * Type: float

### id

 * Description: id
 * Type: str

### p

 * Description: image name
 * Type: str

### u

 * Description: image path
 * Type: str



Precomp
-------

### id

 * Description: id
 * Type: str

### layers

 * Description: layers
 * Type: list of todo_func



