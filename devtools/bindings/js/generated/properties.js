import { value_to_lottie, value_from_lottie, LottieObject } from '../base.js';
import { KeyframeBezierHandle } from './easing.js';
import { Bezier } from './bezier.js';

/*
*/
export class Keyframe extends LottieObject
{
    time;
    in_value;
    out_value;
    jump;

    constructor()
    {
        super();
        this.time = 0;
        this.in_value = null;
        this.out_value = null;
        this.jump = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.time !== null )
            arr["t"] = value_to_lottie(this.time);
        if ( this.in_value !== null )
            arr["i"] = value_to_lottie(this.in_value);
        if ( this.out_value !== null )
            arr["o"] = value_to_lottie(this.out_value);
        if ( this.jump !== null )
            arr["h"] = value_to_lottie(Number(this.jump));
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Keyframe();
        if ( arr["t"] !== undefined )
            obj.time = value_from_lottie(arr["t"]);
        if ( arr["i"] !== undefined )
            obj.in_value = value_from_lottie(arr["i"]);
        if ( arr["o"] !== undefined )
            obj.out_value = value_from_lottie(arr["o"]);
        if ( arr["h"] !== undefined )
            obj.jump = value_from_lottie(Boolean(arr["h"]));
        return obj;
    }
}

/*!
    Keyframe for MultiDimensional values

    @par Bezier easing
    @parblock
    Imagine a quadratic bezier, with starting point at (0, 0) and end point at (1, 1).

    \p out_value and \p in_value are the other two handles for a quadratic bezier,
    expressed as absoulte values in this 0-1 space.

    See also https://cubic-bezier.com/
    @endparblock
*/
export class OffsetKeyframe extends Keyframe
{
    time;
    in_value;
    out_value;
    jump;
    start;
    end;
    in_tan;
    out_tan;

    constructor()
    {
        super();
        this.time = 0;
        this.in_value = null;
        this.out_value = null;
        this.jump = null;
        this.start = null;
        this.end = null;
        this.in_tan = null;
        this.out_tan = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.time !== null )
            arr["t"] = value_to_lottie(this.time);
        if ( this.in_value !== null )
            arr["i"] = value_to_lottie(this.in_value);
        if ( this.out_value !== null )
            arr["o"] = value_to_lottie(this.out_value);
        if ( this.jump !== null )
            arr["h"] = value_to_lottie(Number(this.jump));
        if ( this.start !== null )
            arr["s"] = value_to_lottie(this.start);
        if ( this.end !== null )
            arr["e"] = value_to_lottie(this.end);
        if ( this.in_tan !== null )
            arr["ti"] = value_to_lottie(this.in_tan);
        if ( this.out_tan !== null )
            arr["to"] = value_to_lottie(this.out_tan);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new OffsetKeyframe();
        if ( arr["t"] !== undefined )
            obj.time = value_from_lottie(arr["t"]);
        if ( arr["i"] !== undefined )
            obj.in_value = value_from_lottie(arr["i"]);
        if ( arr["o"] !== undefined )
            obj.out_value = value_from_lottie(arr["o"]);
        if ( arr["h"] !== undefined )
            obj.jump = value_from_lottie(Boolean(arr["h"]));
        if ( arr["s"] !== undefined )
            obj.start = value_from_lottie(arr["s"]);
        if ( arr["e"] !== undefined )
            obj.end = value_from_lottie(arr["e"]);
        if ( arr["ti"] !== undefined )
            obj.in_tan = value_from_lottie(arr["ti"]);
        if ( arr["to"] !== undefined )
            obj.out_tan = value_from_lottie(arr["to"]);
        return obj;
    }
}

/*!
    Keyframe holding Bezier objects
*/
export class ShapePropKeyframe extends Keyframe
{
    time;
    in_value;
    out_value;
    jump;
    start;
    end;

