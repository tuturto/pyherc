Feature: Boots
  as an character
  in order to protect my feet
  I want to use different kinds of boots

  Background:
     Given Pete is Adventurer
       And Pete is standing in room
       And caltrops is located in corner of room

  Scenario: Damage reduction
     Given Pete is wearing light boots
      When Pete steps on caltrops
      Then Trap damage should be reduced

  Scenario: Well protected
     Given Pete is wearing heavy boots
      When Pete steps on caltrops
      Then Trap damage should be 1

  Scenario: Completely protected
     Given Pete is wearing iron boots
      When Pete steps on caltrops
      Then Trap damage should be 0

  Scenario: Moving in heavy armour is slow
     Given Pete wears heavy boots
      When Pete takes a step
      Then Pete should move slower than without heavy boots

  Scenario: Flying boots
     Given Pete wears flying boots
       And pit is next to Pete
      When Pete steps on pit
      Then Pete should be alive

  Scenario: Speed boots
     Given Pete wears speed boots
      When Pete takes a step
      Then Pete should move faster than without speed boots
