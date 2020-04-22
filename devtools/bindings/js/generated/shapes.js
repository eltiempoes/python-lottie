import { value_to_lottie, value_from_lottie, LottieObject } from '../base.js';
import { ShapeProperty, Value, MultiDimensional, GradientColors } from './properties.js';
import { Transform } from './helpers.js';

/*An enumeration.
*/
export const Composite = Object.freeze({
    Above: 1,
    Below: 2,
});
/*An enumeration.
*/
export const GradientType = Object.freeze({
    Linear: 1,
    Radial: 2,
});
/*An enumeration.
*/
export const LineCap = Object.freeze({
    Butt: 1,
    Round: 2,
    Square: 3,
});
/*An enumeration.
*/
export const LineJoin = Object.freeze({
    Miter: 1,
    Round: 2,
    Bevel: 3,
});
/*
*/
export class RepeaterTransform extends Transform
{
    anchor_point;
    position;
    scale;
    rotation;
    opacity;
    skew;
    skew_axis;
    start_opacity;
    end_opacity;

    constructor()
    {
        super();
        this.anchor_point = new MultiDimensional([0, 0]);
        this.position = new MultiDimensional([0, 0]);
        this.scale = new MultiDimensional([100, 100]);
        this.rotation = new Value(0);
        this.opacity = new Value(100);
        this.skew = new Value(0);
        this.skew_axis = new Value(0);
        this.start_opacity = new Value(100);
        this.end_opacity = new Value(100);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.anchor_point !== null )
            arr["a"] = value_to_lottie(this.anchor_point);
        if ( this.position !== null )
            arr["p"] = value_to_lottie(this.position);
        if ( this.scale !== null )
            arr["s"] = value_to_lottie(this.scale);
        if ( this.rotation !== null )
            arr["r"] = value_to_lottie(this.rotation);
        if ( this.opacity !== null )
            arr["o"] = value_to_lottie(this.opacity);
        if ( this.skew !== null )
            arr["sk"] = value_to_lottie(this.skew);
        if ( this.skew_axis !== null )
            arr["sa"] = value_to_lottie(this.skew_axis);
        if ( this.start_opacity !== null )
            arr["so"] = value_to_lottie(this.start_opacity);
        if ( this.end_opacity !== null )
            arr["eo"] = value_to_lottie(this.end_opacity);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new RepeaterTransform();
        if ( arr["a"] !== undefined )
            obj.anchor_point = value_from_lottie(arr["a"]);
        if ( arr["p"] !== undefined )
            obj.position = value_from_lottie(arr["p"]);
        if ( arr["s"] !== undefined )
            obj.scale = value_from_lottie(arr["s"]);
        if ( arr["r"] !== undefined )
            obj.rotation = value_from_lottie(arr["r"]);
        if ( arr["o"] !== undefined )
            obj.opacity = value_from_lottie(arr["o"]);
        if ( arr["sk"] !== undefined )
            obj.skew = value_from_lottie(arr["sk"]);
        if ( arr["sa"] !== undefined )
            obj.skew_axis = value_from_lottie(arr["sa"]);
        if ( arr["so"] !== undefined )
            obj.start_opacity = value_from_lottie(arr["so"]);
        if ( arr["eo"] !== undefined )
            obj.end_opacity = value_from_lottie(arr["eo"]);
        return obj;
    }
}

/*!
    Base class for all elements of ShapeLayer and Group
*/
export class ShapeElement extends LottieObject
{
    hidden;
    name;
    type;
    property_index;
    bm;

    constructor()
    {
        super();
        this.hidden = null;
        this.name = null;
        this.type = null;
        this.property_index = null;
        this.bm = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new ShapeElement();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        return obj;
    }
}

/*An enumeration.
*/
export const StarType = Object.freeze({
    Star: 1,
    Polygon: 2,
});
/*An enumeration.
*/
export const StrokeDashType = Object.freeze({
    Dash: 'd',
    Gap: 'g',
    Offset: 'o',
});
/*!
    Group transform
*/
export class TransformShape extends Transform
{
    hidden;
    name;
    type;
    property_index;
    bm;
    anchor_point;
    position;
    scale;
    rotation;
    opacity;
    skew;
    skew_axis;

