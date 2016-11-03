Feature: Magic
  as an spell caster
  in order to survive my adventure
  I want to use spells

  Background:
     Given Simon is Wizard
       And Uglak is Goblin
       And Uglak is almost dead
       And Simon is standing away from Uglak

  Scenario: Magic missile
       When Simon casts magic missile on Uglak
       Then Uglak should be dead

  Scenario: Fireball
      Given Zhagh is Goblin
        And Zhagh is almost dead
        And Zhagh is standing next to Uglak
        And Simon is standing away from Zhagh
       When Simon casts fireball on Zhagh
       Then Uglak should be dead
        And Zhagh should be dead

  Scenario: Healing
      Given Simon is almost dead
       When Simon casts healing wind
       Then Simon should be in full health

#  @active
#  Scenario: Domain specialization
#      Given Simon has rune
#       When Simon uses rune for fire domain
#       Then Simon should have more fire spells
#        And Rune should not be in inventory of Simon

  Scenario: Out of spirit
      Given Simon has no spirit left
       When Simon casts magic missile on Uglak
       Then Uglak should be alive

  Scenario: Effects
      Given Pete is Adventurer
        And Pete is standing next to Uglak
       When Simon casts fireball on Uglak
       Then Pete should be on fire
        And Pete should have less hitpoints
