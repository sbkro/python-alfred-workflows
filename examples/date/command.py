# -*- coding: utf-8 -*-
from datetime import datetime
import xml.etree.ElementTree as etree
import date.workflows.script_filter as sf


class DateCommand(object):
    def __init__(self, config):
        if 'format' in config:
            self._format = config.get('format')

    def execute(self):
        now = datetime.now()

        items = sf.Items()
        items.append(
            sf.Item(valid='NO').append(sf.Title(now.strftime(self._format)))
        )

        return etree.tostring(items.build())
