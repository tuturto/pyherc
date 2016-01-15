# -*- coding: utf-8 -*-

# Copyright (c) 2010-2015 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Module for item statistics
"""
import os.path

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import unchanged
from docutils.parsers.rst.directives.images import Image
from herculeum.sphinx.helpers import shutdown_application, with_config
from PyQt4.QtGui import QColor, QImage, QPainter


class ItemDescription(nodes.General, nodes.Element):
    """
    Node for describing items
    """
    pass

class ItemTable(nodes.General, nodes.Element):
    """
    Node for presenting multiple items in a table
    """
    pass

def make_row(*args):
    """
    Utility method to create a table row

    .. note:: accepts multiple arguments, each argument is a text for a new cell
    """
    row_node = nodes.row()

    for cell in args:
        entry = nodes.entry()
        para = nodes.paragraph()
        para += nodes.Text(cell, cell)
        entry += para
        row_node += entry

    return row_node

def make_armour_table(env, node):
    """
    Utility method to create a table for armours
    """
    table = nodes.table()
    tgroup = nodes.tgroup(cols=3)
    table += tgroup
    for i in range(4):
        colspec = nodes.colspec(colwidth = 1)
        tgroup += colspec

    rows = []

    thead = nodes.thead()

    row_node = make_row('armour', 'damage reduction', 'speed modifier')
    thead += row_node

    tgroup += thead

    for item_entry in (x for x in env.pyherc_context.items
                       if node.options['type'] in x['item'].tags):

        item = item_entry['item']

        row_node = make_row(item.name,
                            item.armour_data.damage_reduction,
                            item.armour_data.speed_modifier)

        rows.append(row_node)

    tbody = nodes.tbody()
    tbody.extend(rows)
    tgroup += tbody

    return table

def make_weapon_table(env, node):
    """
    Utility method to create a table for weapons
    """
    table = nodes.table()
    tgroup = nodes.tgroup(cols=7)
    table += tgroup
    for i in range(7):
        colspec = nodes.colspec(colwidth = 1)
        tgroup += colspec

    rows = []

    thead = nodes.thead()

    row_node = make_row('weapon', 'damage', 'critical range',
                        'critical damage', 'damage types', 'type',
                        'weight class')
    thead += row_node

    tgroup += thead

    for item_entry in (x for x in env.pyherc_context.items
                       if any(z in x['item'].tags for z in ['weapon', 'ammunition'])):

        item = item_entry['item']

        if item.weapon_data is not None:
            damage_str = str.join(' / ', [str(x[0]) for x in item.weapon_data.damage])
            damage_types_str = str.join(' / ', [str(x[1]) for x in item.weapon_data.damage])
        elif item.ammunition_data is not None:
            damage_str = str.join(' / ', [str(x[0]) for x in item.ammunition_data.damage])
            damage_types_str = str.join(' / ', [str(x[1]) for x in item.ammunition_data.damage])

        if 'simple weapon' in item.tags:
            weapon_type = 'simple'
        elif 'martial weapon' in item.tags:
            weapon_type = 'martial'
        elif 'exotic weapon' in item.tags:
            weapon_type = 'exotic'
        else:
            weapon_type = ' '

        if 'light weapon' in item.tags:
            weapon_weight = 'light'
        elif 'one-handed' in item.tags:
                weapon_weight = 'one-handed'
        elif 'two-handed' in item.tags:
            weapon_weight = 'two-handed'
        else:
            weapon_weight = ' '

        if item.weapon_data is not None:
            row_node = make_row(item.name, damage_str,
                                item.weapon_data.critical_range,
                                item.weapon_data.critical_damage,
                                damage_types_str, weapon_type, weapon_weight)
        elif item.ammunition_data is not None:
            row_node = make_row(item.name, damage_str,
                                item.ammunition_data.critical_range,
                                item.ammunition_data.critical_damage,
                                damage_types_str, weapon_type, weapon_weight)
        rows.append(row_node)

    tbody = nodes.tbody()
    tbody.extend(rows)
    tgroup += tbody

    return table

def process_item_descriptions(app, doctree, fromdocname):
    """
    Process item descriptions after document tree has been built
    """
    env = app.builder.env

    for node in doctree.traverse(ItemTable):

        if node.options['type'] == 'weapon':
            table = make_weapon_table(env, node)
        elif node.options['type'] == 'armour':
            table = make_armour_table(env, node)

        node.replace_self(table)

class ItemTableDirective(Directive):
    """
    Directive to insert a table of items
    """
    has_content = False
    final_argument_whitespace = True
    option_spec = {'type': unchanged}

    def run(self):
        node = ItemTable('')
        node.options = self.options
        return [node]


class ItemDescriptionDirective(Directive):
    """
    Directive to insert item description
    """
    has_content = False
    required_arguments = 1
    final_argument_whitespace = True

    @with_config
    def run(self, config):
        env = self.state.document.settings.env

        targetid = "itemdescription-{0:d}".format(env.new_serialno('itemdescription'))
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
    """
    Directive to insert image of an item
    """

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
        new_image = QImage(32, 32, QImage.Format_ARGB32)
        new_image.fill(QColor(200, 200, 200))
        painter = QPainter(new_image)
        painter.drawPixmap(0, 0, icon)
        painter = None

        new_image.save(os.path.join(folder, file_name))

        self.arguments[0] = os.path.join('generated/', file_name)

        return super(ItemImageDirective, self).run()

class DocumentationContext():
    """
    Context used to store data during doctree building
    """

    def __init__(self):
        """
        Default constructor
        """
        super(DocumentationContext, self).__init__()
        self.items = []

def setup(app):
    """
    Setup integration with Sphinx
    """

    app.add_node(ItemDescription)
    app.add_node(ItemTable)

    app.add_directive('itemdescription', ItemDescriptionDirective)
    app.add_directive('itemtable', ItemTableDirective)
    app.add_directive('itemimage', ItemImageDirective)

    app.connect('doctree-resolved', process_item_descriptions)
    app.connect('env-purge-doc', shutdown_application)
