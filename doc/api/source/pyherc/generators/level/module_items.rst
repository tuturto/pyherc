pyherc.generators.level.items
*****************************

.. automodule:: pyherc.generators.level.items
   :show-inheritance:
   
   .. autoclass:: pyherc.generators.level.items.ItemAdderConfiguration(object)
      :show-inheritance:
      
      .. automethod:: add_item(self, min_amount, max_amount, name = None, type = None, location = None)      
   
   .. autoclass:: pyherc.generators.level.items.ItemAdder(object)
      :show-inheritance:

      .. automethod:: add_items(self, level)
      .. automethod:: generate_items(self, item_spec)
      .. automethod:: place_items(self, items, level)

Example of configuration
========================
The example below shows how ItemAdder can be configured. We are creating an
ItemAdder that can be used to add items for upper and lower catacombs levels.

There are 3 groups of items: 2-4 weapons, 0-2 potions and 1-3 food. All of the
generated items will be placed inside of rooms and no named items are defined.

For brewity, creation of ItemGenerator has been left out from the example.

.. testcode::

    from pyherc.generators.level.items import ItemAdderConfiguration, ItemAdder
    from random import Random

    item_adder_config = ItemAdderConfiguration(['upper catacombs',
                                                'lower catacombs'])
    item_adder_config.add_item(min_amount = 2,
                               max_amount = 4,
                               type = 'weapon',
                               location = 'room')
    item_adder_config.add_item(min_amount = 0,
                               max_amount = 2,
                               type = 'potion',
                               location = 'room')
    item_adder_config.add_item(min_amount = 1,
                               max_amount = 3,
                               type = 'food',
                               location = 'room')
    item_generator = None # here you would normally create proper ItemGenerator
                               
    item_adder = ItemAdder(item_generator,
                           item_adder_config,
                           Random())

    print item_adder
    
item_adder now contains a fully configured ItemAdder object.
    
.. testoutput::

    <pyherc.generators.level.items.ItemAdder object at 0x...>