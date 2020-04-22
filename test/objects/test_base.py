from unittest import mock
from ..base import TestCase
from lottie.objects import base
from lottie import NVector
from lottie.objects.shapes import Rect


class TestEnum(base.LottieEnum):
    Foo = 1
    Bar = 2


class TestLottieBase(TestCase):
    def test_unimplemented(self):
        lottie = base.LottieBase()
        self.assertRaises(NotImplementedError, lottie.to_dict)
        self.assertRaises(NotImplementedError, lottie.load, {})

    def test_enum(self):
        self.assertIsInstance(TestEnum.Foo, base.LottieBase)
        self.assertIsInstance(TestEnum.Foo.to_dict(), int)
        self.assertEqual(TestEnum.Foo.to_dict(), 1)
        self.assertEqual(TestEnum.load(2), TestEnum.Bar)


class TestLottieValueConverter(TestCase):
    def test_p2l(self):
        self.assertIsInstance(base.PseudoBool.py_to_lottie(True), int)
        self.assertEqual(base.PseudoBool.py_to_lottie(True), 1)
        self.assertEqual(base.PseudoBool.py_to_lottie(False), 0)

        self.assertIsInstance(base.PseudoBool.lottie_to_py(1), bool)
        self.assertEqual(base.PseudoBool.py_to_lottie(1), True)
        self.assertEqual(base.PseudoBool.py_to_lottie(0), False)

        self.assertEqual(base.PseudoBool.__name__, base.PseudoBool.name)


class TestLottieProp(TestCase):
    def test_get(self):
        prop = base.LottieProp("foo", "f")
        obj = mock.MagicMock()
        self.assertEqual(obj.foo, prop.get(obj))

    def test_set(self):
        prop = base.LottieProp("foo", "f")
        obj = mock.MagicMock()
        prop.set(obj, 123)
        self.assertEqual(obj.foo, 123)

    def test_load_scalar_lottie(self):
        prop = base.LottieProp("foo", "f", TestEnum)
        v = prop._load_scalar(1)
        self.assertIsInstance(v, TestEnum)
        self.assertEqual(v, TestEnum.Foo)

    def test_load_scalar_type_same(self):
        prop = base.LottieProp("foo", "f", mock.MagicMock)
        sv = mock.MagicMock()
        v = prop._load_scalar(sv)
        self.assertIsInstance(v, mock.MagicMock)
        self.assertEqual(v, sv)
        self.assertIs(v, sv)

    def test_load_scalar_type_convert(self):
        prop = base.LottieProp("foo", "f", float)
        v = prop._load_scalar(1)
        self.assertIsInstance(v, float)
        self.assertEqual(v, 1.0)

    def test_load_scalar_converter(self):
        prop = base.LottieProp("foo", "f", base.PseudoBool)
        v = prop._load_scalar(1)
        self.assertIsInstance(v, bool)
        self.assertEqual(v, True)

    def test_load_scalar_nvector(self):
        prop = base.LottieProp("foo", "f", NVector)
        v = prop._load_scalar([1,2,3])
        self.assertIsInstance(v, NVector)
        self.assertEqual(v, NVector(1, 2, 3))

    def test_load_nolist(self):
        prop = base.LottieProp("foo", "f", mock.MagicMock)
        sv = mock.MagicMock()
        v = prop.load(sv)
        self.assertIsInstance(v, mock.MagicMock)
        self.assertEqual(v, sv)
        self.assertIs(v, sv)

    def test_load_pseudolist_scalar(self):
        prop = base.LottieProp("foo", "f", mock.MagicMock, base.PseudoList)
        sv = mock.MagicMock()
        v = prop.load(sv)
        self.assertIsInstance(v, mock.MagicMock)
        self.assertEqual(v, sv)
        self.assertIs(v, sv)

    def test_load_pseudolist_list(self):
        prop = base.LottieProp("foo", "f", mock.MagicMock, base.PseudoList)
        sv = mock.MagicMock()
        v = prop.load([sv])
        self.assertIsInstance(v, mock.MagicMock)
        self.assertEqual(v, sv)
        self.assertIs(v, sv)

    def test_load_list(self):
        prop = base.LottieProp("foo", "f", mock.MagicMock, True)
        sv = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]
        v = prop.load(sv)
        self.assertIsInstance(v, list)
        self.assertEqual(v, sv)

    def test_basic_to_dict_enum(self):
        prop = base.LottieProp("foo", "f", TestEnum)
        v = prop._basic_to_dict(TestEnum.Foo)
        self.assertIsInstance(v, int)
        self.assertEqual(v, 1)

    def test_basic_to_dict_nvector(self):
        prop = base.LottieProp("foo", "f", NVector)
        v = prop._basic_to_dict(NVector(1, 2, 3))
        self.assertIsInstance(v, list)
        self.assertEqual(v, [1, 2, 3])

    def test_basic_to_dict_list(self):
        prop = base.LottieProp("foo", "f", TestEnum)
        v = prop._basic_to_dict([TestEnum.Foo, TestEnum.Bar])
        self.assertIsInstance(v, list)
        self.assertEqual(v, [1, 2])

    def test_basic_to_dict_simple(self):
        prop = base.LottieProp("foo", "f", int)
        v = prop._basic_to_dict(2)
        self.assertIsInstance(v, int)
        self.assertEqual(v, 2)

    def test_basic_to_dict_float_int(self):
        prop = base.LottieProp("foo", "f", float)
        v = prop._basic_to_dict(2.0)
        self.assertIsInstance(v, int)
        self.assertEqual(v, 2)

    # TODO test stripper
    #def test_basic_to_dict_float_round(self):
        #prop = base.LottieProp("foo", "f", float)
        #v = prop._basic_to_dict(0.3333333)
        #self.assertIsInstance(v, float)
        #self.assertEqual(v, 0.333)

    def test_basic_to_dict_unknown(self):
        prop = base.LottieProp("foo", "f", mock.MagicMock)
        self.assertRaises(Exception, prop._basic_to_dict, mock.MagicMock)

    def test_repr(self):
        prop = base.LottieProp("foo", "bar")
        self.assertIn("foo", repr(prop))
        self.assertIn("bar", repr(prop))


