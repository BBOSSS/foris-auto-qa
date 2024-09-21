import time

import pytest
import requests
import uiautomator2 as u2
from pytest_bdd import scenario, given, when, then
from retry import retry

from setting.test_conf import TEST_CONF as CONF
from utils.u2_utils import check_exists, scroll_check_exists, click_wait


# Load all scenarios from the feature file
# scenarios("../features/weather_forecast_api.feature")

@scenario("../features/weather_forecast_api.feature", "Check the weather forecast for the day after tomorrow")
def test_9th_weather_forecast():
    pass


# Given Steps
@pytest.fixture(scope="session")
@given("weather forecast url")
def url():
    _url = "https://pda.weather.gov.hk/sc/locspc/data/fnd_uc.xml"
    return _url


# When Steps
@when("request weather forecast data", target_fixture="response_data")
def request_weather_forecast_data(url):
    json_data = _get_weather_forecast_data(url)
    # print(json_data)
    return json_data


# Then Steps
@then("get the weather forecast for the day after tomorrow")
def get_the_day_after_tomorrow_weather_forecast(response_data):
    assert response_data
    forecast_detail = response_data["forecast_detail"]
    assert forecast_detail and len(forecast_detail) > 1
    the_day_after_tomorrow_detail = forecast_detail[1]
    assert the_day_after_tomorrow_detail and len(the_day_after_tomorrow_detail) > 0
    print(the_day_after_tomorrow_detail)


@retry(tries=2)
def _get_weather_forecast_data(_url):
    headers = {
        "Host": "pda.weather.gov.hk",
    }
    response = requests.get(_url, headers=headers, timeout=30)
    if not response or response.status_code != 200:
        raise Exception(f"request {_url} failed: {response}")
    else:
        return response.json()
