Feature: Ranged combat
  as an character
  in order to kill enemies from distance
  I want to use ranged weapons

  Background:
     Given Pete is Adventurer
       And Uglak is Goblin
       And Uglak is standing in room
       And Pete is standing away from Uglak

  @automated
  Scenario: hit in ranged combat
     Given Pete wields bow and arrows
      When Pete hits Uglak
      Then Uglak should have less hitpoints