    constructor()
    {
        super();
        this.time = 0;
        this.in_value = null;
        this.out_value = null;
        this.jump = null;
        this.start = null;
        this.end = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.time !== null )
            arr["t"] = value_to_lottie(this.time);
        if ( this.in_value !== null )
            arr["i"] = value_to_lottie(this.in_value);
        if ( this.out_value !== null )
            arr["o"] = value_to_lottie(this.out_value);
        if ( this.jump !== null )
            arr["h"] = value_to_lottie(Number(this.jump));
        if ( this.start !== null )
            arr["s"] = value_to_lottie([this.start]);
        if ( this.end !== null )
            arr["e"] = value_to_lottie([this.end]);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new ShapePropKeyframe();
        if ( arr["t"] !== undefined )
            obj.time = value_from_lottie(arr["t"]);
        if ( arr["i"] !== undefined )
            obj.in_value = value_from_lottie(arr["i"]);
        if ( arr["o"] !== undefined )
            obj.out_value = value_from_lottie(arr["o"]);
        if ( arr["h"] !== undefined )
            obj.jump = value_from_lottie(Boolean(arr["h"]));
        if ( arr["s"] !== undefined )
            obj.start = value_from_lottie(arr["s"][0]);
        if ( arr["e"] !== undefined )
            obj.end = value_from_lottie(arr["e"][0]);
        return obj;
    }
}

/*!
    An animatable property that holds a Bezier
*/
export class ShapeProperty extends LottieObject
{
    value;
    property_index;
    animated;
    keyframes;

    constructor()
    {
        super();
        this.value = new Bezier();
        this.property_index = null;
        this.animated = false;
        this.keyframes = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.value !== null )
            arr["k"] = value_to_lottie(this.value);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.animated !== null )
            arr["a"] = value_to_lottie(Number(this.animated));
        if ( this.keyframes !== null )
            arr["k"] = value_to_lottie(this.keyframes);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new ShapeProperty();
        if ( arr["k"] !== undefined )
            obj.value = value_from_lottie(arr["k"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["a"] !== undefined )
            obj.animated = value_from_lottie(Boolean(arr["a"]));
        if ( arr["k"] !== undefined )
            obj.keyframes = value_from_lottie(arr["k"]);
        return obj;
    }
}

/*!
    An animatable property that holds a float
*/
export class Value extends LottieObject
{
    value;
    property_index;
    animated;
    keyframes;

    constructor(value=null)
    {
        super();
        this.property_index = null;
        this.animated = false;
        this.keyframes = null;
        this.value = value;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.value !== null )
            arr["k"] = value_to_lottie(this.value);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.animated !== null )
            arr["a"] = value_to_lottie(Number(this.animated));
        if ( this.keyframes !== null )
            arr["k"] = value_to_lottie(this.keyframes);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Value();
        if ( arr["k"] !== undefined )
            obj.value = value_from_lottie(arr["k"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["a"] !== undefined )
            obj.animated = value_from_lottie(Boolean(arr["a"]));
        if ( arr["k"] !== undefined )
            obj.keyframes = value_from_lottie(arr["k"]);
        return obj;
    }
}

/*!
    An animatable property that holds a NVector
*/
export class MultiDimensional extends LottieObject
{
    value;
    property_index;
    animated;
    keyframes;

    constructor(value=null)
    {
        super();
        this.property_index = null;
        this.animated = false;
        this.keyframes = null;
        this.value = value;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.value !== null )
            arr["k"] = value_to_lottie(this.value);
        if ( this.property_index !== null )
            arr["ix"] = value_to_lottie(this.property_index);
        if ( this.animated !== null )
            arr["a"] = value_to_lottie(Number(this.animated));
        if ( this.keyframes !== null )
            arr["k"] = value_to_lottie(this.keyframes);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new MultiDimensional();
        if ( arr["k"] !== undefined )
            obj.value = value_from_lottie(arr["k"]);
        if ( arr["ix"] !== undefined )
            obj.property_index = value_from_lottie(arr["ix"]);
        if ( arr["a"] !== undefined )
            obj.animated = value_from_lottie(Boolean(arr["a"]));
        if ( arr["k"] !== undefined )
            obj.keyframes = value_from_lottie(arr["k"]);
        return obj;
    }
}

/*!
    Represents colors and offsets in a gradient
*/
export class GradientColors extends LottieObject
{
    colors;
    count;

    constructor()
    {
        super();
        this.colors = new MultiDimensional([]);
        this.count = 0;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.colors !== null )
            arr["k"] = value_to_lottie(this.colors);
        if ( this.count !== null )
            arr["p"] = value_to_lottie(this.count);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new GradientColors();
        if ( arr["k"] !== undefined )
            obj.colors = value_from_lottie(arr["k"]);
        if ( arr["p"] !== undefined )
            obj.count = value_from_lottie(arr["p"]);
        return obj;
    }
}

