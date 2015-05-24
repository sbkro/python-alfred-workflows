# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree


def getter(attr):
    '''getter method'''
    def _getter(self):
        return getattr(self, '__{0}'.format(attr))

    return _getter


def setter(attr):
    '''setter method'''
    def _setter(self, val):
        setattr(self, '__{0}'.format(attr), val)

    return _setter


class ElementMeta(type):
    def __new__(cls, cls_name, cls_bases, cls_dict):
        if not isinstance(cls_dict.get('__element_name__'), str):
            raise ValueError(
                '__element_name__ must define str. : {0}'.
                format(cls_dict.get('__element_name__').__class__.__name__)
            )

        for se in cls_dict.get('__sub_elements__', []):
            if not isinstance(se, ElementMeta):
                raise ValueError(
                    'value of __sub_elements__ must define ' +
                    'sub class of Element. : {0}'.
                    format(se.__class__.__name__)
                )

        # generate getter/setter
        for attr in cls_dict.get('__attributes__', []):
            if not isinstance(attr, str):
                raise ValueError(
                    'value of __attributes__ must define str. : {0}'.
                    format(attr.__class__.__name__)
                )

            if attr not in cls_dict.keys():
                cls_dict[attr] = property(getter(attr), setter(attr))

        return type.__new__(cls, cls_name, cls_bases, cls_dict)


class Element(object):
    '''
    Base class of XML Element.
    You can generate a xml tree object by extending this class and
    defining the parameters. In detail, refer to follow samples.

    Definition examples. ::
        class Author(Element):
            __element_name__ = 'author'

        class Book(Element):
            __element_name__ = 'book'
            __attributes__ = ['name', 'price']
            __sub_element__ = [Author]

    Code examples. ::
        import Author, Book

        # argument is used as text node content,
        # keyword arguments is used as attributes.
        book = Book(name='learning python', price='3000')
        book.append(Author('aaaa'))

        # create xml object. result as follows.
        #
        # <book name='learning python' price='300'>
        #    <author>aaa</author>
        # </book>
        book.build()
    '''

    __metaclass__ = ElementMeta

    ''' Define element name (Required / str) '''
    __element_name__ = ''

    ''' Define attribute names (Option / list of str) '''
    __attributes__ = []

    ''' Define sub element classes (Option / list of Element) '''
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
        '''
        Return attributes as dict.

        :returns: attributes
        '''
        return {a: getattr(self, a) for a in self.__attributes__
                if getattr(self, a) is not None}

    @property
    def sub_elements(self):
        '''
        Return sub element.

        :returns: sub element.
        '''
        return self._sub_elements

    @property
    def text(self):
        '''
        Return text.

        :returns: text content.
        '''
        return self._text

    def append(self, e):
        '''
        Append child element.

        :param e: child element which append on self.
        :returns: self.
        :raises TypeError: e is invalid.
        '''
        if not isinstance(e, tuple(self.__sub_elements__)):
            raise TypeError(
                'element must be {0}. : {1}'.
                format(
                    [i.__name__ for i in tuple(self.__sub_elements__)],
                    e.__class__.__name__
                )
            )

        self._sub_elements.append(e)

        return self

    def build(self, parent=None):
        '''
        Convert to xml tree from instance variable of element. And return it.

        :param parent:
            parent element.

            If parent is None, this element build as root node.
            If parent is not None, this element build as child of
            specified element.
        :returns: xml tree
        '''
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
