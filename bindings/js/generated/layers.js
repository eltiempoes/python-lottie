import { value_to_lottie, value_from_lottie, LottieObject } from '../base.js';
import { Mask, Transform } from './helpers.js';
import { ShapeElement } from './shapes.js';
import { Value } from './properties.js';
import { Effect } from './effects.js';
import { TextAnimatorData } from './text.js';

/*An enumeration.
*/
export const BlendMode = Object.freeze({
    Normal: 0,
    Multiply: 1,
    Screen: 2,
    Overlay: 3,
    Darken: 4,
    Lighten: 5,
    ColorDodge: 6,
    ColorBurn: 7,
    HardLight: 8,
    SoftLight: 9,
    Difference: 10,
    Exclusion: 11,
    Hue: 12,
    Saturation: 13,
    Color: 14,
    Luminosity: 15,
});
/*An enumeration.
*/
export const MatteMode = Object.freeze({
    Normal: 0,
    Alpha: 1,
    InvertedAlpha: 2,
    Luma: 3,
    InvertedLuma: 4,
});
/*
*/
export class Layer extends LottieObject
{
    threedimensional;
    hidden;
    type;
    name;
    parent;
    stretch;
    transform;
    auto_orient;
    in_point;
    out_point;
    start_time;
    blend_mode;
    matte_mode;
    index;
    has_masks;
    masks;
    effects;

    constructor()
    {
        super();
        this.threedimensional = false;
        this.hidden = null;
        this.type = null;
        this.name = null;
        this.parent = null;
        this.stretch = 1;
        this.transform = new Transform();
        this.auto_orient = false;
        this.in_point = null;
        this.out_point = null;
        this.start_time = 0;
        this.blend_mode = BlendMode.Normal;
        this.matte_mode = null;
        this.index = null;
        this.has_masks = null;
        this.masks = null;
        this.effects = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.threedimensional !== null )
            arr["ddd"] = value_to_lottie(Number(this.threedimensional));
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.parent !== null )
            arr["parent"] = value_to_lottie(this.parent);
        if ( this.stretch !== null )
            arr["sr"] = value_to_lottie(this.stretch);
        if ( this.transform !== null )
            arr["ks"] = value_to_lottie(this.transform);
        if ( this.auto_orient !== null )
            arr["ao"] = value_to_lottie(Number(this.auto_orient));
        if ( this.in_point !== null )
            arr["ip"] = value_to_lottie(this.in_point);
        if ( this.out_point !== null )
            arr["op"] = value_to_lottie(this.out_point);
        if ( this.start_time !== null )
            arr["st"] = value_to_lottie(this.start_time);
        if ( this.blend_mode !== null )
            arr["bm"] = value_to_lottie(this.blend_mode);
        if ( this.matte_mode !== null )
            arr["tt"] = value_to_lottie(this.matte_mode);
        if ( this.index !== null )
            arr["ind"] = value_to_lottie(this.index);
        if ( this.has_masks !== null )
            arr["hasMask"] = value_to_lottie(this.has_masks);
        if ( this.masks !== null )
            arr["masksProperties"] = value_to_lottie(this.masks);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Layer();
        if ( arr["ddd"] !== undefined )
            obj.threedimensional = value_from_lottie(Boolean(arr["ddd"]));
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["parent"] !== undefined )
            obj.parent = value_from_lottie(arr["parent"]);
        if ( arr["sr"] !== undefined )
            obj.stretch = value_from_lottie(arr["sr"]);
        if ( arr["ks"] !== undefined )
            obj.transform = value_from_lottie(arr["ks"]);
        if ( arr["ao"] !== undefined )
            obj.auto_orient = value_from_lottie(Boolean(arr["ao"]));
        if ( arr["ip"] !== undefined )
            obj.in_point = value_from_lottie(arr["ip"]);
        if ( arr["op"] !== undefined )
            obj.out_point = value_from_lottie(arr["op"]);
        if ( arr["st"] !== undefined )
            obj.start_time = value_from_lottie(arr["st"]);
        if ( arr["bm"] !== undefined )
            obj.blend_mode = value_from_lottie(arr["bm"]);
        if ( arr["tt"] !== undefined )
            obj.matte_mode = value_from_lottie(arr["tt"]);
        if ( arr["ind"] !== undefined )
            obj.index = value_from_lottie(arr["ind"]);
        if ( arr["hasMask"] !== undefined )
            obj.has_masks = value_from_lottie(arr["hasMask"]);
        if ( arr["masksProperties"] !== undefined )
            obj.masks = value_from_lottie(arr["masksProperties"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        return obj;
    }
}

