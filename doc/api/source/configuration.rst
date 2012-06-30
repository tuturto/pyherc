Configuration
*************
Configuration of pyherc is driven by external files and internal scripts.
External files are located in resources directory and internal scripts
in package :py:mod:`pyherc.config`.

Level configuration
===================
Level configuration is done with internal scripts and supports dynamic
detection and loading of scripts. It is enough to place new file
containing configuration script in correct directory, call initialise method
and supply correct namespace:

.. code-block:: python

   config = Configuration(self.base_path, self.world)
   config.initialise(herculeum.config.levels)

The file containing configuration should contain following function to perform
configuration.

.. code-block:: python

    def init_level(rng, item_generator, creature_generator, level_size)

This function should create :py:class:`pyherc.generators.level.config.LevelGeneratorFactoryConfig`
with appropriate values and return it. This configuration is eventually fed to
:class:`pyherc.generators.level.generator.LevelGeneratorFactory` when new level
is requested.
