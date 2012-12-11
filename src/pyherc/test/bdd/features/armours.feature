Feature: Armours
  as an character
  in order to protect myself
  I want to use different kinds of armours

  Background:
     Given Pete is Adventurer
       And Uglak is Goblin
       And Uglak is standing in room
       And Pete is standing next to Uglak

  Scenario: Damage reduction
      Given Pete wields club
        And Uglak wears leather armour
       When Pete hits Uglak
       Then Attack damage should be reduced

  Scenario: Well protected
      Given Uglak wields dagger
        And Pete wears scale mail
       When Uglak hits Pete
       Then Attack damage should be one

  Scenario: Completely protected
      Given Uglak wields dagger
        And Pete wears plate mail
       When Uglak hits Pete
       Then Attack damage should be zero
