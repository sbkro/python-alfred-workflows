# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
from nose.tools import eq_, assert_raises
from workflows.commons.xml_tree import Element


class SubItem(Element):
    __element_name__ = 'subitem'
    __attributes__ = ['type']


class Item(Element):
    __element_name__ = 'item'
    __attributes__ = ['type']
    __sub_elements__ = [SubItem]


def test_metaclass():
    with assert_raises(ValueError) as e:
        class ElementNameNotString(Element):
            __element_name__ = 100
    eq_('', str(e.exception))

    with assert_raises(ValueError) as e:
        class ElementNameNotDefined(Element):
            pass
    eq_('', str(e.exception))

    with assert_raises(ValueError) as e:
        class SubElementNotElement(Element):
            __element_name__ = 'tag'
            __sub_elements__ = ['dummy']
    eq_('', str(e.exception))

    with assert_raises(ValueError) as e:
        class AttributeNotString(Element):
            __element_name__ = 'tag'
            __attributes__ = [100]
    eq_('', str(e.exception))


def test_overwrite_property():
    class Sample(Element):
        __element_name__ = 'tag'
        __attributes__ = ['attr']

        @property
        def attr(self):
            return 'customized in getter'

        @attr.setter
        def attr(self, val):
            self._attr = 'customized in setter'

    e = Sample(attr='value')
    eq_('customized in getter', e.attr)

    e.attr = 'value'
    eq_('customized in setter', e._attr)


def test__repr__():
    eq_('<Item (name="item" text="None" attributes="{}")>', repr(Item()))


def test_properties():
    e = Item('item text', type='hoge')
    se = SubItem()
    e.append(se)

    # auto-generated setter method
    eq_('hoge', e.type)

    eq_([se], e.sub_elements)
    eq_({'type': 'hoge'}, e.attributes)
    eq_('item text', e.text)


def test_append():
    e = Item()
    eq_(e, e.append(SubItem()))


def test_append_with_invalid_node():
    item = Item()
    with assert_raises(TypeError) as e:
        item.append('dummy')
        eq_('', str(e.exception))

    sub_item = SubItem()
    with assert_raises(TypeError) as e:
        sub_item.append(SubItem())
        eq_('', str(e.exception))


def test_depth_0():
    eq_('<item />', etree.tostring(Item().build()))


def test_depth_0_with_text():
    eq_('<item>text</item>', etree.tostring(Item('text').build()))


def test_depth_0_with_attrs():
    eq_('<item type="abc" />', etree.tostring(Item(type="abc").build()))


def test_depth_1():
    e = Item()
    e.append(SubItem())
    eq_('<item><subitem /></item>', etree.tostring(e.build()))


def test_depth_1_with_text():
    e = Item()
    e.append(SubItem('item text'))
    eq_('<item><subitem>item text</subitem></item>', etree.tostring(e.build()))


def test_depth_1_with_attrs():
    e = Item()
    e.append(SubItem(type='abc'))
    eq_('<item><subitem type="abc" /></item>', etree.tostring(e.build()))


def test_depth_1_with_multiple_nodes():
    e = Item()
    e.append(SubItem()).append(SubItem())
    eq_('<item><subitem /><subitem /></item>', etree.tostring(e.build()))
