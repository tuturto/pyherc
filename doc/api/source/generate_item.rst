Generating an item
******************
This section will have a look at item generation and how to add new items into
the game.

Overview of generating item
===========================
:class:`pyherc.generators.item.ItemGenerator` is used to generate items.

To generate item, following code can be used:

.. code-block:: python

    new_item = self.item_generator.generate_item(item_type = 'food')

This will generate a random item of type food. To generate item of specic name,
following code can be used:

.. code-block:: python

    new_item = self.item_generator.generate_item(name = 'apple')

This will generate an apple.

Defining items
==============
Items are defined in configuration scripts that are fed to 
:class:`pyherc.config.config.Configuration` during system startup. Following 
example defines an apple and dagger for configuration.

.. testcode::

    from pyherc.generators import ItemConfigurations
    from pyherc.generators import ItemConfiguration, WeaponConfiguration
    from pyherc.rules.effects import EffectHandle

    def init_items():
        """
        Initialise common items
        """
        config = []

        config.append(
                      ItemConfiguration(name = 'apple',
                                        cost = 1,
                                        weight = 1,
                                        icons = [501],
                                        types = ['food'],
                                        rarity = 'common'))

        config.append(
                      ItemConfiguration(name = 'dagger',
                                        cost = 2,
                                        weight = 1,
                                        icons = [602, 603],
                                        types = ['weapon',
                                                   'light weapon',
                                                   'melee',
                                                   'simple weapon'],
                                        rarity = 'common',
                                        weapon_configration = WeaponConfiguration(
                                                damage = 2,
                                                critical_range = 11,
                                                critical_damage = 2,
                                                damage_types = ['piercing',
                                                                'slashing'],
                                                weapon_class = 'simple')))

        return config

    config = init_items()
    
    print len(config)
    print config[0]

Example creates a list containing two ItemConfiguration objects.
    
.. testoutput::
        
    2
    <pyherc.generators.item.ItemConfiguration object at 0x...>
        
For more details regarding to configuration, refer to :doc:`configuration`
page.