/*!
    Layer with no data, useful to group layers together
*/
export class NullLayer extends Layer
{
    threedimensional;
    hidden;
    type;
    name;
    parent;
    stretch;
    transform;
    auto_orient;
    in_point;
    out_point;
    start_time;
    blend_mode;
    matte_mode;
    index;
    has_masks;
    masks;
    effects;

    constructor()
    {
        super();
        this.type = 3;
        this.threedimensional = false;
        this.hidden = null;
        this.name = null;
        this.parent = null;
        this.stretch = 1;
        this.transform = new Transform();
        this.auto_orient = false;
        this.in_point = null;
        this.out_point = null;
        this.start_time = 0;
        this.blend_mode = BlendMode.Normal;
        this.matte_mode = null;
        this.index = null;
        this.has_masks = null;
        this.masks = null;
        this.effects = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.threedimensional !== null )
            arr["ddd"] = value_to_lottie(Number(this.threedimensional));
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.parent !== null )
            arr["parent"] = value_to_lottie(this.parent);
        if ( this.stretch !== null )
            arr["sr"] = value_to_lottie(this.stretch);
        if ( this.transform !== null )
            arr["ks"] = value_to_lottie(this.transform);
        if ( this.auto_orient !== null )
            arr["ao"] = value_to_lottie(Number(this.auto_orient));
        if ( this.in_point !== null )
            arr["ip"] = value_to_lottie(this.in_point);
        if ( this.out_point !== null )
            arr["op"] = value_to_lottie(this.out_point);
        if ( this.start_time !== null )
            arr["st"] = value_to_lottie(this.start_time);
        if ( this.blend_mode !== null )
            arr["bm"] = value_to_lottie(this.blend_mode);
        if ( this.matte_mode !== null )
            arr["tt"] = value_to_lottie(this.matte_mode);
        if ( this.index !== null )
            arr["ind"] = value_to_lottie(this.index);
        if ( this.has_masks !== null )
            arr["hasMask"] = value_to_lottie(this.has_masks);
        if ( this.masks !== null )
            arr["masksProperties"] = value_to_lottie(this.masks);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new NullLayer();
        if ( arr["ddd"] !== undefined )
            obj.threedimensional = value_from_lottie(Boolean(arr["ddd"]));
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["parent"] !== undefined )
            obj.parent = value_from_lottie(arr["parent"]);
        if ( arr["sr"] !== undefined )
            obj.stretch = value_from_lottie(arr["sr"]);
        if ( arr["ks"] !== undefined )
            obj.transform = value_from_lottie(arr["ks"]);
        if ( arr["ao"] !== undefined )
            obj.auto_orient = value_from_lottie(Boolean(arr["ao"]));
        if ( arr["ip"] !== undefined )
            obj.in_point = value_from_lottie(arr["ip"]);
        if ( arr["op"] !== undefined )
            obj.out_point = value_from_lottie(arr["op"]);
        if ( arr["st"] !== undefined )
            obj.start_time = value_from_lottie(arr["st"]);
        if ( arr["bm"] !== undefined )
            obj.blend_mode = value_from_lottie(arr["bm"]);
        if ( arr["tt"] !== undefined )
            obj.matte_mode = value_from_lottie(arr["tt"]);
        if ( arr["ind"] !== undefined )
            obj.index = value_from_lottie(arr["ind"]);
        if ( arr["hasMask"] !== undefined )
            obj.has_masks = value_from_lottie(arr["hasMask"]);
        if ( arr["masksProperties"] !== undefined )
            obj.masks = value_from_lottie(arr["masksProperties"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        return obj;
    }
}

