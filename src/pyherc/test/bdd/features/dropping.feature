Feature: Dropping items
  as an character
  in order to manage my inventory
  I want to drop items

  Scenario: drop item
     Given Pete is Adventurer
       And Pete is standing in room
       And Pete has dagger
      When Pete drops dagger
      Then dagger should be in room
       And dagger should be at same place as Pete
       And dagger should not be in inventory of Pete
       And time should pass for Pete
