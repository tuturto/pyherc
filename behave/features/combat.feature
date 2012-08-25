Feature: Combat
  as an character
  in order to kill enemies
  I want to damage my enemies

  Scenario: hit in unarmed combat
     Given Pete is Adventurer
       And Uglak is Goblin
       And Uglak is standing in room
       And Pete is standing next to Uglak     
      When Uglak hits Pete
      Then Pete should have less hitpoints

  Scenario: hit in melee combat
     Given Pete is Adventurer
       And Uglak is Goblin
       And Uglak wields dagger
       And Uglak is standing in room
       And Pete is standing next to Uglak     
      When Uglak hits Pete
      Then Pete should have less hitpoints