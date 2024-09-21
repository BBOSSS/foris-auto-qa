Feature: Weather Forecast API
  Tests the day after tomorrow weather forecast

  Scenario: Check the weather forecast for the day after tomorrow
    Given weather forecast url
    When request weather forecast data
    Then get the weather forecast for the day after tomorrow