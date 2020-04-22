import { value_to_lottie, value_from_lottie, LottieObject } from '../base.js';

/*!
    Single bezier curve
*/
export class Bezier extends LottieObject
{
    closed;
    in_tangents;
    out_tangents;
    vertices;

    constructor()
    {
        super();
        this.closed = false;
        this.in_tangents = [];
        this.out_tangents = [];
        this.vertices = [];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.closed !== null )
            arr["c"] = value_to_lottie(this.closed);
        if ( this.in_tangents !== null )
            arr["i"] = value_to_lottie(this.in_tangents);
        if ( this.out_tangents !== null )
            arr["o"] = value_to_lottie(this.out_tangents);
        if ( this.vertices !== null )
            arr["v"] = value_to_lottie(this.vertices);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Bezier();
        if ( arr["c"] !== undefined )
            obj.closed = value_from_lottie(arr["c"]);
        if ( arr["i"] !== undefined )
            obj.in_tangents = value_from_lottie(arr["i"]);
        if ( arr["o"] !== undefined )
            obj.out_tangents = value_from_lottie(arr["o"]);
        if ( arr["v"] !== undefined )
            obj.vertices = value_from_lottie(arr["v"]);
        return obj;
    }
}

