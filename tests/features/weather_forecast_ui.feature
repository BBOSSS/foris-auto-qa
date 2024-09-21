Feature: Weather Forecast UI
  Tests 9-Day Weather Forecast

  Scenario: Check the weather forecast for the 9th day
    Given connect phone
    And launch myobservatory app
    When skip launch ads
    And open 9-day weather forecast page
    Then get 9th day weather forecast detail info