/*
*/
export class PreCompLayer extends Layer
{
    threedimensional;
    hidden;
    type;
    name;
    parent;
    stretch;
    transform;
    auto_orient;
    in_point;
    out_point;
    start_time;
    blend_mode;
    matte_mode;
    index;
    has_masks;
    masks;
    effects;
    reference_id;
    time_remapping;
    width;
    height;

    constructor()
    {
        super();
        this.threedimensional = false;
        this.hidden = null;
        this.type = null;
        this.name = null;
        this.parent = null;
        this.stretch = 1;
        this.transform = new Transform();
        this.auto_orient = false;
        this.in_point = null;
        this.out_point = null;
        this.start_time = 0;
        this.blend_mode = BlendMode.Normal;
        this.matte_mode = null;
        this.index = null;
        this.has_masks = null;
        this.masks = null;
        this.effects = null;
        this.reference_id = '';
        this.time_remapping = null;
        this.width = 512;
        this.height = 512;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.threedimensional !== null )
            arr["ddd"] = value_to_lottie(Number(this.threedimensional));
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.parent !== null )
            arr["parent"] = value_to_lottie(this.parent);
        if ( this.stretch !== null )
            arr["sr"] = value_to_lottie(this.stretch);
        if ( this.transform !== null )
            arr["ks"] = value_to_lottie(this.transform);
        if ( this.auto_orient !== null )
            arr["ao"] = value_to_lottie(Number(this.auto_orient));
        if ( this.in_point !== null )
            arr["ip"] = value_to_lottie(this.in_point);
        if ( this.out_point !== null )
            arr["op"] = value_to_lottie(this.out_point);
        if ( this.start_time !== null )
            arr["st"] = value_to_lottie(this.start_time);
        if ( this.blend_mode !== null )
            arr["bm"] = value_to_lottie(this.blend_mode);
        if ( this.matte_mode !== null )
            arr["tt"] = value_to_lottie(this.matte_mode);
        if ( this.index !== null )
            arr["ind"] = value_to_lottie(this.index);
        if ( this.has_masks !== null )
            arr["hasMask"] = value_to_lottie(this.has_masks);
        if ( this.masks !== null )
            arr["masksProperties"] = value_to_lottie(this.masks);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        if ( this.reference_id !== null )
            arr["refId"] = value_to_lottie(this.reference_id);
        if ( this.time_remapping !== null )
            arr["tm"] = value_to_lottie(this.time_remapping);
        if ( this.width !== null )
            arr["w"] = value_to_lottie(this.width);
        if ( this.height !== null )
            arr["h"] = value_to_lottie(this.height);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new PreCompLayer();
        if ( arr["ddd"] !== undefined )
            obj.threedimensional = value_from_lottie(Boolean(arr["ddd"]));
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["parent"] !== undefined )
            obj.parent = value_from_lottie(arr["parent"]);
        if ( arr["sr"] !== undefined )
            obj.stretch = value_from_lottie(arr["sr"]);
        if ( arr["ks"] !== undefined )
            obj.transform = value_from_lottie(arr["ks"]);
        if ( arr["ao"] !== undefined )
            obj.auto_orient = value_from_lottie(Boolean(arr["ao"]));
        if ( arr["ip"] !== undefined )
            obj.in_point = value_from_lottie(arr["ip"]);
        if ( arr["op"] !== undefined )
            obj.out_point = value_from_lottie(arr["op"]);
        if ( arr["st"] !== undefined )
            obj.start_time = value_from_lottie(arr["st"]);
        if ( arr["bm"] !== undefined )
            obj.blend_mode = value_from_lottie(arr["bm"]);
        if ( arr["tt"] !== undefined )
            obj.matte_mode = value_from_lottie(arr["tt"]);
        if ( arr["ind"] !== undefined )
            obj.index = value_from_lottie(arr["ind"]);
        if ( arr["hasMask"] !== undefined )
            obj.has_masks = value_from_lottie(arr["hasMask"]);
        if ( arr["masksProperties"] !== undefined )
            obj.masks = value_from_lottie(arr["masksProperties"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        if ( arr["refId"] !== undefined )
            obj.reference_id = value_from_lottie(arr["refId"]);
        if ( arr["tm"] !== undefined )
            obj.time_remapping = value_from_lottie(arr["tm"]);
        if ( arr["w"] !== undefined )
            obj.width = value_from_lottie(arr["w"]);
        if ( arr["h"] !== undefined )
            obj.height = value_from_lottie(arr["h"]);
        return obj;
    }
}