    constructor()
    {
        super();
        this.type = 'tr';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.anchor_point = new MultiDimensional([0, 0]);
        this.position = new MultiDimensional([0, 0]);
        this.scale = new MultiDimensional([100, 100]);
        this.rotation = new Value(0);
        this.opacity = new Value(100);
        this.skew = new Value(0);
        this.skew_axis = new Value(0);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.anchor_point !== null )
            arr["a"] = value_to_lottie(this.anchor_point);
        if ( this.position !== null )
            arr["p"] = value_to_lottie(this.position);
        if ( this.scale !== null )
            arr["s"] = value_to_lottie(this.scale);
        if ( this.rotation !== null )
            arr["r"] = value_to_lottie(this.rotation);
        if ( this.opacity !== null )
            arr["o"] = value_to_lottie(this.opacity);
        if ( this.skew !== null )
            arr["sk"] = value_to_lottie(this.skew);
        if ( this.skew_axis !== null )
            arr["sa"] = value_to_lottie(this.skew_axis);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new TransformShape();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["a"] !== undefined )
            obj.anchor_point = value_from_lottie(arr["a"]);
        if ( arr["p"] !== undefined )
            obj.position = value_from_lottie(arr["p"]);
        if ( arr["s"] !== undefined )
            obj.scale = value_from_lottie(arr["s"]);
        if ( arr["r"] !== undefined )
            obj.rotation = value_from_lottie(arr["r"]);
        if ( arr["o"] !== undefined )
            obj.opacity = value_from_lottie(arr["o"]);
        if ( arr["sk"] !== undefined )
            obj.skew = value_from_lottie(arr["sk"]);
        if ( arr["sa"] !== undefined )
            obj.skew_axis = value_from_lottie(arr["sa"]);
        return obj;
    }
}

/*
    Trims shapes into a segment
*/
export class Trim extends ShapeElement
{
    hidden;
    name;
    type;
    property_index;
    bm;
    start;
    end;
    angle;
    m;

    constructor()
    {
        super();
        this.type = 'tm';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.start = new Value(0);
        this.end = new Value(100);
        this.angle = new Value(0);
        this.m = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.start !== null )
            arr["s"] = value_to_lottie(this.start);
        if ( this.end !== null )
            arr["e"] = value_to_lottie(this.end);
        if ( this.angle !== null )
            arr["o"] = value_to_lottie(this.angle);
        if ( this.m !== null )
            arr["m"] = value_to_lottie(this.m);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Trim();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["s"] !== undefined )
            obj.start = value_from_lottie(arr["s"]);
        if ( arr["e"] !== undefined )
            obj.end = value_from_lottie(arr["e"]);
        if ( arr["o"] !== undefined )
            obj.angle = value_from_lottie(arr["o"]);
        if ( arr["m"] !== undefined )
            obj.m = value_from_lottie(arr["m"]);
        return obj;
    }
}

/*!
    Solid fill color
*/
export class Fill extends ShapeElement
{
    hidden;
    name;
    type;
    property_index;
    bm;
    opacity;
    color;
    r;

    constructor()
    {
        super();
        this.type = 'fl';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.opacity = new Value(100);
        this.color = new MultiDimensional([1, 1, 1]);
        this.r = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.opacity !== null )
            arr["o"] = value_to_lottie(this.opacity);
        if ( this.color !== null )
            arr["c"] = value_to_lottie(this.color);
        if ( this.r !== null )
            arr["r"] = value_to_lottie(this.r);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Fill();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["o"] !== undefined )
            obj.opacity = value_from_lottie(arr["o"]);
        if ( arr["c"] !== undefined )
            obj.color = value_from_lottie(arr["c"]);
        if ( arr["r"] !== undefined )
            obj.r = value_from_lottie(arr["r"]);
        return obj;
    }
}

/*
*/
export class Gradient extends LottieObject
{
    start_point;
    end_point;
    gradient_type;
    highlight_length;
    highlight_angle;
    colors;

    constructor()
    {
        super();
        this.start_point = new MultiDimensional([0, 0]);
        this.end_point = new MultiDimensional([0, 0]);
        this.gradient_type = GradientType.Linear;
        this.highlight_length = new Value(0);
        this.highlight_angle = new Value(0);
        this.colors = new GradientColors();
    }

