Feature: Edit user in users

Background: admin logged and actual page is users page
  Given admin is logged
  And actual page is users page


Scenario: Edit user as admin
  When click 'edit' button
  And edit some columns correctly
  And save changes
  Then users informations are actualized


Scenario: Change user group
  Given there are two or more user groups
  When click 'edit' button
  And change group
  And save changes
  Then user is in another group

Scenario: Change users <column> to invalid <column>
  When click 'edit' button
  And change <column> to invalid <column>
  And save changes
  Then users informations are not changed

Examples: Type_of_information
  | column           |
  | email            |
  | nick             |
  | password         |

Scenario: Change users password and type incorrect confirm password
  When click 'edit' button
  And change password
  And fill column confirm password incorrect
  And save changes
  Then users informations are not changed
