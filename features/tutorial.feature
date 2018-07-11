Feature: showing off behave

  Scenario: run a simple test
     Given we have behave installed
      When we implement a test
      Then behave will test it for us!

Feature: context.text
    Scenario: some scenario
    Given a sample text loaded into the frobulator
        """
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
        eiusmod tempor incididunt ut labore et dolore magna aliqua.
        """
    When we activate the frobulator
    Then we will find it similar to English

Feature: context.table
    Scenario: some scenario
  Given a set of specific users
     | name      | department  |
     | Barry     | Beer Cans   |
     | Pudey     | Silly Walks |
     | Two-Lumps | Silly Walks |

 When we count the number of people in each department
 Then we will find two people in "Silly Walks"
  But we will find one person in "Beer Cans"

    """python
    @given('a set of specific users')
    def step_impl(context):
        for row in context.table:
        model.add_user(name=row['name'], department=row['department'])
    """

Feature: Response
    Scenario: look up a book
    Given I search for a valid book
    Then the result page will include "success"

    Scenario: look up an invalid book
    Given I search for a invalid book
    Then the result page will include "failure"