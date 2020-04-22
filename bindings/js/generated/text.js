import { value_to_lottie, value_from_lottie, LottieObject } from '../base.js';
import { Value, MultiDimensional } from './properties.js';

/*
*/
export class Font extends LottieObject
{
    ascent;
    font_family;
    name;
    font_style;

    constructor()
    {
        super();
        this.ascent = null;
        this.font_family = 'sans';
        this.name = 'sans-Regular';
        this.font_style = 'Regular';
    }

    to_lottie()
    {
        var arr = {};
        if ( this.ascent !== null )
            arr["ascent"] = value_to_lottie(this.ascent);
        if ( this.font_family !== null )
            arr["fFamily"] = value_to_lottie(this.font_family);
        if ( this.name !== null )
            arr["fName"] = value_to_lottie(this.name);
        if ( this.font_style !== null )
            arr["fStyle"] = value_to_lottie(this.font_style);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Font();
        if ( arr["ascent"] !== undefined )
            obj.ascent = value_from_lottie(arr["ascent"]);
        if ( arr["fFamily"] !== undefined )
            obj.font_family = value_from_lottie(arr["fFamily"]);
        if ( arr["fName"] !== undefined )
            obj.name = value_from_lottie(arr["fName"]);
        if ( arr["fStyle"] !== undefined )
            obj.font_style = value_from_lottie(arr["fStyle"]);
        return obj;
    }
}

/*
*/
export class FontList extends LottieObject
{
    list;

    constructor()
    {
        super();
        this.list = [];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.list !== null )
            arr["list"] = value_to_lottie(this.list);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new FontList();
        if ( arr["list"] !== undefined )
            obj.list = value_from_lottie(arr["list"]);
        return obj;
    }
}

/*
*/
export class MaskedPath extends LottieObject
{
    mask;
    f;
    l;
    r;

    constructor()
    {
        super();
        this.mask = null;
        this.f = null;
        this.l = null;
        this.r = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.mask !== null )
            arr["m"] = value_to_lottie(this.mask);
        if ( this.f !== null )
            arr["f"] = value_to_lottie(this.f);
        if ( this.l !== null )
            arr["l"] = value_to_lottie(this.l);
        if ( this.r !== null )
            arr["r"] = value_to_lottie(this.r);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new MaskedPath();
        if ( arr["m"] !== undefined )
            obj.mask = value_from_lottie(arr["m"]);
        if ( arr["f"] !== undefined )
            obj.f = value_from_lottie(arr["f"]);
        if ( arr["l"] !== undefined )
            obj.l = value_from_lottie(arr["l"]);
        if ( arr["r"] !== undefined )
            obj.r = value_from_lottie(arr["r"]);
        return obj;
    }
}

/*
*/
export class TextAnimatorDataProperty extends LottieObject
{
    rotation;
    rx;
    ry;
    skew;
    skew_axis;
    scale;
    anchor;
    opacity;
    position;
    stroke_width;
    stroke_color;
    fill_color;
    fh;
    fs;
    fb;
    tracking;

