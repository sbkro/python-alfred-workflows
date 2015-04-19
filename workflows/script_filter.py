# -*- coding: utf-8 -*-
from .commons.xml_tree import Element


class Title(Element):
    __element_name__ = 'title'


class SubTitle(Element):
    __element_name__ = 'subtitle'
    __attributes__ = ['mod']


class Icon(Element):
    __element_name__ = 'icon'
    __attributes__ = ['type']


class Text(Element):
    __element_name__ = 'text'
    __attributes__ = ['type']


class Item(Element):
    __element_name__ = 'item'
    __attributes__ = ['uid', 'arg', 'valid', 'autocomplete', 'type']
    __sub_elements__ = [Title, SubTitle, Icon, Text]


class Items(Element):
    __element_name__ = 'items'
    __sub_elements__ = [Item]
