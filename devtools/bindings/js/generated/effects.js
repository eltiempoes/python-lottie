import { value_to_lottie, value_from_lottie, LottieObject } from '../base.js';
import { Value, MultiDimensional } from './properties.js';

/*!
    Value for an effect
*/
export class EffectValue extends LottieObject
{
    effect_index;
    name;
    type;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new EffectValue();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        return obj;
    }
}

/*
*/
export class EffectValueAngle extends EffectValue
{
    effect_index;
    name;
    type;
    value;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.value = new Value(0);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.value !== null )
            arr["v"] = value_to_lottie(this.value);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new EffectValueAngle();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["v"] !== undefined )
            obj.value = value_from_lottie(arr["v"]);
        return obj;
    }
}

/*
*/
export class EffectValueCheckbox extends EffectValue
{
    effect_index;
    name;
    type;
    value;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.value = new Value(0);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.value !== null )
            arr["v"] = value_to_lottie(this.value);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new EffectValueCheckbox();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["v"] !== undefined )
            obj.value = value_from_lottie(arr["v"]);
        return obj;
    }
}

/*
*/
export class EffectValueColor extends EffectValue
{
    effect_index;
    name;
    type;
    value;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.value = new MultiDimensional([0, 0, 0]);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.value !== null )
            arr["v"] = value_to_lottie(this.value);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new EffectValueColor();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["v"] !== undefined )
            obj.value = value_from_lottie(arr["v"]);
        return obj;
    }
}

/*
*/
export class EffectValueDropDown extends EffectValue
{
    effect_index;
    name;
    type;
    value;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.value = new Value(0);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.value !== null )
            arr["v"] = value_to_lottie(this.value);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new EffectValueDropDown();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["v"] !== undefined )
            obj.value = value_from_lottie(arr["v"]);
        return obj;
    }
}

/*
*/
export class EffectValueLayer extends EffectValue
{
    effect_index;
    name;
    type;
    value;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.value = new Value(0);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.value !== null )
            arr["v"] = value_to_lottie(this.value);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new EffectValueLayer();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["v"] !== undefined )
            obj.value = value_from_lottie(arr["v"]);
        return obj;
    }
}

/*
*/
export class EffectValuePoint extends EffectValue
{
    effect_index;
    name;
    type;
    value;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.value = new MultiDimensional([0, 0]);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.value !== null )
            arr["v"] = value_to_lottie(this.value);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new EffectValuePoint();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["v"] !== undefined )
            obj.value = value_from_lottie(arr["v"]);
        return obj;
    }
}

/*
*/
export class EffectValueSlider extends EffectValue
{
    effect_index;
    name;
    type;
    value;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.value = new Value(0);
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.value !== null )
            arr["v"] = value_to_lottie(this.value);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new EffectValueSlider();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["v"] !== undefined )
            obj.value = value_from_lottie(arr["v"]);
        return obj;
    }
}

/*!
    Layer effect
*/
export class Effect extends LottieObject
{
    effect_index;
    name;
    type;
    effects;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.effects = [];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Effect();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        return obj;
    }
}

/*
*/
export class EffectNoValue extends EffectValue
{
    effect_index;
    name;
    type;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new EffectNoValue();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        return obj;
    }
}

/*!
    Replaces the whole layer with the given color
    @note Opacity is in [0, 1]
*/
export class FillEffect extends Effect
{
    effect_index;
    name;
    type;
    effects;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.effects = [new EffectValuePoint(), new EffectValueDropDown(), new EffectValueColor(), new EffectValueDropDown(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider()];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new FillEffect();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        return obj;
    }
}

/*!
    Gaussian blur
*/
export class GaussianBlurEffect extends Effect
{
    effect_index;
    name;
    type;
    effects;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.effects = [new EffectValueSlider(), new EffectValueSlider(), new EffectValueCheckbox()];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new GaussianBlurEffect();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        return obj;
    }
}

/*
*/
export class Matte3Effect extends Effect
{
    effect_index;
    name;
    type;
    effects;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.effects = [new EffectValueSlider()];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new Matte3Effect();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        return obj;
    }
}

/*
*/
export class ProLevelsEffect extends Effect
{
    effect_index;
    name;
    type;
    effects;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.effects = [new EffectValueDropDown(), new EffectNoValue(), new EffectNoValue(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectNoValue(), new EffectNoValue(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectNoValue(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectNoValue(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectNoValue(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectNoValue()];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new ProLevelsEffect();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        return obj;
    }
}

/*
*/
export class StrokeEffect extends Effect
{
    effect_index;
    name;
    type;
    effects;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.effects = [new EffectValueColor(), new EffectValueCheckbox(), new EffectValueCheckbox(), new EffectValueColor(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueDropDown(), new EffectValueDropDown()];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new StrokeEffect();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        return obj;
    }
}

/*!
    Colorizes the layer
    @note Opacity is in [0, 100]
*/
export class TintEffect extends Effect
{
    effect_index;
    name;
    type;
    effects;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.effects = [new EffectValueColor(), new EffectValueColor(), new EffectValueSlider()];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new TintEffect();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        return obj;
    }
}

/*!
    Maps layers colors based on bright/mid/dark colors
*/
export class TritoneEffect extends Effect
{
    effect_index;
    name;
    type;
    effects;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.effects = [new EffectValueColor(), new EffectValueColor(), new EffectValueColor()];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new TritoneEffect();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        return obj;
    }
}

/*!
    Gaussian blur
*/
export class ChangeColorEffect extends Effect
{
    effect_index;
    name;
    type;
    effects;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.effects = [new EffectValueDropDown(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueColor(), new EffectValueSlider(), new EffectValueSlider(), new EffectValueDropDown(), new EffectValueDropDown()];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new ChangeColorEffect();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        return obj;
    }
}

/*!
    Adds a shadow to the layer
    @note Opacity is in [0, 255]
*/
export class DropShadowEffect extends Effect
{
    effect_index;
    name;
    type;
    effects;

    constructor()
    {
        super();
        this.effect_index = null;
        this.name = null;
        this.type = null;
        this.effects = [new EffectValueColor(), new EffectValueSlider(), new EffectValueAngle(), new EffectValueSlider(), new EffectValueSlider()];
    }

    to_lottie()
    {
        var arr = {};
        if ( this.effect_index !== null )
            arr["ix"] = value_to_lottie(this.effect_index);
        if ( this.name !== null )
            arr["nm"] = value_to_lottie(this.name);
        if ( this.type !== null )
            arr["ty"] = value_to_lottie(this.type);
        if ( this.effects !== null )
            arr["ef"] = value_to_lottie(this.effects);
        return arr;
    }

    static from_lottie(arr)
    {
        var obj = new DropShadowEffect();
        if ( arr["ix"] !== undefined )
            obj.effect_index = value_from_lottie(arr["ix"]);
        if ( arr["nm"] !== undefined )
            obj.name = value_from_lottie(arr["nm"]);
        if ( arr["ty"] !== undefined )
            obj.type = value_from_lottie(arr["ty"]);
        if ( arr["ef"] !== undefined )
            obj.effects = value_from_lottie(arr["ef"]);
        return obj;
    }
}