    constructor()
    {
        super();
        this.rotation = new Value(0);
        this.rx = new Value(0);
        this.ry = new Value(0);
        this.skew = new Value(0);
        this.skew_axis = new Value(0);
        this.scale = new MultiDimensional(null);
        this.anchor = new MultiDimensional(null);
        this.opacity = new Value(0);
        this.position = new MultiDimensional(null);
        this.stroke_width = new Value(0);
        this.stroke_color = new MultiDimensional(null);
        this.fill_color = new MultiDimensional(null);
        this.fh = new Value(0);
        this.fs = new Value(0);
        this.fb = new Value(0);
        this.tracking = new Value(0);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.rotation !== null )
            arr["r"] = value_to_lottie(this.rotation);
        if ( this.rx !== null )
            arr["rx"] = value_to_lottie(this.rx);
        if ( this.ry !== null )
            arr["ry"] = value_to_lottie(this.ry);
        if ( this.skew !== null )
            arr["sk"] = value_to_lottie(this.skew);
        if ( this.skew_axis !== null )
            arr["sa"] = value_to_lottie(this.skew_axis);
        if ( this.scale !== null )
            arr["s"] = value_to_lottie(this.scale);
        if ( this.anchor !== null )
            arr["a"] = value_to_lottie(this.anchor);
        if ( this.opacity !== null )
            arr["o"] = value_to_lottie(this.opacity);
        if ( this.position !== null )
            arr["p"] = value_to_lottie(this.position);
        if ( this.stroke_width !== null )
            arr["sw"] = value_to_lottie(this.stroke_width);
        if ( this.stroke_color !== null )
            arr["sc"] = value_to_lottie(this.stroke_color);
        if ( this.fill_color !== null )
            arr["fc"] = value_to_lottie(this.fill_color);
        if ( this.fh !== null )
            arr["fh"] = value_to_lottie(this.fh);
        if ( this.fs !== null )
            arr["fs"] = value_to_lottie(this.fs);
        if ( this.fb !== null )
            arr["fb"] = value_to_lottie(this.fb);
        if ( this.tracking !== null )
            arr["t"] = value_to_lottie(this.tracking);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new TextAnimatorDataProperty();
        if ( arr["r"] !== undefined )
            obj.rotation = value_from_lottie(arr["r"]);
        if ( arr["rx"] !== undefined )
            obj.rx = value_from_lottie(arr["rx"]);
        if ( arr["ry"] !== undefined )
            obj.ry = value_from_lottie(arr["ry"]);
        if ( arr["sk"] !== undefined )
            obj.skew = value_from_lottie(arr["sk"]);
        if ( arr["sa"] !== undefined )
            obj.skew_axis = value_from_lottie(arr["sa"]);
        if ( arr["s"] !== undefined )
            obj.scale = value_from_lottie(arr["s"]);
        if ( arr["a"] !== undefined )
            obj.anchor = value_from_lottie(arr["a"]);
        if ( arr["o"] !== undefined )
            obj.opacity = value_from_lottie(arr["o"]);
        if ( arr["p"] !== undefined )
            obj.position = value_from_lottie(arr["p"]);
        if ( arr["sw"] !== undefined )
            obj.stroke_width = value_from_lottie(arr["sw"]);
        if ( arr["sc"] !== undefined )
            obj.stroke_color = value_from_lottie(arr["sc"]);
        if ( arr["fc"] !== undefined )
            obj.fill_color = value_from_lottie(arr["fc"]);
        if ( arr["fh"] !== undefined )
            obj.fh = value_from_lottie(arr["fh"]);
        if ( arr["fs"] !== undefined )
            obj.fs = value_from_lottie(arr["fs"]);
        if ( arr["fb"] !== undefined )
            obj.fb = value_from_lottie(arr["fb"]);
        if ( arr["t"] !== undefined )
            obj.tracking = value_from_lottie(arr["t"]);
        return obj;
    }
}

/*An enumeration.
*/
export const TextJustify = Object.freeze({
    Left: 0,
    Right: 1,
    Center: 2,
});
/*
*/
export class TextMoreOptions extends LottieObject
{
    alignment;
    g;

    constructor()
    {
        super();
        this.alignment = new MultiDimensional([0, 0]);
        this.g = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.alignment !== null )
            arr["a"] = value_to_lottie(this.alignment);
        if ( this.g !== null )
            arr["g"] = value_to_lottie(this.g);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new TextMoreOptions();
        if ( arr["a"] !== undefined )
            obj.alignment = value_from_lottie(arr["a"]);
        if ( arr["g"] !== undefined )
            obj.g = value_from_lottie(arr["g"]);
        return obj;
    }
}

