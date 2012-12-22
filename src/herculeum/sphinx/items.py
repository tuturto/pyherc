#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
#
#   This file is part of pyherc.
#
#   pyherc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyherc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

"""
Module for item statistics
"""
from docutils import nodes
from docutils.parsers.rst import directives, Directive
from docutils.parsers.rst.directives.images import Image
from docutils.parsers.rst.directives import unchanged
from herculeum.sphinx.helpers import with_config
import os.path
import re
from PyQt4.QtGui import QImage
from PyQt4.QtCore import Qt

class ItemDescription(nodes.General, nodes.Element):
    pass

class ItemTable(nodes.General, nodes.Element):
    pass

def visit_itemdescription_node(self, node):
    self.visit_admonition(node)

def depart_itemdescription_node(self, node):
    self.depart_admonition(node)

def process_item_descriptions(app, doctree, fromdocname):
    env = app.builder.env

    for node in doctree.traverse(ItemTable):

        table = nodes.table()
        tgroup = nodes.tgroup(cols=8)
        table += tgroup
        for i in range(8):
            colspec = nodes.colspec(colwidth = 10)
            tgroup += colspec

        rows = []
        for item_entry in (x for x in env.pyherc_context.items
                           if node.options['type'] in x['item'].tags):
            row_node = nodes.row()
            item = item_entry['item']

            entry = nodes.entry()
            para = nodes.paragraph()
            para += nodes.Text(item.name, item.name)
            entry += para
            row_node += entry

            entry = nodes.entry()
            para = nodes.paragraph()
            damage_str = str.join(' / ', [str(x[0]) for x in item.weapon_data.damage])
            para += nodes.Text(damage_str, damage_str)
            entry += para
            row_node += entry

            entry = nodes.entry()
            para = nodes.paragraph()
            para += nodes.Text(item.weapon_data.critical_range, item.weapon_data.critical_range)
            entry += para
            row_node += entry

            entry = nodes.entry()
            para = nodes.paragraph()
            para += nodes.Text(item.weapon_data.critical_damage, item.weapon_data.critical_damage)
            entry += para
            row_node += entry

            entry = nodes.entry()
            para = nodes.paragraph()
            damage_str = str.join(' / ', [str(x[1]) for x in item.weapon_data.damage])
            para += nodes.Text(damage_str, damage_str)
            entry += para
            row_node += entry

            if 'simple weapon' in item.tags:
                weapon_type = 'simple'
            elif 'martial weapon' in item.tags:
                weapon_type = 'martial'
            elif 'exotic weapon' in item.tags:
                weapon_type = 'exotic'
            else:
                weapon_type = ' '

            entry = nodes.entry()
            para = nodes.paragraph()
            para += nodes.Text(weapon_type, weapon_type)
            entry += para
            row_node += entry

            if 'light' in item.tags:
                weapon_weight = 'light'
            elif 'one-handed' in item.tags:
                weapon_weight = 'one-handed'
            elif 'two-handed' in item.tags:
                weapon_weight = 'two-handed'
            else:
                weapon_weight = ' '

            entry = nodes.entry()
            para = nodes.paragraph()
            para += nodes.Text(weapon_weight, weapon_weight)
            entry += para
            row_node += entry

            entry = nodes.entry()
            para = nodes.paragraph()
            para += nodes.Text(item.rarity, item.rarity)
            entry += para
            row_node += entry

            rows.append(row_node)

        tbody = nodes.tbody()
        tbody.extend(rows)
        tgroup += tbody

        node.replace_self(table)

class ItemTableDirective(Directive):
    has_content = False
    final_argument_whitespace = True
    option_spec = {'type': unchanged}

    def run(self):
        node = ItemTable('')
        node.options = self.options
        return [node]


class ItemDescriptionDirective(Directive):

    # this enables content in the directive
    has_content = False
    required_arguments = 1
    final_argument_whitespace = True

    @with_config
    def run(self, config):
        env = self.state.document.settings.env

        targetid = "itemdescription-%d" % env.new_serialno('itemdescription')
        targetnode = nodes.target('', '', ids=[targetid])

        para = nodes.paragraph()
        generator = config.item_generator

        item = generator.generate_item(name = self.arguments[0])

        para += nodes.Text(item.description, item.description)

        if not hasattr(env, 'pyherc_context'):
            env.pyherc_context = DocumentationContext()

        env.pyherc_context.items.append({'docname': env.docname,
                                         'lineno': self.lineno,
                                         'item': item,
                                         'target': targetnode})

        return [para]

class ItemImageDirective(Image):

    @with_config
    def run(self, config):
        folder = os.path.abspath('./source/generated')

        generator = config.item_generator
        item = generator.generate_item(name = self.arguments[0])
        file_name = item.name
        file_name = file_name + '.png'
        file_name = file_name.replace(' ', '')

        surface_manager = config.surface_manager
        icon = surface_manager.get_icon(item.icon)
        img = icon.toImage()
        new_image = img.convertToFormat(QImage.Format_RGB32,
                                        Qt.DiffuseAlphaDither)

        new_image.save(os.path.join(folder, file_name))

        self.arguments[0] = os.path.join('generated/', file_name)

        return super(ItemImageDirective, self).run()

class DocumentationContext(object):

    def __init__(self):
        super(DocumentationContext, self).__init__()
        self.items = []

def setup(app):
    app.add_node(ItemDescription)
    app.add_node(ItemTable)

    app.add_directive('itemdescription', ItemDescriptionDirective)
    app.add_directive('itemtable', ItemTableDirective)
    app.add_directive('itemimage', ItemImageDirective)

    app.connect('doctree-resolved', process_item_descriptions)
