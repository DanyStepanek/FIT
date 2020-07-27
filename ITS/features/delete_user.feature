Feature: Delete user from users

  Background: admin logged and actual page is users page
    Given admin is logged
    And actual page is users page
    And user list contains two users


  Scenario: Delete user as admin
    When user is selected
    And click 'delete' button
    Then user is deleted

  Scenario: Delete users without check any user in user list
    When no user is selected
    And click 'delete' button
    Then no user is deleted