/*!
    @see http://docs.aenhancers.com/other/textdocument/
*/
export class TextDocument extends LottieObject
{
    font_family;
    color;
    font_size;
    line_height;
    wrap_size;
    text;
    justify;

    constructor()
    {
        super();
        this.font_family = '';
        this.color = [0, 0, 0];
        this.font_size = 10;
        this.line_height = null;
        this.wrap_size = null;
        this.text = '';
        this.justify = TextJustify.Left;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.font_family !== null )
            arr["f"] = value_to_lottie(this.font_family);
        if ( this.color !== null )
            arr["fc"] = value_to_lottie(this.color);
        if ( this.font_size !== null )
            arr["s"] = value_to_lottie(this.font_size);
        if ( this.line_height !== null )
            arr["lh"] = value_to_lottie(this.line_height);
        if ( this.wrap_size !== null )
            arr["sz"] = value_to_lottie(this.wrap_size);
        if ( this.text !== null )
            arr["t"] = value_to_lottie(this.text);
        if ( this.justify !== null )
            arr["j"] = value_to_lottie(this.justify);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new TextDocument();
        if ( arr["f"] !== undefined )
            obj.font_family = value_from_lottie(arr["f"]);
        if ( arr["fc"] !== undefined )
            obj.color = value_from_lottie(arr["fc"]);
        if ( arr["s"] !== undefined )
            obj.font_size = value_from_lottie(arr["s"]);
        if ( arr["lh"] !== undefined )
            obj.line_height = value_from_lottie(arr["lh"]);
        if ( arr["sz"] !== undefined )
            obj.wrap_size = value_from_lottie(arr["sz"]);
        if ( arr["t"] !== undefined )
            obj.text = value_from_lottie(arr["t"]);
        if ( arr["j"] !== undefined )
            obj.justify = value_from_lottie(arr["j"]);
        return obj;
    }
}

/*
*/
export class TextDataKeyframe extends LottieObject
{
    start;
    time;

    constructor()
    {
        super();
        this.start = null;
        this.time = 0;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.start !== null )
            arr["s"] = value_to_lottie(this.start);
        if ( this.time !== null )
            arr["t"] = value_to_lottie(this.time);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new TextDataKeyframe();
        if ( arr["s"] !== undefined )
            obj.start = value_from_lottie(arr["s"]);
        if ( arr["t"] !== undefined )
            obj.time = value_from_lottie(arr["t"]);
        return obj;
    }
}

/*
*/
export class TextData extends LottieObject
{
    keyframes;

    constructor()
    {
        super();
        this.keyframes = [];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.keyframes !== null )
            arr["k"] = value_to_lottie(this.keyframes);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new TextData();
        if ( arr["k"] !== undefined )
            obj.keyframes = value_from_lottie(arr["k"]);
        return obj;
    }
}

/*
*/
export class TextAnimatorData extends LottieObject
{
    properties;
    data;
    more_options;
    masked_path;

    constructor()
    {
        super();
        this.properties = [];
        this.data = new TextData();
        this.more_options = new TextMoreOptions();
        this.masked_path = new MaskedPath();
    }

    to_lottie()
    {
        var arr = {};
        if ( this.properties !== null )
            arr["a"] = value_to_lottie(this.properties);
        if ( this.data !== null )
            arr["d"] = value_to_lottie(this.data);
        if ( this.more_options !== null )
            arr["m"] = value_to_lottie(this.more_options);
        if ( this.masked_path !== null )
            arr["p"] = value_to_lottie(this.masked_path);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new TextAnimatorData();
        if ( arr["a"] !== undefined )
            obj.properties = value_from_lottie(arr["a"]);
        if ( arr["d"] !== undefined )
            obj.data = value_from_lottie(arr["d"]);
        if ( arr["m"] !== undefined )
            obj.more_options = value_from_lottie(arr["m"]);
        if ( arr["p"] !== undefined )
            obj.masked_path = value_from_lottie(arr["p"]);
        return obj;
    }
}