    to_lottie()
    {
        var arr = {};
        if ( this.start_point !== null )
            arr["s"] = value_to_lottie(this.start_point);
        if ( this.end_point !== null )
            arr["e"] = value_to_lottie(this.end_point);
        if ( this.gradient_type !== null )
            arr["t"] = value_to_lottie(this.gradient_type);
        if ( this.highlight_length !== null )
            arr["h"] = value_to_lottie(this.highlight_length);
        if ( this.highlight_angle !== null )
            arr["a"] = value_to_lottie(this.highlight_angle);
        if ( this.colors !== null )
            arr["g"] = value_to_lottie(this.colors);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Gradient();
        if ( arr["s"] !== undefined )
            obj.start_point = value_from_lottie(arr["s"]);
        if ( arr["e"] !== undefined )
            obj.end_point = value_from_lottie(arr["e"]);
        if ( arr["t"] !== undefined )
            obj.gradient_type = value_from_lottie(arr["t"]);
        if ( arr["h"] !== undefined )
            obj.highlight_length = value_from_lottie(arr["h"]);
        if ( arr["a"] !== undefined )
            obj.highlight_angle = value_from_lottie(arr["a"]);
        if ( arr["g"] !== undefined )
            obj.colors = value_from_lottie(arr["g"]);
        return obj;
    }
}

/*!
    Gradient fill
*/
export class GradientFill extends Gradient
{
    hidden;
    name;
    type;
    property_index;
    bm;
    start_point;
    end_point;
    gradient_type;
    highlight_length;
    highlight_angle;
    colors;
    opacity;
    r;

    constructor()
    {
        super();
        this.type = 'gf';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.start_point = new MultiDimensional([0, 0]);
        this.end_point = new MultiDimensional([0, 0]);
        this.gradient_type = GradientType.Linear;
        this.highlight_length = new Value(0);
        this.highlight_angle = new Value(0);
        this.colors = new GradientColors();
        this.opacity = new Value(100);
        this.r = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.start_point !== null )
            arr["s"] = value_to_lottie(this.start_point);
        if ( this.end_point !== null )
            arr["e"] = value_to_lottie(this.end_point);
        if ( this.gradient_type !== null )
            arr["t"] = value_to_lottie(this.gradient_type);
        if ( this.highlight_length !== null )
            arr["h"] = value_to_lottie(this.highlight_length);
        if ( this.highlight_angle !== null )
            arr["a"] = value_to_lottie(this.highlight_angle);
        if ( this.colors !== null )
            arr["g"] = value_to_lottie(this.colors);
        if ( this.opacity !== null )
            arr["o"] = value_to_lottie(this.opacity);
        if ( this.r !== null )
            arr["r"] = value_to_lottie(this.r);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new GradientFill();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["s"] !== undefined )
            obj.start_point = value_from_lottie(arr["s"]);
        if ( arr["e"] !== undefined )
            obj.end_point = value_from_lottie(arr["e"]);
        if ( arr["t"] !== undefined )
            obj.gradient_type = value_from_lottie(arr["t"]);
        if ( arr["h"] !== undefined )
            obj.highlight_length = value_from_lottie(arr["h"]);
        if ( arr["a"] !== undefined )
            obj.highlight_angle = value_from_lottie(arr["a"]);
        if ( arr["g"] !== undefined )
            obj.colors = value_from_lottie(arr["g"]);
        if ( arr["o"] !== undefined )
            obj.opacity = value_from_lottie(arr["o"]);
        if ( arr["r"] !== undefined )
            obj.r = value_from_lottie(arr["r"]);
        return obj;
    }
}

/*!
    ShapeElement that can contain other shapes
    @note Shapes inside the same group will create "holes" in other shapes
*/
export class Group extends ShapeElement
{
    hidden;
    name;
    type;
    property_index;
    bm;
    number_of_properties;
    shapes;