/*!
    Layer containing ShapeElement objects
*/
export class ShapeLayer extends Layer
{
    threedimensional;
    hidden;
    type;
    name;
    parent;
    stretch;
    transform;
    auto_orient;
    in_point;
    out_point;
    start_time;
    blend_mode;
    matte_mode;
    index;
    has_masks;
    masks;
    effects;
    shapes;

    constructor()
    {
        super();
        this.type = 4;
        this.threedimensional = false;
        this.hidden = null;
        this.name = null;
        this.parent = null;
        this.stretch = 1;
        this.transform = new Transform();
        this.auto_orient = false;
        this.in_point = null;
        this.out_point = null;
        this.start_time = 0;
        this.blend_mode = BlendMode.Normal;
        this.matte_mode = null;
        this.index = null;
        this.has_masks = null;
        this.masks = null;
        this.effects = null;
        this.shapes = [];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.threedimensional !== null )
            arr["ddd"] = value_to_lottie(Number(this.threedimensional));
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.parent !== null )
            arr["parent"] = value_to_lottie(this.parent);
        if ( this.stretch !== null )
            arr["sr"] = value_to_lottie(this.stretch);
        if ( this.transform !== null )
            arr["ks"] = value_to_lottie(this.transform);
        if ( this.auto_orient !== null )
            arr["ao"] = value_to_lottie(Number(this.auto_orient));
        if ( this.in_point !== null )
            arr["ip"] = value_to_lottie(this.in_point);
        if ( this.out_point !== null )
            arr["op"] = value_to_lottie(this.out_point);
        if ( this.start_time !== null )
            arr["st"] = value_to_lottie(this.start_time);
        if ( this.blend_mode !== null )
            arr["bm"] = value_to_lottie(this.blend_mode);
        if ( this.matte_mode !== null )
            arr["tt"] = value_to_lottie(this.matte_mode);
        if ( this.index !== null )
            arr["ind"] = value_to_lottie(this.index);
        if ( this.has_masks !== null )
            arr["hasMask"] = value_to_lottie(this.has_masks);
        if ( this.masks !== null )
            arr["masksProperties"] = value_to_lottie(this.masks);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        if ( this.shapes !== null )
            arr["shapes"] = value_to_lottie(this.shapes);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new ShapeLayer();
        if ( arr["ddd"] !== undefined )
            obj.threedimensional = value_from_lottie(Boolean(arr["ddd"]));
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["parent"] !== undefined )
            obj.parent = value_from_lottie(arr["parent"]);
        if ( arr["sr"] !== undefined )
            obj.stretch = value_from_lottie(arr["sr"]);
        if ( arr["ks"] !== undefined )
            obj.transform = value_from_lottie(arr["ks"]);
        if ( arr["ao"] !== undefined )
            obj.auto_orient = value_from_lottie(Boolean(arr["ao"]));
        if ( arr["ip"] !== undefined )
            obj.in_point = value_from_lottie(arr["ip"]);
        if ( arr["op"] !== undefined )
            obj.out_point = value_from_lottie(arr["op"]);
        if ( arr["st"] !== undefined )
            obj.start_time = value_from_lottie(arr["st"]);
        if ( arr["bm"] !== undefined )
            obj.blend_mode = value_from_lottie(arr["bm"]);
        if ( arr["tt"] !== undefined )
            obj.matte_mode = value_from_lottie(arr["tt"]);
        if ( arr["ind"] !== undefined )
            obj.index = value_from_lottie(arr["ind"]);
        if ( arr["hasMask"] !== undefined )
            obj.has_masks = value_from_lottie(arr["hasMask"]);
        if ( arr["masksProperties"] !== undefined )
            obj.masks = value_from_lottie(arr["masksProperties"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        if ( arr["shapes"] !== undefined )
            obj.shapes = value_from_lottie(arr["shapes"]);
        return obj;
    }
}

