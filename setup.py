#!/usr/bin/env python

from distutils.core import setup

setup(name = 'herculeum',
      version = '0.11',
      description = 'Small roguelike game',
      author = 'Tuukka Turto',
      author_email = 'tuukka.turto@oktaeder.net',
      url = 'https://github.com/tuturto/pyherc/',
      classifiers = ['Development Status :: 3 - Alpha',
                     'Environment :: Console :: Curses',
                     'Environment :: Win32 (MS Windows)',
                     'Environment :: X11 Applications :: Qt',
                     'Environment :: MacOS X',
                     'Intended Audience :: End Users/Desktop',
                     'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                     'Natural Language :: English',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3',
                     'Topic :: Games/Entertainment :: Role-Playing'],
      packages = ['herculeum',
                 'herculeum.ai',
                 'herculeum.config', 'herculeum.config.levels',
                 'herculeum.ui',
                 'herculeum.ui.controllers', 'herculeum.ui.gui', 'herculeum.ui.text',
                 'pyherc',
                 'pyherc.ai',
                 'pyherc.config', 'pyherc.config.dsl',
                 'pyherc.data', 'pyherc.data.effects', 'pyherc.data.magic',
                 'pyherc.data.traps',
                 'pyherc.events',
                 'pyherc.generators', 'pyherc.generators.level',
                 'pyherc.generators.level.decorator', 'pyherc.generators.level.partitioners',
                 'pyherc.generators.level.room',
                 'pyherc.ports',
                 'pyherc.rules', 'pyherc.rules.combat', 'pyherc.rules.consume',
                 'pyherc.rules.inventory', 'pyherc.rules.magic',
                 'pyherc.rules.moving', 'pyherc.rules.waiting'],
      scripts = ['src/scripts/herculeum'],
      package_data={'herculeum': ['*.hy',
                               'ai/*.hy']},
      requires = ['decorator (==3.4.0)',
                  'hy (==0.9.12)',
                  'docopt (==0.6.1)'],
      package_dir = {'herculeum': 'src/herculeum',
                     'pyherc': 'src/pyherc'})
