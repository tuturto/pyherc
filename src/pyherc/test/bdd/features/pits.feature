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
