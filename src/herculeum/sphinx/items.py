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
from herculeum.sphinx.helpers import with_config
import os.path
import re
from PyQt4.QtGui import QImage
from PyQt4.QtCore import Qt

class ItemDescription(nodes.General, nodes.Element):
    pass

def visit_itemdescription_node(self, node):
    self.visit_admonition(node)

def depart_itemdescription_node(self, node):
    self.depart_admonition(node)

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

def setup(app):
    app.add_node(ItemDescription)

    app.add_directive('itemdescription', ItemDescriptionDirective)
    app.add_directive('itemimage', ItemImageDirective)