    constructor()
    {
        super();
        this.type = 'gr';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.number_of_properties = null;
        this.shapes = [new TransformShape()];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.number_of_properties !== null )
            arr["np"] = value_to_lottie(this.number_of_properties);
        if ( this.shapes !== null )
            arr["it"] = value_to_lottie(this.shapes);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Group();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["np"] !== undefined )
            obj.number_of_properties = value_from_lottie(arr["np"]);
        if ( arr["it"] !== undefined )
            obj.shapes = value_from_lottie(arr["it"]);
        return obj;
    }
}

/*
*/
export class Merge extends ShapeElement
{
    hidden;
    name;
    type;
    property_index;
    bm;
    merge_mode;

    constructor()
    {
        super();
        this.type = 'mm';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.merge_mode = 1;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.merge_mode !== null )
            arr["mm"] = value_to_lottie(this.merge_mode);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Merge();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["mm"] !== undefined )
            obj.merge_mode = value_from_lottie(arr["mm"]);
        return obj;
    }
}

/*
*/
export class Modifier extends ShapeElement
{
    hidden;
    name;
    type;
    property_index;
    bm;

    constructor()
    {
        super();
        this.hidden = null;
        this.name = null;
        this.type = null;
        this.property_index = null;
        this.bm = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Modifier();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        return obj;
    }
}

/*
    Duplicates previous shapes in a group
*/
export class Repeater extends Modifier
{
    hidden;
    name;
    type;
    property_index;
    bm;
    copies;
    offset;
    composite;
    transform;

    constructor()
    {
        super();
        this.type = 'rp';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.copies = new Value(1);
        this.offset = new Value(0);
        this.composite = Composite.Above;
        this.transform = new RepeaterTransform();
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.copies !== null )
            arr["c"] = value_to_lottie(this.copies);
        if ( this.offset !== null )
            arr["o"] = value_to_lottie(this.offset);
        if ( this.composite !== null )
            arr["m"] = value_to_lottie(this.composite);
        if ( this.transform !== null )
            arr["tr"] = value_to_lottie(this.transform);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Repeater();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["c"] !== undefined )
            obj.copies = value_from_lottie(arr["c"]);
        if ( arr["o"] !== undefined )
            obj.offset = value_from_lottie(arr["o"]);
        if ( arr["m"] !== undefined )
            obj.composite = value_from_lottie(arr["m"]);
        if ( arr["tr"] !== undefined )
            obj.transform = value_from_lottie(arr["tr"]);
        return obj;
    }
}

/*
    Rounds corners of other shapes
*/
export class RoundedCorners extends Modifier
{
    hidden;
    name;
    type;
    property_index;
    bm;
    radius;

    constructor()
    {
        super();
        this.type = 'rd';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.radius = new Value(0);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.radius !== null )
            arr["r"] = value_to_lottie(this.radius);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new RoundedCorners();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["r"] !== undefined )
            obj.radius = value_from_lottie(arr["r"]);
        return obj;
    }
}

/*!
    Drawable shape
*/
export class Shape extends ShapeElement
{
    hidden;
    name;
    type;
    property_index;
    bm;
    direction;

    constructor()
    {
        super();
        this.hidden = null;
        this.name = null;
        this.type = null;
        this.property_index = null;
        this.bm = null;
        this.direction = 0;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.direction !== null )
            arr["d"] = value_to_lottie(this.direction);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Shape();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["d"] !== undefined )
            obj.direction = value_from_lottie(arr["d"]);
        return obj;
    }
}

/*!
    Star shape
*/
export class Star extends Shape
{
    hidden;
    name;
    type;
    property_index;
    bm;
    direction;
    position;
    inner_radius;
    inner_roundness;
    outer_radius;
    outer_roundness;
    rotation;
    points;
    star_type;

