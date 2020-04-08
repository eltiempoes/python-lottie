import { Vector } from './vector.js'

export class TgsObject
{
    to_lottie()
    {
        return {};
    }
}

export function value_from_lottie(x)
{
    return x;
}

export function value_to_lottie(x)
{
    if ( x instanceof TgsObject )
        return x.to_lottie();
    if ( x instanceof Array )
        return x.map(value_to_lottie);
    if ( x instanceof Vector )
        return x.components;
    return x;
}
