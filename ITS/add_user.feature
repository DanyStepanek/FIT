Feature: Add user to users

Background: admin logged and actual page is users page
  Given admin is logged
  And actual page is users page


Scenario: Add user as admin
  When click 'add new' button
  And fill all required columns correctly
  And save changes
  Then user is added and shown in table of users


Scenario: Add user with the same nick
  When click 'add new' button
  And fill all required columns correctly
  And set nick as already used nick in current user group
  And save changes
  Then user is not added

Scenario: Add user with the same nick to another user group
  When click 'add new' button
  And fill all required columns correctly
  And set nick as already used nick in another user group
  And save changes
  Then user is added and shown in table of users


Scenario: Add user with invalid <column>
  When click 'add new' button
  And fill all required columns correctly except <column>
  And save changes
  Then user is not added

Examples: Type_of_information
  | column           |
  | email            |
  | nick             |
  | password         |


Scenario: Add user with valid password but with incorrect confirm password
  When click 'add new' button
  And fill all required columns correctly except confirm password
  And save changes
  Then user is not added
