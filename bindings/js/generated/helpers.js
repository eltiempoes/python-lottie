import { value_to_lottie, value_from_lottie, LottieObject } from '../base.js';
import { ShapeProperty, Value, MultiDimensional } from './properties.js';

/*!
    How masks interact with each other
    \see https://helpx.adobe.com/after-effects/using/alpha-channels-masks-mattes.html
    
*/
export const MaskMode = Object.freeze({
    No: 'n',
    Add: 'a',
    Subtract: 's',
    Intersect: 'i',
    Lightent: 'l',
    Darken: 'd',
    Difference: 'f',
});
/*!
    Layer transform
*/
export class Transform extends LottieObject
{
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
        var obj = new Transform();
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
*/
export class Mask extends LottieObject
{
    inverted;
    name;
    shape;
    opacity;
    mode;
    dilate;

    constructor()
    {
        super();
        this.inverted = false;
        this.name = null;
        this.shape = new ShapeProperty();
        this.opacity = new Value(100);
        this.mode = MaskMode.Intersect;
        this.dilate = new Value(0);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.inverted !== null )
            arr["inv"] = value_to_lottie(this.inverted);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.shape !== null )
            arr["pt"] = value_to_lottie(this.shape);
        if ( this.opacity !== null )
            arr["o"] = value_to_lottie(this.opacity);
        if ( this.mode !== null )
            arr["mode"] = value_to_lottie(this.mode);
        if ( this.dilate !== null )
            arr["x"] = value_to_lottie(this.dilate);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Mask();
        if ( arr["inv"] !== undefined )
            obj.inverted = value_from_lottie(arr["inv"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["pt"] !== undefined )
            obj.shape = value_from_lottie(arr["pt"]);
        if ( arr["o"] !== undefined )
            obj.opacity = value_from_lottie(arr["o"]);
        if ( arr["mode"] !== undefined )
            obj.mode = value_from_lottie(arr["mode"]);
        if ( arr["x"] !== undefined )
            obj.dilate = value_from_lottie(arr["x"]);
        return obj;
    }
}