/*!
    Layer with a solid color rectangle
*/
export class SolidColorLayer extends Layer
{
    threedimensional;
    hidden;
    type;
    name;
    parent;
    stretch;
    transform;
    auto_orient;
    in_point;
    out_point;
    start_time;
    blend_mode;
    matte_mode;
    index;
    has_masks;
    masks;
    effects;
    color;
    height;
    width;

    constructor()
    {
        super();
        this.type = 1;
        this.threedimensional = false;
        this.hidden = null;
        this.name = null;
        this.parent = null;
        this.stretch = 1;
        this.transform = new Transform();
        this.auto_orient = false;
        this.in_point = null;
        this.out_point = null;
        this.start_time = 0;
        this.blend_mode = BlendMode.Normal;
        this.matte_mode = null;
        this.index = null;
        this.has_masks = null;
        this.masks = null;
        this.effects = null;
        this.color = '';
        this.height = 0;
        this.width = 0;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.threedimensional !== null )
            arr["ddd"] = value_to_lottie(Number(this.threedimensional));
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.parent !== null )
            arr["parent"] = value_to_lottie(this.parent);
        if ( this.stretch !== null )
            arr["sr"] = value_to_lottie(this.stretch);
        if ( this.transform !== null )
            arr["ks"] = value_to_lottie(this.transform);
        if ( this.auto_orient !== null )
            arr["ao"] = value_to_lottie(Number(this.auto_orient));
        if ( this.in_point !== null )
            arr["ip"] = value_to_lottie(this.in_point);
        if ( this.out_point !== null )
            arr["op"] = value_to_lottie(this.out_point);
        if ( this.start_time !== null )
            arr["st"] = value_to_lottie(this.start_time);
        if ( this.blend_mode !== null )
            arr["bm"] = value_to_lottie(this.blend_mode);
        if ( this.matte_mode !== null )
            arr["tt"] = value_to_lottie(this.matte_mode);
        if ( this.index !== null )
            arr["ind"] = value_to_lottie(this.index);
        if ( this.has_masks !== null )
            arr["hasMask"] = value_to_lottie(this.has_masks);
        if ( this.masks !== null )
            arr["masksProperties"] = value_to_lottie(this.masks);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        if ( this.color !== null )
            arr["sc"] = value_to_lottie(this.color);
        if ( this.height !== null )
            arr["sh"] = value_to_lottie(this.height);
        if ( this.width !== null )
            arr["sw"] = value_to_lottie(this.width);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new SolidColorLayer();
        if ( arr["ddd"] !== undefined )
            obj.threedimensional = value_from_lottie(Boolean(arr["ddd"]));
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["parent"] !== undefined )
            obj.parent = value_from_lottie(arr["parent"]);
        if ( arr["sr"] !== undefined )
            obj.stretch = value_from_lottie(arr["sr"]);
        if ( arr["ks"] !== undefined )
            obj.transform = value_from_lottie(arr["ks"]);
        if ( arr["ao"] !== undefined )
            obj.auto_orient = value_from_lottie(Boolean(arr["ao"]));
        if ( arr["ip"] !== undefined )
            obj.in_point = value_from_lottie(arr["ip"]);
        if ( arr["op"] !== undefined )
            obj.out_point = value_from_lottie(arr["op"]);
        if ( arr["st"] !== undefined )
            obj.start_time = value_from_lottie(arr["st"]);
        if ( arr["bm"] !== undefined )
            obj.blend_mode = value_from_lottie(arr["bm"]);
        if ( arr["tt"] !== undefined )
            obj.matte_mode = value_from_lottie(arr["tt"]);
        if ( arr["ind"] !== undefined )
            obj.index = value_from_lottie(arr["ind"]);
        if ( arr["hasMask"] !== undefined )
            obj.has_masks = value_from_lottie(arr["hasMask"]);
        if ( arr["masksProperties"] !== undefined )
            obj.masks = value_from_lottie(arr["masksProperties"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        if ( arr["sc"] !== undefined )
            obj.color = value_from_lottie(arr["sc"]);
        if ( arr["sh"] !== undefined )
            obj.height = value_from_lottie(arr["sh"]);
        if ( arr["sw"] !== undefined )
            obj.width = value_from_lottie(arr["sw"]);
        return obj;
    }
}