    constructor()
    {
        super();
        this.type = 'sr';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.direction = 0;
        this.position = new MultiDimensional([0, 0]);
        this.inner_radius = new Value(0);
        this.inner_roundness = new Value(0);
        this.outer_radius = new Value(0);
        this.outer_roundness = new Value(0);
        this.rotation = new Value(0);
        this.points = new Value(5);
        this.star_type = StarType.Star;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.direction !== null )
            arr["d"] = value_to_lottie(this.direction);
        if ( this.position !== null )
            arr["p"] = value_to_lottie(this.position);
        if ( this.inner_radius !== null )
            arr["ir"] = value_to_lottie(this.inner_radius);
        if ( this.inner_roundness !== null )
            arr["is"] = value_to_lottie(this.inner_roundness);
        if ( this.outer_radius !== null )
            arr["or"] = value_to_lottie(this.outer_radius);
        if ( this.outer_roundness !== null )
            arr["os"] = value_to_lottie(this.outer_roundness);
        if ( this.rotation !== null )
            arr["r"] = value_to_lottie(this.rotation);
        if ( this.points !== null )
            arr["pt"] = value_to_lottie(this.points);
        if ( this.star_type !== null )
            arr["sy"] = value_to_lottie(this.star_type);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Star();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["d"] !== undefined )
            obj.direction = value_from_lottie(arr["d"]);
        if ( arr["p"] !== undefined )
            obj.position = value_from_lottie(arr["p"]);
        if ( arr["ir"] !== undefined )
            obj.inner_radius = value_from_lottie(arr["ir"]);
        if ( arr["is"] !== undefined )
            obj.inner_roundness = value_from_lottie(arr["is"]);
        if ( arr["or"] !== undefined )
            obj.outer_radius = value_from_lottie(arr["or"]);
        if ( arr["os"] !== undefined )
            obj.outer_roundness = value_from_lottie(arr["os"]);
        if ( arr["r"] !== undefined )
            obj.rotation = value_from_lottie(arr["r"]);
        if ( arr["pt"] !== undefined )
            obj.points = value_from_lottie(arr["pt"]);
        if ( arr["sy"] !== undefined )
            obj.star_type = value_from_lottie(arr["sy"]);
        return obj;
    }
}

/*
*/
export class StrokeDash extends LottieObject
{
    name;
    type;
    length;

    constructor()
    {
        super();
        this.name = 'dash';
        this.type = StrokeDashType.Dash;
        this.length = new Value(0);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["n"] = value_to_lottie(this.type);
        if ( this.length !== null )
            arr["v"] = value_to_lottie(this.length);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new StrokeDash();
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["n"] !== undefined )
            obj.type = value_from_lottie(arr["n"]);
        if ( arr["v"] !== undefined )
            obj.length = value_from_lottie(arr["v"]);
        return obj;
    }
}

/*
*/
export class BaseStroke extends LottieObject
{
    line_cap;
    line_join;
    miter_limit;
    opacity;
    width;
    dashes;

    constructor()
    {
        super();
        this.line_cap = LineCap.Round;
        this.line_join = LineJoin.Round;
        this.miter_limit = 0;
        this.opacity = new Value(100);
        this.width = new Value(1);
        this.dashes = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.line_cap !== null )
            arr["lc"] = value_to_lottie(this.line_cap);
        if ( this.line_join !== null )
            arr["lj"] = value_to_lottie(this.line_join);
        if ( this.miter_limit !== null )
            arr["ml"] = value_to_lottie(this.miter_limit);
        if ( this.opacity !== null )
            arr["o"] = value_to_lottie(this.opacity);
        if ( this.width !== null )
            arr["w"] = value_to_lottie(this.width);
        if ( this.dashes !== null )
            arr["d"] = value_to_lottie(this.dashes);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new BaseStroke();
        if ( arr["lc"] !== undefined )
            obj.line_cap = value_from_lottie(arr["lc"]);
        if ( arr["lj"] !== undefined )
            obj.line_join = value_from_lottie(arr["lj"]);
        if ( arr["ml"] !== undefined )
            obj.miter_limit = value_from_lottie(arr["ml"]);
        if ( arr["o"] !== undefined )
            obj.opacity = value_from_lottie(arr["o"]);
        if ( arr["w"] !== undefined )
            obj.width = value_from_lottie(arr["w"]);
        if ( arr["d"] !== undefined )
            obj.dashes = value_from_lottie(arr["d"]);
        return obj;
    }
}

/*!
    Ellipse shape
*/
export class Ellipse extends Shape
{
    hidden;
    name;
    type;
    property_index;
    bm;
    direction;
    position;
    size;

