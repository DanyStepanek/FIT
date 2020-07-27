Feature: Edit user in users

  Background: admin logged and actual page is users page
    Given admin is logged
    And actual page is users page
    And user list contains two users


  Scenario: Edit user as admin
    When click 'edit' button
    And edit some columns correctly
    And save changes
    Then users informations are actualized

  Scenario: Change users email to invalid email
    When click 'edit' button
    And change email to invalid email
    And save changes
    Then users informations are not changed
    And the page is not changed

  Scenario: Change users nick to invalid nick
    When click 'edit' button
    And change nick to invalid nick
    And save changes
    Then users informations are not changed
    And the page is not changed

  Scenario: Change users password to invalid password
    When click 'edit' button
    And change password to invalid password
    And save changes
    Then users informations are not changed
    And the page is not changed

  Scenario: Change users password and type incorrect confirm password
    When click 'edit' button
    And change password
    And fill column confirm password incorrect
    And save changes
    Then users informations are not changed
    And the page is not changed