/*
*/
export class TextLayer extends Layer
{
    threedimensional;
    hidden;
    type;
    name;
    parent;
    stretch;
    transform;
    auto_orient;
    in_point;
    out_point;
    start_time;
    blend_mode;
    matte_mode;
    index;
    has_masks;
    masks;
    effects;
    data;

    constructor()
    {
        super();
        this.type = 5;
        this.threedimensional = false;
        this.hidden = null;
        this.name = null;
        this.parent = null;
        this.stretch = 1;
        this.transform = new Transform();
        this.auto_orient = false;
        this.in_point = null;
        this.out_point = null;
        this.start_time = 0;
        this.blend_mode = BlendMode.Normal;
        this.matte_mode = null;
        this.index = null;
        this.has_masks = null;
        this.masks = null;
        this.effects = null;
        this.data = new TextAnimatorData();
    }

    to_lottie()
    {
        var arr = {};
        if ( this.threedimensional !== null )
            arr["ddd"] = value_to_lottie(Number(this.threedimensional));
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.parent !== null )
            arr["parent"] = value_to_lottie(this.parent);
        if ( this.stretch !== null )
            arr["sr"] = value_to_lottie(this.stretch);
        if ( this.transform !== null )
            arr["ks"] = value_to_lottie(this.transform);
        if ( this.auto_orient !== null )
            arr["ao"] = value_to_lottie(Number(this.auto_orient));
        if ( this.in_point !== null )
            arr["ip"] = value_to_lottie(this.in_point);
        if ( this.out_point !== null )
            arr["op"] = value_to_lottie(this.out_point);
        if ( this.start_time !== null )
            arr["st"] = value_to_lottie(this.start_time);
        if ( this.blend_mode !== null )
            arr["bm"] = value_to_lottie(this.blend_mode);
        if ( this.matte_mode !== null )
            arr["tt"] = value_to_lottie(this.matte_mode);
        if ( this.index !== null )
            arr["ind"] = value_to_lottie(this.index);
        if ( this.has_masks !== null )
            arr["hasMask"] = value_to_lottie(this.has_masks);
        if ( this.masks !== null )
            arr["masksProperties"] = value_to_lottie(this.masks);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        if ( this.data !== null )
            arr["t"] = value_to_lottie(this.data);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new TextLayer();
        if ( arr["ddd"] !== undefined )
            obj.threedimensional = value_from_lottie(Boolean(arr["ddd"]));
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["parent"] !== undefined )
            obj.parent = value_from_lottie(arr["parent"]);
        if ( arr["sr"] !== undefined )
            obj.stretch = value_from_lottie(arr["sr"]);
        if ( arr["ks"] !== undefined )
            obj.transform = value_from_lottie(arr["ks"]);
        if ( arr["ao"] !== undefined )
            obj.auto_orient = value_from_lottie(Boolean(arr["ao"]));
        if ( arr["ip"] !== undefined )
            obj.in_point = value_from_lottie(arr["ip"]);
        if ( arr["op"] !== undefined )
            obj.out_point = value_from_lottie(arr["op"]);
        if ( arr["st"] !== undefined )
            obj.start_time = value_from_lottie(arr["st"]);
        if ( arr["bm"] !== undefined )
            obj.blend_mode = value_from_lottie(arr["bm"]);
        if ( arr["tt"] !== undefined )
            obj.matte_mode = value_from_lottie(arr["tt"]);
        if ( arr["ind"] !== undefined )
            obj.index = value_from_lottie(arr["ind"]);
        if ( arr["hasMask"] !== undefined )
            obj.has_masks = value_from_lottie(arr["hasMask"]);
        if ( arr["masksProperties"] !== undefined )
            obj.masks = value_from_lottie(arr["masksProperties"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        if ( arr["t"] !== undefined )
            obj.data = value_from_lottie(arr["t"]);
        return obj;
    }
}