class MockObject(base.LottieObject):
    _props = [
        base.LottieProp("foo", "f", None, True),
        base.LottieProp("bar", "b"),
        base.LottieProp("name", "nm", str),
    ]

    def __init__(self, foo=None, bar=None, name=None):
        self.foo = foo
        self.bar = bar
        self.name = name


MockObject._props[0].type = MockObject


class Derived(MockObject):
    _props = [
        base.LottieProp("awoo", "ft", int)
    ]


class TestLottieObject(TestCase):
    def test_to_dict(self):
        obj = MockObject([MockObject([], 456)], 123)
        self.assertDictEqual(obj.to_dict(), {"f": [{"f": [], "b": 456}], "b": 123})

    def test_load(self):
        obj = MockObject.load({"f": [{"f": [], "b": 456}], "b": 123})
        self.assertEqual(obj.bar, 123)
        self.assertEqual(len(obj.foo), 1)
        self.assertEqual(obj.foo[0].bar, 456)
        self.assertEqual(obj.foo[0].foo, [])

    def test_find_list(self):
        obj = MockObject([MockObject([], 456), MockObject([], 789, "foo")], 123)
        self.assertEqual(obj.find("foo").bar, 789)

    def test_find_not_found(self):
        obj = MockObject([MockObject([], 456), MockObject([], 789, "foo")], 123)
        self.assertIsNone(obj.find("bar"))

    def test_find_child(self):
        obj = MockObject([], MockObject([], 789, "foo"))
        self.assertEqual(obj.find("foo").bar, 789)

    def test_inherit_properties(self):
        obj = Derived([], 123)
        obj.awoo = 621
        self.assertDictEqual(obj.to_dict(), {"f": [], "b": 123, "ft": 621})


class MyLottie(base.CustomObject):
    wrapped_lottie = Rect
    _props = [
        base.LottieProp("p1", "p1", NVector),
        base.LottieProp("p2", "p2", NVector),
    ]
    fullname = "%s.%s" % (__name__, "MyLottie")

    def __init__(self, p1=None, p2=None):
        super().__init__()
        self.p1 = p1 or NVector(0, 0)
        self.p2 = p2 or NVector(0, 0)

    def _build_wrapped(self):
        rect = Rect()
        rect.position.value = (self.p1 + self.p2) / 2
        rect.size.value = self.p2 - self.p1
        return rect


class TestCustomObject(TestCase):
    def test_to_dict(self):
        obj = MyLottie(NVector(10, 20), NVector(20, 30))
        obj.refresh()

        self.assertDictEqual(
            obj.to_dict(),
            {
                "ty": "rc",
                "d": 0,
                "p": {"a": 0, "k": [15, 25]},
                "s": {"a": 0, "k": [10, 10]},
                "r": {"a": 0, "k": 0},
                "__pyclass": MyLottie.fullname,
                "p1": [10, 20],
                "p2": [20, 30],
            }
        )

    def test_load(self):
        obj = Rect.load({
            "ty": "rc",
            "d": 0,
            "p": {"a": 0, "k": [15, 25]},
            "s": {"a": 0, "k": [10, 10]},
            "r": {"a": 0, "k": 0},
            "__pyclass": MyLottie.fullname,
            "p1": [10, 20],
            "p2": [20, 30],
        })
        self.assertIsInstance(obj, MyLottie)
        self.assertEqual(obj.p1, NVector(10, 20))
        self.assertEqual(obj.p2, NVector(20, 30))
        self.assertEqual(obj.wrapped.position.value, NVector(15, 25))

    def test_load_norefresh(self):
        dic = {
            "ty": "rc",
            "d": 0,
            "p": {"a": 0, "k": [115, 125]},
            "s": {"a": 0, "k": [110, 110]},
            "r": {"a": 0, "k": 0},
            "__pyclass": MyLottie.fullname,
            "p1": [10, 20],
            "p2": [20, 30],
        }
        obj = Rect.load(dic)
        self.assertDictEqual(obj.to_dict(), dic)
