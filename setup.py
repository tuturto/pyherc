#!/usr/bin/env python

from distutils.core import setup
import py2exe

setup(name = 'herculeum',
      version = '0.8',
      description = 'Small roguelike game',
      long_description = 'Herculeum is a simple roguelike game, where player has to dwelve deep into a dungeon.',
      author = 'Tuukka Turto',
      author_email = 'tuukka.turto@oktaeder.net',
      url = 'https://github.com/tuturto/pyherc/',
      classifiers = ['Development Status :: 3 - Alpha',
                     'Intended Audience :: End Users/Desktop',
                     'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                     'Natural Language :: English',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python :: 2.7',
                     'Topic :: Games/Entertainment :: Role-Playing'],
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
      requires = ['decorator'],
      options = {
                 'py2exe': {
                            'dll_excludes': ['MSVCP90.dll'],
                            'includes': ['sip']
                            }},
      package_dir = {'': 'src'})
