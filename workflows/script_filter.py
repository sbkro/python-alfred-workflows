# -*- coding: utf-8 -*-
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


class Icon(Element):
    '''
    Icon element. This element is child node of **Item**.
    '''
    __element_name__ = 'icon'
    __attributes__ = ['type']


class Text(Element):
    '''
    Text element. This element is child node of **Item**.
    '''
    __element_name__ = 'text'
    __attributes__ = ['type']


class Item(Element):
    '''
    Item element. This element is child node of **Items**.
    '''
    __element_name__ = 'item'
    __attributes__ = ['uid', 'arg', 'valid', 'autocomplete', 'type']
    __sub_elements__ = [Title, SubTitle, Icon, Text]


class Items(Element):
    '''
    Items element. This element is root node.
    '''
    __element_name__ = 'items'
    __sub_elements__ = [Item]
