export class Vector
{
    constructor(...components)
    {
        if ( this.constructor._size && components.length == 0 )
            this.components = new Float32Array(this.constructor._size)
        else
            this.components = Float32Array.from(components);
    }

    length()
    {
        return Math.hypot(...this.components);
    }

    length_squared()
    {
        return this.components.reduce((a, b) => a*a + b*b);
    }

    normalize()
    {
        var len = this.length();
        this.components.forEach((v, i, arr) => arr[i] /= len);
        return this;
    }

    flip()
    {
        this.components.forEach((v, i, arr) => arr[i] = -v);
        return this;
    }

    subtract(other)
    {
        this.components.forEach((v, i, arr) => arr[i] -= other.components[i]);
        return this;
    }

    add(other)
    {
        this.components.forEach((v, i, arr) => arr[i] += other.components[i]);
        return this;
    }

    divide(scalar)
    {
        this.components.forEach((v, i, arr) => arr[i] /= scalar);
        return this;
    }

    multiply(scalar)
    {
        this.components.forEach((v, i, arr) => arr[i] *= scalar);
        return this;
    }

    clone()
    {
        return new this.constructor(...this.components);
    }

    static define_named_component(name, index)
    {
        Object.defineProperty(this.prototype, name, {
            configurable: false,
            enumerable: false,
            get: function(){return this.components[index];},
            set: function(v){return this.components[index] = v;},
        });
    }

    static define_size(size)
    {
        this._size = size;
    }

    dot(other)
    {
        return (
            this.components
            .map((v, i) => v * other.components[i])
            .reduce((a, b) => a+b)
        );
    }

    lerp(other, factor)
    {
        return this.multiply(1-factor).add(other.clone().multiply(factor));
    }
}

