Generating an item
******************
This section will have a look at item generation and how to add new items into
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

Defining items
==============
Items are defined in resources/items.xml. Following snippet is used for dagger::

    <item>
        <name>dagger</name>
        <cost>2</cost>
        <damage>2</damage>
        <criticalRange>11</criticalRange>
        <criticalDamage>2</criticalDamage>
        <weight>1</weight>
        <damageTypes>
            <damageType>piercing</damageType>
            <damageType>slashing</damageType>
        </damageTypes>
        <class>simple</class>
        <icons>
            <icon>ITEM_DAGGER_1</icon>
        </icons>
        <types>
            <type>weapon</type>
            <type>light weapon</type>
            <type>melee</type>
            <type>simple weapon</type>
        </types>
        <rarity>common</rarity>
    </item>
    
+---------------+-------------------------------+--------------------------------------------------------------------------------+
|Element        |Explanation                    |Notes                                                                           |
+===============+===============================+================================================================================+
|Name           |Name of the item               |                                                                                |
+---------------+-------------------------------+--------------------------------------------------------------------------------+
|Cost           |Base cost in coins             |                                                                                |
+---------------+-------------------------------+--------------------------------------------------------------------------------+
|Damage         |Base damage                    |                                                                                |
+---------------+-------------------------------+--------------------------------------------------------------------------------+
|criticalRange  |Chances for critical hit       |                                                                                |
+---------------+-------------------------------+--------------------------------------------------------------------------------+
|criticalDamage |Amount of critical damage      |                                                                                |
+---------------+-------------------------------+--------------------------------------------------------------------------------+
|weight         |Weight of the item             |                                                                                |
+---------------+-------------------------------+--------------------------------------------------------------------------------+
|damageTypes    |Types of damage weapon does    |                                                                                |
+---------------+-------------------------------+--------------------------------------------------------------------------------+
|class          |Class of the weapon            |                                                                                |
+---------------+-------------------------------+--------------------------------------------------------------------------------+
|icons          |Icons used to display the item |Only one is selected when item is created                                       |
+---------------+-------------------------------+--------------------------------------------------------------------------------+
|types          |Tags                           |Used in item generation, for example when generator should make 'simple weapon' |
+---------------+-------------------------------+--------------------------------------------------------------------------------+
|rarity         |Rarity of the item             |common, uncommon, rare, epic, legendary, artifact                               |
+---------------+-------------------------------+--------------------------------------------------------------------------------+

