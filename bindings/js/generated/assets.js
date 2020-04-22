import { value_to_lottie, value_from_lottie, LottieObject } from '../base.js';
import { Layer } from './layers.js';
import { ShapeElement } from './shapes.js';

/*
*/
export class Asset extends LottieObject
{

    constructor()
    {
        super();
    }

    to_lottie()
    {
        var arr = {};
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Asset();
        return obj;
    }
}

/*!
    Character shapes
*/
export class CharacterData extends LottieObject
{
    shapes;

    constructor()
    {
        super();
        this.shapes = [];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.shapes !== null )
            arr["shapes"] = value_to_lottie(this.shapes);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new CharacterData();
        if ( arr["shapes"] !== undefined )
            obj.shapes = value_from_lottie(arr["shapes"]);
        return obj;
    }
}

/*!
    Defines character shapes to avoid loading system fonts
*/
export class Chars extends LottieObject
{
    character;
    font_family;
    font_size;
    font_style;
    width;
    data;

    constructor()
    {
        super();
        this.character = '';
        this.font_family = '';
        this.font_size = 0;
        this.font_style = '';
        this.width = 0;
        this.data = new CharacterData();
    }

    to_lottie()
    {
        var arr = {};
        if ( this.character !== null )
            arr["ch"] = value_to_lottie(this.character);
        if ( this.font_family !== null )
            arr["fFamily"] = value_to_lottie(this.font_family);
        if ( this.font_size !== null )
            arr["size"] = value_to_lottie(this.font_size);
        if ( this.font_style !== null )
            arr["style"] = value_to_lottie(this.font_style);
        if ( this.width !== null )
            arr["w"] = value_to_lottie(this.width);
        if ( this.data !== null )
            arr["data"] = value_to_lottie(this.data);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Chars();
        if ( arr["ch"] !== undefined )
            obj.character = value_from_lottie(arr["ch"]);
        if ( arr["fFamily"] !== undefined )
            obj.font_family = value_from_lottie(arr["fFamily"]);
        if ( arr["size"] !== undefined )
            obj.font_size = value_from_lottie(arr["size"]);
        if ( arr["style"] !== undefined )
            obj.font_style = value_from_lottie(arr["style"]);
        if ( arr["w"] !== undefined )
            obj.width = value_from_lottie(arr["w"]);
        if ( arr["data"] !== undefined )
            obj.data = value_from_lottie(arr["data"]);
        return obj;
    }
}

/*!
        External image

        \see http://docs.aenhancers.com/sources/filesource/
*/
export class Image extends Asset
{
    height;
    width;
    id;
    image;
    image_path;
    embedded;

    constructor()
    {
        super();
        this.height = 0;
        this.width = 0;
        this.id = '';
        this.image = '';
        this.image_path = '';
        this.embedded = false;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.height !== null )
            arr["h"] = value_to_lottie(this.height);
        if ( this.width !== null )
            arr["w"] = value_to_lottie(this.width);
        if ( this.id !== null )
            arr["id"] = value_to_lottie(this.id);
        if ( this.image !== null )
            arr["p"] = value_to_lottie(this.image);
        if ( this.image_path !== null )
            arr["u"] = value_to_lottie(this.image_path);
        if ( this.embedded !== null )
            arr["e"] = value_to_lottie(Number(this.embedded));
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Image();
        if ( arr["h"] !== undefined )
            obj.height = value_from_lottie(arr["h"]);
        if ( arr["w"] !== undefined )
            obj.width = value_from_lottie(arr["w"]);
        if ( arr["id"] !== undefined )
            obj.id = value_from_lottie(arr["id"]);
        if ( arr["p"] !== undefined )
            obj.image = value_from_lottie(arr["p"]);
        if ( arr["u"] !== undefined )
            obj.image_path = value_from_lottie(arr["u"]);
        if ( arr["e"] !== undefined )
            obj.embedded = value_from_lottie(Boolean(arr["e"]));
        return obj;
    }
}

/*
*/
export class Precomp extends Asset
{
    id;
    layers;

    constructor()
    {
        super();
        this.id = '';
        this.layers = [];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.id !== null )
            arr["id"] = value_to_lottie(this.id);
        if ( this.layers !== null )
            arr["layers"] = value_to_lottie(this.layers);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Precomp();
        if ( arr["id"] !== undefined )
            obj.id = value_from_lottie(arr["id"]);
        if ( arr["layers"] !== undefined )
            obj.layers = value_from_lottie(arr["layers"]);
        return obj;
    }
}

