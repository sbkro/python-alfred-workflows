# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree


def getter(attr):
    def _getter(self):
        return getattr(self, '__{0}'.format(attr))

    return _getter


def setter(attr):
    def _setter(self, val):
        setattr(self, '__{0}'.format(attr), val)

    return _setter


class ElementMeta(type):
    def __new__(cls, cls_name, cls_bases, cls_dict):
        if not isinstance(cls_dict.get('__element_name__'), str):
            raise ValueError()

        for se in cls_dict.get('__sub_elements__', []):
            if not isinstance(se, ElementMeta):
                raise ValueError()

        # generate getter/setter
        for attr in cls_dict.get('__attributes__', []):
            if not isinstance(attr, str):
                raise ValueError()

            if attr not in cls_dict.keys():
                cls_dict[attr] = property(getter(attr), setter(attr))

        return type.__new__(cls, cls_name, cls_bases, cls_dict)


class Element(object):
    __metaclass__ = ElementMeta

    # TODO: comment
    __element_name__ = ''
    __attributes__ = []
    __sub_elements__ = []

    def __init__(self, text=None, **kwargs):
        self._text = text
        self._sub_elements = []

        for a in self.__attributes__:
            setattr(self, a, kwargs.get(a, None))

    def __repr__(self):
        return '<{0} (name="{1}" text="{2}" attributes="{3}")>'.format(
            self.__class__.__name__,
            self.__element_name__,
            self._text,
            self.attributes)

    @property
    def attributes(self):
        return {a: getattr(self, a) for a in self.__attributes__
                if getattr(self, a) is not None}

    @property
    def sub_elements(self):
        return self._sub_elements

    @property
    def text(self):
        return self._text

    def append(self, e):
        if not isinstance(e, tuple(self.__sub_elements__)):
            raise TypeError()

        self._sub_elements.append(e)

        return self

    def build(self, parent=None):
        if parent is None:
            e = etree.Element(self.__element_name__, attrib=self.attributes)
        else:
            e = etree.SubElement(
                parent, self.__element_name__, attrib=self.attributes
            )

        if self._text:
            e.text = self._text

        [se.build(parent=e) for se in self.sub_elements]

        return e
