Feature: Pits
  as an evil overlord
  in order to protect the dungeon
  I want to place pits there

  Background:
     Given Pete is Adventurer
       And Pete is standing in room
       And pit is next to Pete

  Scenario: Dying when falling into a pit
       When Pete walks on pit
       Then Pete should be dead

  Scenario: Dropping items into a pit
      Given Pete wears flying boots
        And Pete has dagger
       When Pete walks on pit
        And Pete drops dagger
       Then dagger should not be in room
