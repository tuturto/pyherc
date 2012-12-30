#!/usr/bin/env python

from distutils.core import setup
import py2exe

setup(name = 'herculeum',
      version = '0.8',
      description = 'Small roguelike',
      author = 'Tuukka Turto',
      author_email = 'tuukka.turto@oktaeder.net',
      url = 'https://github.com/tuturto/pyherc/',
      windows = [{'script': 'src/herculeum/main.py',
                  'dest_base': 'herculeum',
                  'icon_resources': [(0,'resources/herculeum.ico')]
                  }],
      packages = ['herculeum', 
                 'herculeum.config', 'herculeum.config.levels',
                 'herculeum.gui', 
                 'pyherc',
                 'pyherc.ai',
                 'pyherc.config', 'pyherc.config.dsl',
                 'pyherc.data', 'pyherc.data.effects',
                 'pyherc.events',
                 'pyherc.generators', 'pyherc.generators.level', 
                 'pyherc.generators.level.decorator', 'pyherc.generators.level.partitioners',
                 'pyherc.generators.level.room',
                 'pyherc.rules', 'pyherc.rules.attack', 'pyherc.rules.consume',
                 'pyherc.rules.inventory', 'pyherc.rules.move'],
      options = {
                 "py2exe": {
                            "dll_excludes": ["MSVCP90.dll"],
                            "includes": ["sip"]
                            }},
      package_dir = {'': 'src'})
