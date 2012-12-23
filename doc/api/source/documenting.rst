Documentation help
******************
This section will have a list of custom helpers for documentation.

Intro
=====
Documentation for both Herculeum and pyherc is written with Sphinx_. It has
been extended with custom directives that are tailored specifically for this
project. Files for documentation can be found in doc-directory.

Setup
-----
To take these extended directives into use, they have to be first included in
conf.py found in source directory of document::

    extensions = ['sphinx.ext.autodoc',
                  'herculeum.sphinx.items']

Items
-----
Items can be shown in manual easily. There are two directives for single items:
itemimage and itemdescription. Both take single parameter which is name of the
item to show::

    .. itemimage:: warhammer

    .. itemdescription:: warhammer

Resulting output:

.. itemimage:: warhammer

.. itemdescription:: warhammer
    
Previous example renders icon of warhammer and short description. Both of these are
loaded directly from configuration of the game, ensuring that they are always
up to date.

Showing list of certain type of items is easy::

    .. itemtable::
       :type: weapon

.. itemtable::
   :type: weapon
       
This will show statistics of all weapons that have entry in documentation.

.. _Sphinx: http://sphinx-doc.org/
