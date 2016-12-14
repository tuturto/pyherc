Feature: Waiting
  as an character
  in order to manage my tactical options
  I want to wait

  @automated
  Scenario: wait
     Given Pete is Adventurer
      When Pete waits
      Then time should pass for Pete
