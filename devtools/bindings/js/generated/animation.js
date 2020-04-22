import { value_to_lottie, value_from_lottie, LottieObject } from '../base.js';
import { Chars, Asset } from './assets.js';
import { FontList } from './text.js';
import { Layer } from './layers.js';

/*!
    Top level object, describing the animation

    @see http://docs.aenhancers.com/items/compitem/
    @todo rename to Composition?
*/
export class Animation extends LottieObject
{
    tgs;
    version;
    frame_rate;
    in_point;
    out_point;
    width;
    height;
    name;
    threedimensional;
    assets;
    fonts;
    layers;
    chars;

    constructor()
    {
        super();
        this.tgs = 1;
        this.version = '5.5.2';
        this.frame_rate = 60;
        this.in_point = 0;
        this.out_point = 60;
        this.width = 512;
        this.height = 512;
        this.name = null;
        this.threedimensional = false;
        this.assets = [];
        this.fonts = null;
        this.layers = [];
        this.chars = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.tgs !== null )
            arr["tgs"] = value_to_lottie(Number(this.tgs));
        if ( this.version !== null )
            arr["v"] = value_to_lottie(this.version);
        if ( this.frame_rate !== null )
            arr["fr"] = value_to_lottie(this.frame_rate);
        if ( this.in_point !== null )
            arr["ip"] = value_to_lottie(this.in_point);
        if ( this.out_point !== null )
            arr["op"] = value_to_lottie(this.out_point);
        if ( this.width !== null )
            arr["w"] = value_to_lottie(this.width);
        if ( this.height !== null )
            arr["h"] = value_to_lottie(this.height);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.threedimensional !== null )
            arr["ddd"] = value_to_lottie(Number(this.threedimensional));
        if ( this.assets !== null )
            arr["assets"] = value_to_lottie(this.assets);
        if ( this.fonts !== null )
            arr["fonts"] = value_to_lottie(this.fonts);
        if ( this.layers !== null )
            arr["layers"] = value_to_lottie(this.layers);
        if ( this.chars !== null )
            arr["chars"] = value_to_lottie(this.chars);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Animation();
        if ( arr["tgs"] !== undefined )
            obj.tgs = value_from_lottie(Boolean(arr["tgs"]));
        if ( arr["v"] !== undefined )
            obj.version = value_from_lottie(arr["v"]);
        if ( arr["fr"] !== undefined )
            obj.frame_rate = value_from_lottie(arr["fr"]);
        if ( arr["ip"] !== undefined )
            obj.in_point = value_from_lottie(arr["ip"]);
        if ( arr["op"] !== undefined )
            obj.out_point = value_from_lottie(arr["op"]);
        if ( arr["w"] !== undefined )
            obj.width = value_from_lottie(arr["w"]);
        if ( arr["h"] !== undefined )
            obj.height = value_from_lottie(arr["h"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ddd"] !== undefined )
            obj.threedimensional = value_from_lottie(Boolean(arr["ddd"]));
        if ( arr["assets"] !== undefined )
            obj.assets = value_from_lottie(arr["assets"]);
        if ( arr["fonts"] !== undefined )
            obj.fonts = value_from_lottie(arr["fonts"]);
        if ( arr["layers"] !== undefined )
            obj.layers = value_from_lottie(arr["layers"]);
        if ( arr["chars"] !== undefined )
            obj.chars = value_from_lottie(arr["chars"]);
        return obj;
    }
}

