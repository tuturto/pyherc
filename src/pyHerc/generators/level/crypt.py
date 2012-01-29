#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2012 Tuukka Turto
#
#   This file is part of pyHerc.
#
#   pyHerc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyHerc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyHerc.  If not, see <http://www.gnu.org/licenses/>.

class CryptGenerator:
    '''
    Class used to generate crypts
    '''
    def __init__(self, action_factory):
        self.logger = logging.getLogger('pyHerc.generators.cryptgenerator.CryptGenerator')
        self.item_generator = pyHerc.generators.ItemGenerator()
        self.creature_generator = pyHerc.generators.CreatureGenerator(action_factory)

    def __getstate__(self):
        '''
        Override __getstate__ in order to get pickling work
        '''
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        '''
        Override __setstate__ in order to get pickling work
        '''
        self.__dict__.update(d)
        self.logger = logging.getLogger('pyHerc.generators.cryptgenerator.CryptGenerator')

    def generate_level(self, portal, model, new_portals = 0, level=1, room_min_size = (2, 2)):
        pass
