Generating an item
******************
This section will have a look at item generation and how to add new levels into
the game.

Overview of generating item
===========================
:class:`pyherc.generators.item.ItemGenerator` is used to generate items.

To generate item, following code can be used:

.. code-block:: python

    new_item = self.item_generator.generate_item(model.tables, {'type':'food'})

This will generate a random item of type food.

Instance of :class:`pyherc.rules.tables.Tables` is passed as a first argument
to the method. It contains (among other things) list of all possible items
that the game can create. These are loaded as the game starts up. File where
item definitions are, is resources/items.xml. By editing this file, new items
can be easily added.

Second parameter given to the method is a dictionary, which defines parameters
used in item generation. Following keys are currently supported:

  - name: generates item with given name
  - type: generates item with given type (food, weapon)

