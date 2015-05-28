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


class ScriptFilterManager(object):
    def __init__(self):
        self._items = Items()

    def tostring(self):
        import xml.etree.ElementTree as etree
        return etree.tostring(self._items.build())

    def append_item(self, title, icon_path,
                    subtitle=None, uid=None, arg=None, valid=None,
                    autocomplete=None, item_type=None, icon_type=None):
        item_attrs = {
            'uid': uid,
            'arg': arg,
            'valid': valid,
            'autocomplete': autocomplete,
            'type': item_type
        }

        icon_attrs = {
            'type': icon_type
        }

        i = Item(**item_attrs)
        i.append(Title(title))

        if subtitle is not None:
            i.append(SubTitle(subtitle))

        i.append(Icon(icon_path, **icon_attrs))

        self._items.append(i)

    def append_subtitle(self, index, subtitle,
                        shift=None, fn=None, ctrl=None, alt=None, cmd=None):
        i = self._items.sub_elements[index]

        if SubTitle in i.sub_elements:
            raise ValueError('Subtitle element exist.')

        if subtitle is not None:
            i.append(SubTitle(subtitle))
        if shift is not None:
            i.append(SubTitle(shift, mod='shift'))
        if fn is not None:
            i.append(SubTitle(fn, mod='fn'))
        if ctrl is not None:
            i.append(SubTitle(ctrl, mod='ctrl'))
        if alt is not None:
            i.append(SubTitle(alt, mod='alt'))
        if cmd is not None:
            i.append(SubTitle(cmd, mod='cmd'))

    def append_icon(self, index, path, filetype=False):
        item = self._items.sub_elements[index]

        if Icon in item.sub_elements:
            raise ValueError('Icon element exist.')

        icon_attrs = {'type': 'fileicon'} if filetype is True else {}
        item.append(Icon(path, **icon_attrs))

    def append_text(self, index, copy=None, largetype=None):
        item = self._items.sub_elements[index]

        if Text in item.sub_elements:
            raise ValueError('Text element exist.')

        if copy is not None:
            item.append(Text(copy, type='copy'))

        if largetype is not None:
            item.append(Text(largetype, type='largetype'))
