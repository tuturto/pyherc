Feature: Combat
  as an character
  in order to kill enemies
  I want to damage my enemies

  Background:
     Given Pete is Adventurer
       And Uglak is Goblin
       And Pete is standing next to Uglak
  
  Scenario: hit in unarmed combat
      When Uglak hits Pete
      Then Pete should have less hitpoints

  Scenario: hit in melee combat
     Given Uglak wields dagger
      When Uglak hits Pete
      Then Pete should have less hitpoints

  Scenario: Suspectible against piercing damage
     Given Pete wields dagger
       And Uglak is suspectible against piercing
      When Pete hits Uglak
      Then Uglak should suffer extra damage

  Scenario: die in combat
      Given Uglak wields dagger
        And Uglak is almost dead
       When Pete hits Uglak
       Then Uglak should be dead
        And dagger should be in room