    constructor()
    {
        super();
        this.type = 'el';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.direction = 0;
        this.position = new MultiDimensional([0, 0]);
        this.size = new MultiDimensional([0, 0]);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.direction !== null )
            arr["d"] = value_to_lottie(this.direction);
        if ( this.position !== null )
            arr["p"] = value_to_lottie(this.position);
        if ( this.size !== null )
            arr["s"] = value_to_lottie(this.size);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Ellipse();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["d"] !== undefined )
            obj.direction = value_from_lottie(arr["d"]);
        if ( arr["p"] !== undefined )
            obj.position = value_from_lottie(arr["p"]);
        if ( arr["s"] !== undefined )
            obj.size = value_from_lottie(arr["s"]);
        return obj;
    }
}

/*!
    Gradient stroke
*/
export class GradientStroke extends Gradient
{
    hidden;
    name;
    type;
    property_index;
    bm;
    line_cap;
    line_join;
    miter_limit;
    opacity;
    width;
    dashes;
    start_point;
    end_point;
    gradient_type;
    highlight_length;
    highlight_angle;
    colors;

    constructor()
    {
        super();
        this.type = 'gs';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.line_cap = LineCap.Round;
        this.line_join = LineJoin.Round;
        this.miter_limit = 0;
        this.opacity = new Value(100);
        this.width = new Value(1);
        this.dashes = null;
        this.start_point = new MultiDimensional([0, 0]);
        this.end_point = new MultiDimensional([0, 0]);
        this.gradient_type = GradientType.Linear;
        this.highlight_length = new Value(0);
        this.highlight_angle = new Value(0);
        this.colors = new GradientColors();
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.line_cap !== null )
            arr["lc"] = value_to_lottie(this.line_cap);
        if ( this.line_join !== null )
            arr["lj"] = value_to_lottie(this.line_join);
        if ( this.miter_limit !== null )
            arr["ml"] = value_to_lottie(this.miter_limit);
        if ( this.opacity !== null )
            arr["o"] = value_to_lottie(this.opacity);
        if ( this.width !== null )
            arr["w"] = value_to_lottie(this.width);
        if ( this.dashes !== null )
            arr["d"] = value_to_lottie(this.dashes);
        if ( this.start_point !== null )
            arr["s"] = value_to_lottie(this.start_point);
        if ( this.end_point !== null )
            arr["e"] = value_to_lottie(this.end_point);
        if ( this.gradient_type !== null )
            arr["t"] = value_to_lottie(this.gradient_type);
        if ( this.highlight_length !== null )
            arr["h"] = value_to_lottie(this.highlight_length);
        if ( this.highlight_angle !== null )
            arr["a"] = value_to_lottie(this.highlight_angle);
        if ( this.colors !== null )
            arr["g"] = value_to_lottie(this.colors);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new GradientStroke();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["lc"] !== undefined )
            obj.line_cap = value_from_lottie(arr["lc"]);
        if ( arr["lj"] !== undefined )
            obj.line_join = value_from_lottie(arr["lj"]);
        if ( arr["ml"] !== undefined )
            obj.miter_limit = value_from_lottie(arr["ml"]);
        if ( arr["o"] !== undefined )
            obj.opacity = value_from_lottie(arr["o"]);
        if ( arr["w"] !== undefined )
            obj.width = value_from_lottie(arr["w"]);
        if ( arr["d"] !== undefined )
            obj.dashes = value_from_lottie(arr["d"]);
        if ( arr["s"] !== undefined )
            obj.start_point = value_from_lottie(arr["s"]);
        if ( arr["e"] !== undefined )
            obj.end_point = value_from_lottie(arr["e"]);
        if ( arr["t"] !== undefined )
            obj.gradient_type = value_from_lottie(arr["t"]);
        if ( arr["h"] !== undefined )
            obj.highlight_length = value_from_lottie(arr["h"]);
        if ( arr["a"] !== undefined )
            obj.highlight_angle = value_from_lottie(arr["a"]);
        if ( arr["g"] !== undefined )
            obj.colors = value_from_lottie(arr["g"]);
        return obj;
    }
}

/*!
    Animatable Bezier curve
*/
export class Path extends Shape
{
    hidden;
    name;
    type;
    property_index;
    bm;
    direction;
    shape;
    index;