/*
*/
export class ImageLayer extends Layer
{
    threedimensional;
    hidden;
    type;
    name;
    parent;
    stretch;
    transform;
    auto_orient;
    in_point;
    out_point;
    start_time;
    blend_mode;
    matte_mode;
    index;
    has_masks;
    masks;
    effects;
    image_id;

    constructor()
    {
        super();
        this.type = 2;
        this.threedimensional = false;
        this.hidden = null;
        this.name = null;
        this.parent = null;
        this.stretch = 1;
        this.transform = new Transform();
        this.auto_orient = false;
        this.in_point = null;
        this.out_point = null;
        this.start_time = 0;
        this.blend_mode = BlendMode.Normal;
        this.matte_mode = null;
        this.index = null;
        this.has_masks = null;
        this.masks = null;
        this.effects = null;
        this.image_id = '';
    }

    to_lottie()
    {
        var arr = {};
        if ( this.threedimensional !== null )
            arr["ddd"] = value_to_lottie(Number(this.threedimensional));
        if ( this.hidden !== null )
            arr["hd"] = value_to_lottie(this.hidden);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.parent !== null )
            arr["parent"] = value_to_lottie(this.parent);
        if ( this.stretch !== null )
            arr["sr"] = value_to_lottie(this.stretch);
        if ( this.transform !== null )
            arr["ks"] = value_to_lottie(this.transform);
        if ( this.auto_orient !== null )
            arr["ao"] = value_to_lottie(Number(this.auto_orient));
        if ( this.in_point !== null )
            arr["ip"] = value_to_lottie(this.in_point);
        if ( this.out_point !== null )
            arr["op"] = value_to_lottie(this.out_point);
        if ( this.start_time !== null )
            arr["st"] = value_to_lottie(this.start_time);
        if ( this.blend_mode !== null )
            arr["bm"] = value_to_lottie(this.blend_mode);
        if ( this.matte_mode !== null )
            arr["tt"] = value_to_lottie(this.matte_mode);
        if ( this.index !== null )
            arr["ind"] = value_to_lottie(this.index);
        if ( this.has_masks !== null )
            arr["hasMask"] = value_to_lottie(this.has_masks);
        if ( this.masks !== null )
            arr["masksProperties"] = value_to_lottie(this.masks);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        if ( this.image_id !== null )
            arr["refId"] = value_to_lottie(this.image_id);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new ImageLayer();
        if ( arr["ddd"] !== undefined )
            obj.threedimensional = value_from_lottie(Boolean(arr["ddd"]));
        if ( arr["hd"] !== undefined )
            obj.hidden = value_from_lottie(arr["hd"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["parent"] !== undefined )
            obj.parent = value_from_lottie(arr["parent"]);
        if ( arr["sr"] !== undefined )
            obj.stretch = value_from_lottie(arr["sr"]);
        if ( arr["ks"] !== undefined )
            obj.transform = value_from_lottie(arr["ks"]);
        if ( arr["ao"] !== undefined )
            obj.auto_orient = value_from_lottie(Boolean(arr["ao"]));
        if ( arr["ip"] !== undefined )
            obj.in_point = value_from_lottie(arr["ip"]);
        if ( arr["op"] !== undefined )
            obj.out_point = value_from_lottie(arr["op"]);
        if ( arr["st"] !== undefined )
            obj.start_time = value_from_lottie(arr["st"]);
        if ( arr["bm"] !== undefined )
            obj.blend_mode = value_from_lottie(arr["bm"]);
        if ( arr["tt"] !== undefined )
            obj.matte_mode = value_from_lottie(arr["tt"]);
        if ( arr["ind"] !== undefined )
            obj.index = value_from_lottie(arr["ind"]);
        if ( arr["hasMask"] !== undefined )
            obj.has_masks = value_from_lottie(arr["hasMask"]);
        if ( arr["masksProperties"] !== undefined )
            obj.masks = value_from_lottie(arr["masksProperties"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        if ( arr["refId"] !== undefined )
            obj.image_id = value_from_lottie(arr["refId"]);
        return obj;
    }
}

