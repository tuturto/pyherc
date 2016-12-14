Feature: Society management
  as an elder
  in order to ensure survival
  I want to manage my society

  Scenario: viewing council
      When I view council
      Then Each member is shown

  Scenario: viewing council member
      When I view council memeber
      Then council member is shown
       And their mood is indicated

  Scenario: viewing society
      When I view society
      Then general report of society is shown
       And random council memeber voices their opinion

  Scenario: diminishing raw materials
     Given society has lots of raw materials
       And society has expensive construction project
       And society has no raw material income
      When time passes
      Then amount of raw materials should go down

  Scenario: collecting raw materials
     Given society has some raw materials
       And society has no construction project
       And society has medium raw material income
      When time passes
      Then amount of raw materials should go up