    constructor()
    {
        super();
        this.type = 'sh';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.direction = 0;
        this.shape = new ShapeProperty();
        this.index = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.direction !== null )
            arr["d"] = value_to_lottie(this.direction);
        if ( this.shape !== null )
            arr["ks"] = value_to_lottie(this.shape);
        if ( this.index !== null )
            arr["ind"] = value_to_lottie(this.index);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Path();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["d"] !== undefined )
            obj.direction = value_from_lottie(arr["d"]);
        if ( arr["ks"] !== undefined )
            obj.shape = value_from_lottie(arr["ks"]);
        if ( arr["ind"] !== undefined )
            obj.index = value_from_lottie(arr["ind"]);
        return obj;
    }
}

/*!
    A simple rectangle shape
*/
export class Rect extends Shape
{
    hidden;
    name;
    type;
    property_index;
    bm;
    direction;
    position;
    size;
    rounded;

    constructor()
    {
        super();
        this.type = 'rc';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.direction = 0;
        this.position = new MultiDimensional([0, 0]);
        this.size = new MultiDimensional([0, 0]);
        this.rounded = new Value(0);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.direction !== null )
            arr["d"] = value_to_lottie(this.direction);
        if ( this.position !== null )
            arr["p"] = value_to_lottie(this.position);
        if ( this.size !== null )
            arr["s"] = value_to_lottie(this.size);
        if ( this.rounded !== null )
            arr["r"] = value_to_lottie(this.rounded);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Rect();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["d"] !== undefined )
            obj.direction = value_from_lottie(arr["d"]);
        if ( arr["p"] !== undefined )
            obj.position = value_from_lottie(arr["p"]);
        if ( arr["s"] !== undefined )
            obj.size = value_from_lottie(arr["s"]);
        if ( arr["r"] !== undefined )
            obj.rounded = value_from_lottie(arr["r"]);
        return obj;
    }
}

/*!
    Solid stroke
*/
export class Stroke extends BaseStroke
{
    hidden;
    name;
    type;
    property_index;
    bm;
    line_cap;
    line_join;
    miter_limit;
    opacity;
    width;
    dashes;
    color;

    constructor()
    {
        super();
        this.type = 'st';
        this.hidden = null;
        this.name = null;
        this.property_index = null;
        this.bm = null;
        this.line_cap = LineCap.Round;
        this.line_join = LineJoin.Round;
        this.miter_limit = 0;
        this.opacity = new Value(100);
        this.width = new Value(1);
        this.dashes = null;
        this.color = new MultiDimensional([0, 0, 0]);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.bm !== null )
            arr["bm"] = value_to_lottie(this.bm);
        if ( this.line_cap !== null )
            arr["lc"] = value_to_lottie(this.line_cap);
        if ( this.line_join !== null )
            arr["lj"] = value_to_lottie(this.line_join);
        if ( this.miter_limit !== null )
            arr["ml"] = value_to_lottie(this.miter_limit);
        if ( this.opacity !== null )
            arr["o"] = value_to_lottie(this.opacity);
        if ( this.width !== null )
            arr["w"] = value_to_lottie(this.width);
        if ( this.dashes !== null )
            arr["d"] = value_to_lottie(this.dashes);
        if ( this.color !== null )
            arr["c"] = value_to_lottie(this.color);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Stroke();
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["bm"] !== undefined )
            obj.bm = value_from_lottie(arr["bm"]);
        if ( arr["lc"] !== undefined )
            obj.line_cap = value_from_lottie(arr["lc"]);
        if ( arr["lj"] !== undefined )
            obj.line_join = value_from_lottie(arr["lj"]);
        if ( arr["ml"] !== undefined )
            obj.miter_limit = value_from_lottie(arr["ml"]);
        if ( arr["o"] !== undefined )
            obj.opacity = value_from_lottie(arr["o"]);
        if ( arr["w"] !== undefined )
            obj.width = value_from_lottie(arr["w"]);
        if ( arr["d"] !== undefined )
            obj.dashes = value_from_lottie(arr["d"]);
        if ( arr["c"] !== undefined )
            obj.color = value_from_lottie(arr["c"]);
        return obj;
    }
}

