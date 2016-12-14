Feature: Boots
  as an character
  in order to protect my feet
  I want to use different kinds of boots

  Background:
     Given Pete is Adventurer
       And Pete is standing in room

  @automated
  Scenario: Damage reduction
     Given Pete wears light boots
       And caltrops is next to Pete
      When Pete walks on caltrops
      Then damage should be reduced

  @automated
  Scenario: Well protected
     Given Pete wears heavy boots
       And caltrops is next to Pete
      When Pete walks on caltrops
      Then damage should be 1

  @automated
  Scenario: Completely protected
     Given Pete wears iron boots
       And caltrops is next to Pete
      When Pete walks on caltrops
      Then damage should be 0

  @automated
  Scenario: Moving with heavy boots on is slow
     Given Pete wears heavy boots
      When Pete takes a step
      Then Pete should move slower than without heavy boots

  @automated
  Scenario: Flying boots
     Given Pete wears flying boots
       And pit is next to Pete
      When Pete walks on pit
      Then Pete should be alive

  @automated
  Scenario: Speed boots
     Given Pete wears speed boots
      When Pete takes a step
      Then Pete should move faster than without speed boots
