pyherc.config
*************

Overview
========

Configuration of the game is placed in one convenient location, namely to 
Configuration class. Initialisation is done by creating an instance of
Configuration object and passing path to the directory where resources can be
found and instance of Model class. After this configuration can be set by
calling initialise():

.. code-block:: python
    
  model = Model()
  base_path = './'
  self.config = Configuration(base_path, model)
  self.config.initialise()

API
===

.. automodule:: pyherc.config
   :members:
