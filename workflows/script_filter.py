# -*- coding: utf-8 -*-
import uuid
from .commons.xml_tree import Element

'''
This module is utilities of Script Filter.
By using it, the follwing functions are provided.

    * data structure for Script Filter. and convert to XML from it.

About Script Filter, refer to **Script Filter XML format ** workflows
from Alfred Preferences.

Code examples ::
    items = Items()

    i = Item(uid='desktop', arg='~/Desktop', valid='YES',
             autocomplate='Desktop', type='file')
    i.append(Title('Desktop'))
    i.append(SubTitle('~/Desktop'))
    i.append(Icon('~/Desktop', type='fileicon'))

    items.append(i)

    import xml.etree.ElementTree as etree
    print etree.tostring(items.build())

    # display follows xml.
    #
    # <items>
    #     <item uid="desktop" arg="~/Desktop" valid="YES"
    #      autocomplate="Desktop" type="file">
    #         <title>Desktop</title>
    #         <subtitle>~/Desktop</subtitle>
    #         <icon type="fileicon">~/Desktop</title>
    #     </item>
    # </items>
'''


class Title(Element):
    '''
    Title element. This element is child node of **Item**.
    '''
    __element_name__ = 'title'


class SubTitle(Element):
    '''
    Subtitle element. This element is child node of **Item**.
    '''
    __element_name__ = 'subtitle'
    __attributes__ = ['mod']

    _mod_defs = ['shift', 'fn', 'ctrl', 'alt', 'cmd', None]

    @property
    def mod(self):
        return self.__mod

    @mod.setter
    def mod(self, mod):
        if mod not in self._mod_defs:
            raise ValueError('mod must be {0}'.format(self._mod_defs))

        self.__mod = mod


class Icon(Element):
    '''
    Icon element. This element is child node of **Item**.
    '''
    __element_name__ = 'icon'
    __attributes__ = ['type']

    _type_defs = ['fileicon', 'filetype', None]

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        if type not in self._type_defs:
            raise ValueError('type must be {0}'.format(self._type_defs))

        self.__type = type


class Text(Element):
    '''
    Text element. This element is child node of **Item**.
    '''
    __element_name__ = 'text'
    __attributes__ = ['type']

    _type_defs = ['copy', 'largetype', None]

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        if type not in self._type_defs:
            raise ValueError('type must be {0}'.format(self._type_defs))

        self.__type = type


class Item(Element):
    '''
    Item element. This element is child node of **Items**.
    '''
    __element_name__ = 'item'
    __attributes__ = ['uid', 'arg', 'valid', 'autocomplete', 'type']
    __sub_elements__ = [Title, SubTitle, Icon, Text]

    _valid_defs = [True, False, None]

    @property
    def uid(self):
        return self.__uid

    @uid.setter
    def uid(self, uid):
        if uid:
            self.__uid = uid
        else:
            self.__uid = str(uuid.uuid1())

    @property
    def valid(self):
        return self.__valid

    @valid.setter
    def valid(self, valid):
        if valid not in self._valid_defs:
            raise ValueError('valid must be {0}'.format(self._valid_defs))

        if valid is True:
            self.__valid = 'YES'
        elif valid is False:
            self.__valid = 'no'
        else:
            self.__valid = None


class Items(Element):
    '''
    Items element. This element is root node.
    '''
    __element_name__ = 'items'
    __sub_elements__ = [Item]
