Feature: Moving around
  as an character
  in order to explore the dungeon
  I want to walk around

  Background:
     Given Pete is Adventurer
       And Pete is Player
       And Pete is standing in room
       And stairs is Portal
       And stairs leads outside
       And stairs is away from Pete

  Scenario: Walking
       When Pete walks on stairs
       Then Pete and stairs are located at the same place
  
  Scenario: Leaving dungeon
       When Pete walks on stairs
        And Pete enters stairs
       Then Game ends
