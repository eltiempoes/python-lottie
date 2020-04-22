import { value_to_lottie, value_from_lottie, LottieObject } from '../base.js';

/*!
    Bezier handle for keyframe interpolation
*/
export class KeyframeBezierHandle extends LottieObject
{
    x;
    y;

    constructor()
    {
        super();
        this.x = 0;
        this.y = 0;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.x !== null )
            arr["x"] = value_to_lottie([this.x]);
        if ( this.y !== null )
            arr["y"] = value_to_lottie([this.y]);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new KeyframeBezierHandle();
        if ( arr["x"] !== undefined )
            obj.x = value_from_lottie(arr["x"][0]);
        if ( arr["y"] !== undefined )
            obj.y = value_from_lottie(arr["y"][0]);
        return obj;
    }
}

