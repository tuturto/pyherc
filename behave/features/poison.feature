Feature: Poisoning
  as a poison
  in order to function as poison
  I want to damage my targets

  Scenario: poison causes damage
     Given Pete is Adventurer
      When Pete suffers from weak poison
      Then Pete should have less hitpoints

  Scenario: poison kills character
     Given Uglak is Goblin
       And Uglak is standing in room
      When Uglak suffers from strong poison
      Then Uglak should be dead
       And Uglak is not in room
