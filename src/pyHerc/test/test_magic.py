#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010 Tuukka Turto
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

import pyHerc
import pyHerc.rules.magic

class test_magic:

    def test_healingEffect(self):
        """
        Test that a healing effect can be applied on a character
        """
        character = pyHerc.data.model.Character()
        character.hp = 1
        pyHerc.rules.magic.castEffect(character, {'name':'healing', 'power':'1d10'}, [10])

        assert(character.hp == 11)
