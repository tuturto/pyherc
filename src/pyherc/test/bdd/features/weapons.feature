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

  Scenario: Split damage
      Given Uglak wields sword
       When Uglak hits Pete
       Then Attack should deal piercing damage
        And Attack should deal slashing damage

  Scenario: Hitting with heavy weapon is slow
      Given Pete wields warhammer
       When Pete hits Uglak
       Then Pete should attack slower than without warhammer
