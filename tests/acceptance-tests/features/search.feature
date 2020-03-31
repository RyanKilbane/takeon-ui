Feature: Search function

  Background: Setting the correct url
    Given reference column is 1
    And period column is 2
    And survey column is 3

  Scenario Outline: Using an existing full reference entry
    Given a <reference> has been entered into the reference search input
    When it is submitted
    Then <reference> and <period> and <survey> will be displayed

    Examples:git
      | reference   | period | survey |
      | 49900000796 | 201903 | 0066   |
      | 49900000796 | 201906 | 0066   |


  Scenario Outline: Using a non-existing full reference entry
    Given a <reference> has been entered into the reference search input
    When it is submitted
    Then no table should appear

    Examples:
      | reference   |
      | 49900000999 |
      | 65900000103 |
      | 4998800105  |


  Scenario Outline: Searching using a partial reference
    Given a <partreference> has been entered into the reference search input
    When it is submitted
    Then <reference> and <period> and <survey> will be displayed

    Examples:
      | partreference | reference   | period | survey |
      | 499           | 49900000119 | 201712 | 0066   |
      | 103           | 49900000103 | 201712 | 0066   |
      | 011           | 49900000119 | 201712 | 0067   |


  Scenario Outline: Using an existing Survey id
    Given a <survey> has been entered into the survey search input
    When it is submitted
    Then <reference> and <period> and <survey> will be displayed
    Examples:
      | survey | reference   | period |
      | 0066   | 49900000119 | 201712 |
      | 0067   | 49900000119 | 201712 |

  Scenario Outline: Using an existing survey ID and reference
    Given a <survey> has been entered into the survey search input
    And a <reference> has been entered into the reference search input
    When it is submitted
    Then <reference> and <period> and <survey> will be displayed
    Examples:
      | survey | reference   | period |
      | 066    | 49900000100 | 201712 |
      | 067    | 49900000119 | 201712 |