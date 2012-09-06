Feature: Weapons
  as an character
  in order to kill enemies
  I want to have different kinds of weapons

  Background:
     Given Pete is Adventurer
       And Uglak is Goblin
       And Uglak is standing in room
       And Pete is standing next to Uglak

  Scenario: Piercing damage
      Given Uglak wields dagger
       When Uglak hits Pete
       Then Attack should deal piercing damage
