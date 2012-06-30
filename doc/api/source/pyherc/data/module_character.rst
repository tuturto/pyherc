pyherc.data.character
*********************
.. automodule:: pyherc.data.character
   :show-inheritance:

   .. autoclass:: Character
      :show-inheritance:
      
      .. automethod:: __init__(model, action_factory, effects_collection, rng)

      .. autoattribute:: hit_points
      .. autoattribute:: max_hp
      .. autoattribute:: body
      .. autoattribute:: finesse
      .. autoattribute:: mind

      .. automethod:: receive_event(event)
      .. automethod:: act(model)
      .. automethod:: get_attack()
      .. automethod:: set_attack()
      .. automethod:: identify_item(item)
      .. automethod:: is_proficient(weapon)
      .. automethod:: set_mimic_item(item)
      .. automethod:: get_mimic_item()
      .. automethod:: get_location()
      .. automethod:: set_location(location)
      .. automethod:: execute_action(action_parameters)
      .. automethod:: create_action(action_parameters)
      .. automethod:: move(direction)
      .. automethod:: is_move_legal(direction, movement_mode)
      .. automethod:: perform_attack(direction)
      .. automethod:: drink(potion)
      .. automethod:: raise_event(event)
      .. automethod:: add_effect_handle(effect)
      .. automethod:: get_effect_handles(trigger = None)
      .. automethod:: remove_effect_handle(handle)
      .. automethod:: add_effect(effect)
      .. automethod:: get_effects()
      .. automethod:: remove_expired_effects()
      .. automethod:: add_to_tick(cost)
