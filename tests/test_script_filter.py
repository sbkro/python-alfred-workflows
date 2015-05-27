# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as etree
from nose.tools import eq_, ok_, assert_raises
from workflows.script_filter import Items, Item, Title, SubTitle, Icon, Text


def assert_xml(expect, actual):
    eq_(expect.tag, actual.tag)
    eq_(expect.attrib, actual.attrib)
    eq_(str.rstrip(expect.text) if expect.text is not None else '',
        str.rstrip(actual.text) if actual.text is not None else '')

    for i, child_expect in enumerate(expect):
        assert_xml(child_expect, actual[i])


def test_script_xml_filter_format():
    root = Items()

    i1 = Item(uid='desktop', arg='~/Desktop', valid=True,
              autocomplete='Desktop', type='file')
    i1.append(Title('Desktop'))
    i1.append(SubTitle('~/Desktop'))
    i1.append(Icon('~/Desktop', type='fileicon'))
    root.append(i1)

    i2 = Item(uid='flickr', valid=False, autocomplete='flickr')
    i2.append(Title('Flickr'))
    i2.append(Icon('flickr.png'))
    root.append(i2)

    i3 = Item(uid='image', autocomplete='My holiday photo', type='file')
    i3.append(Title('My holiday photo'))
    i3.append(SubTitle('~/Pictures/My holiday photo.jpg'))
    i3.append(Icon('public.jpeg', type='filetype'))
    root.append(i3)

    i4 = Item(uid='home', arg="~/", valid=True, autocomplete='Home',
              type='file')
    i4.append(Title('Home Folder'))
    i4.append(Icon('~/', type='fileicon'))
    i4.append(SubTitle('Home folder ~/'))
    i4.append(SubTitle('Subtext when shift is pressed', mod='shift'))
    i4.append(SubTitle('Subtext when fn is pressed', mod='fn'))
    i4.append(SubTitle('Subtext when ctrl is pressed', mod='ctrl'))
    i4.append(SubTitle('Subtext when alt is pressed', mod='alt'))
    i4.append(SubTitle('Subtext when cmd is pressed', mod='cmd'))
    i4.append(Text('Text when copying', type='copy'))
    i4.append(Text('Text for LargeType', type='largetype'))
    root.append(i4)

    a = etree.parse(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'data', 'script_filter_xml_format.xml')
    )

    assert_xml(a.getroot(), root.build())


def test_item():
    item = Item('root')

    eq_(None, item.valid)
    ok_(isinstance(item.uid, basestring))

    item.valid = True
    eq_('YES', item.valid)

    item.valid = False
    eq_('no', item.valid)

    with assert_raises(ValueError) as e:
        item.valid = 'dummy'
    eq_('valid must be [True, False, None]', str(e.exception))


def test_subtitle():
    # not attribute
    root = etree.Element('root')
    e = SubTitle('subtitle_text')
    e.build(root)
    eq_('<root><subtitle>subtitle_text</subtitle></root>',
        etree.tostring(root))

    # mod / shift
    root = etree.Element('root')
    e = SubTitle('subtitle_text', mod='shift')
    e.build(root)
    eq_('<root><subtitle mod="shift">subtitle_text</subtitle></root>',
        etree.tostring(root))

    # mod / fn
    root = etree.Element('root')
    e = SubTitle('subtitle_text', mod='fn')
    e.build(root)
    eq_('<root><subtitle mod="fn">subtitle_text</subtitle></root>',
        etree.tostring(root))

    # mod / ctrl
    root = etree.Element('root')
    e = SubTitle('subtitle_text', mod='ctrl')
    e.build(root)
    eq_('<root><subtitle mod="ctrl">subtitle_text</subtitle></root>',
        etree.tostring(root))

    # mod / alt
    root = etree.Element('root')
    e = SubTitle('subtitle_text', mod='alt')
    e.build(root)
    eq_('<root><subtitle mod="alt">subtitle_text</subtitle></root>',
        etree.tostring(root))

    # mod / cmd
    root = etree.Element('root')
    e = SubTitle('subtitle_text', mod='cmd')
    e.build(root)
    eq_('<root><subtitle mod="cmd">subtitle_text</subtitle></root>',
        etree.tostring(root))

    # error
    with assert_raises(ValueError) as ve:
        e = SubTitle('root')
        e.mod = 'dummy'
    eq_("mod must be ['shift', 'fn', 'ctrl', 'alt', 'cmd', None]",
        str(ve.exception))


def test_icon():
    # not attribute
    root = etree.Element('root')
    e = Icon('icon_text')
    e.build(root)
    eq_('<root><icon>icon_text</icon></root>', etree.tostring(root))

    # fileicon attribute
    root = etree.Element('root')
    e = Icon('icon_text', type='fileicon')
    e.build(root)
    eq_('<root><icon type="fileicon">icon_text</icon></root>',
        etree.tostring(root))

    # filetype attribute
    root = etree.Element('root')
    e = Icon('icon_text', type='filetype')
    e.build(root)
    eq_('<root><icon type="filetype">icon_text</icon></root>',
        etree.tostring(root))

    # error
    with assert_raises(ValueError) as ve:
        e = Icon('root')
        e.type = 'dummy'
    eq_("type must be ['fileicon', 'filetype', None]", str(ve.exception))


def test_text():
    # copy
    root = etree.Element('root')
    e = Text('text', type='copy')
    e.build(root)
    eq_('<root><text type="copy">text</text></root>', etree.tostring(root))

    # largetype
    root = etree.Element('root')
    e = Text('text', type='largetype')
    e.build(root)
    eq_('<root><text type="largetype">text</text></root>',
        etree.tostring(root))

    # error
    with assert_raises(ValueError) as ve:
        e = Text('text')
        e.type = 'dummy'
    eq_("type must be ['copy', 'largetype', None]", str(ve.exception))
