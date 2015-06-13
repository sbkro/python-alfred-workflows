# -*- coding: utf-8 -*-
import uuid
from .commons.xml_tree import Element


class Title(Element):
    '''Title element. This element is child node of **Item**.'''
    __element_name__ = 'title'


class SubTitle(Element):
    '''Subtitle element. This element is child node of **Item**.'''
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
    '''Icon element. This element is child node of **Item**.'''
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
    '''Text element. This element is child node of **Item**.'''
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
    '''Item element. This element is child node of **Items**.'''
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
    '''Items element. This element is root node.'''
    __element_name__ = 'items'
    __sub_elements__ = [Item]


class ScriptFilterManager(object):
    '''
    This is an utility class for script filter.
    You can create script filter xml easily using following method.

    1. Create object.

        Examples:

            manager = ScriptFilterManager()

    2. Append result item.
       One item corresponds to the Alfred's results of the one line.

       This class provide two type APIs.
       One is basic method. Create a new result item.
       Other is extension method. Add information to specified result.

        Examples:

            manager.append_item('Desktop', '~/Desktop',
                                subtitle='~/Desktop',
                                arg='~/Desktop', valid=True,
                                autocomplate='Desktop', icon_type='fileicon'
                                is_file=True)

    3. Get script filter xml as string. And return stdout to Alfred.

        Examples::

            print manager.tostring()

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
    def __init__(self):
        self._items = Items()

    def tostring(self):
        '''
        Return script filter xml as string.

        Returns:
            str: script filter.
        '''
        import xml.etree.ElementTree as etree
        return etree.tostring(self._items.build())

    def append_item(self, title, icon_path_or_name,
                    subtitle=None, uid=None, arg=None, valid=None,
                    autocomplete=None, icon_type=None, is_file=False):
        '''
        Add Alfred's result item. This is a basic method API.

        Args:
            title (str): title text.
            icon_path_or_name (str): icon path or name.
            subtitle (str, optional): sub title text.
            uid (str, optional): unique id of item
            arg (str, optional): arg of item.
            valid (bool, optional):
                If valid is False, it won't be actioned.
            autocomplete (str, optional):
                If you select the item, this string is complemented in Alfred.
            icon_type (str, optional):
                Loading type of specified icon. Type is follows.

                fileicon: load file type directory from icon path.
                filetype: load file type from icon name.
            is_file (bool, optional): item is treated as file.
        '''
        item_attrs = {
            'uid': uid,
            'arg': arg,
            'valid': valid,
            'autocomplete': autocomplete,
            'type': 'file' if is_file else None
        }

        icon_attrs = {
            'type': icon_type
        }

        i = Item(**item_attrs)
        i.append(Title(title))

        if subtitle is not None:
            i.append(SubTitle(subtitle))

        i.append(Icon(icon_path_or_name, **icon_attrs))

        self._items.append(i)

    def append_subtitle(self, index, subtitle,
                        shift=None, fn=None, ctrl=None, alt=None, cmd=None):
        '''
        Add the sub title to an existing result item.
        This is an extension method API.

        Args:
            index (int): item index.
            subtitle (str): sub title text.
            shift (str, optional): sub title text when shift is pressed.
            fn (str, optional): sub title text when fn is pressed.
            ctrl (str, optional): sub title text when ctrl is pressed.
            alt (str, optional): sub title text when alt is pressed.
            cmd (str, optional): sub title text when cmd is pressed.

        Raises:
            ValueError: If subtitle is added in specified item, already.
        '''
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

    def append_text(self, index, copy=None, largetype=None):
        '''
        Add the text infromation to an existing result item.
        This is an extension method API.

        Args:
            index (int): item index.
            copy (str, optional): text when coping.
            largetype (str, optional): text for LargeType.

        Raises:
            ValueError: If text is added in specified item, already.
        '''
        item = self._items.sub_elements[index]

        if Text in item.sub_elements:
            raise ValueError('Text element exist.')

        if copy is not None:
            item.append(Text(copy, type='copy'))

        if largetype is not None:
            item.append(Text(largetype, type='largetype'))
