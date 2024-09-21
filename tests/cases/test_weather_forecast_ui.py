import time

import pytest
import uiautomator2 as u2
from pytest_bdd import scenario, given, when, then
from retry import retry

from setting.test_conf import TEST_CONF as CONF
from utils.u2_utils import check_exists, scroll_check_exists, click_wait


# Load all scenarios from the feature file
# scenarios("../features/weather_forecast_ui.feature")

@scenario("../features/weather_forecast_ui.feature", "Check the weather forecast for the 9th day")
def test_9th_weather_forecast():
    pass


# Given Steps
@pytest.fixture(scope="session")
@given("connect phone")
def phone():
    serial = CONF["device_serial"]
    _phone = u2.connect_usb(serial)
    return _phone


@given("launch myobservatory app")
def launch_app(phone):
    app_name = CONF["package_name"]
    print(f"restart app: {app_name}")
    phone.app_stop(app_name)
    time.sleep(2)
    phone.app_start(app_name)
    time.sleep(5)


# When Steps
@when("skip launch ads")
def skip_launch_ads(phone):
    print("skip launch ads")
    # hko.MyObservatory_v1_0:id/exit_btn
    resource_id = get_resource_id("exit_btn")
    if not check_exists(phone, resourceId=resource_id):
        return
    phone.press("back")
    time.sleep(2)


@when("open 9-day weather forecast page")
def open_9day_weather_forecast_page(phone):
    open_weather_forecast_activity(phone)


# Then Steps
@then("get 9th day weather forecast detail info")
def get_9th_weather_forecast(phone):
    phone(scrollable=True).scroll.toEnd()
    time.sleep(2)
    info = {}

    element = _get_last_element(phone, "sevenday_forecast_date")
    assert element and element.info and element.info.get("text")
    info["date"] = element.info.get("text")

    element = _get_last_element(phone, "sevenday_forecast_day_of_week")
    assert element and element.info and element.info.get("contentDescription")
    info["week"] = element.info.get("contentDescription")

    element = _get_last_element(phone, "sevenday_forecast_temp")
    assert element and element.info and element.info.get("text")
    info["temperature"] = element.info.get("text")

    element = _get_last_element(phone, "sevenday_forecast_rh")
    assert element and element.info and element.info.get("text")
    info["relative_humidity"] = element.info.get("text")

    element = _get_last_element(phone, "psrText")
    assert element and element.info and element.info.get("text")
    info["probability_significant_rainfall"] = element.info.get("text")

    element = _get_last_element(phone, "sevenday_forecast_wind")
    assert element and element.info and element.info.get("text")
    info["wind"] = element.info.get("text")

    element = _get_last_element(phone, "sevenday_forecast_details")
    assert element and element.info and element.info.get("text")
    info["details"] = element.info.get("text")

    print(f"get_9th_weather_forecast: {info}")


def expand_navigate(_phone):
    print("expand navigate page")
    # hko.MyObservatory_v1_0:id/homepage_icon
    resource_id = get_resource_id("homepage_icon")
    # already expand navigate page
    if check_exists(_phone, tries=2, resourceId=resource_id):
        return
    desc = {
        "CN": "转到上一层级",
        "TC": "向上瀏覽",
        "EN": "Navigate up",
    }
    locator = dict(description=desc[CONF["language"]])
    if check_exists(_phone, **locator):
        click_wait(_phone, **locator)


def expand_forecast_warning_services(_phone):
    print("expand forecast warning services")
    text = {
        "CN": "预报及警告服务",
        "TC": "預報及警告服務",
        "EN": "Forecast & Warning Services",
    }
    locator = dict(text=text[CONF["language"]])
    if not scroll_check_exists(_phone, "down", tries=5, delay=2, **locator):
        raise Exception(f"element not exists: {locator}")

    desc = {
        "CN": "已隐藏",
        "TC": "已隱藏",
        "EN": "Collapsed",
    }
    if _phone(**locator).right(description=desc[CONF["language"]]):
        click_wait(_phone, **locator)


@retry(tries=3, delay=2)
def open_weather_forecast_activity(_phone):
    expand_navigate(_phone)
    expand_forecast_warning_services(_phone)

    print("open weather forecast activity")
    text = {
        "CN": "九天预报",
        "TC": "九天預報",
        "EN": "9-Day Forecast",
    }
    locator = dict(text=text[CONF["language"]])
    if not scroll_check_exists(_phone, "up", tries=5, delay=2, **locator):
        raise Exception(f"element not exists: {locator}")
    else:
        click_wait(_phone, **locator)

    # 9-Day Forecast has a certain chance of recognition error and needs to be retried
    text = {
        "CN": "天气预报",
        "TC": "天氣預報",
        "EN": "Weather Forecast",
    }
    locator = dict(text=text[CONF["language"]])
    if not check_exists(_phone, tries=2, **locator):
        raise Exception("open Weather Forecast Activity failed")


def get_resource_id(resource_id):
    return f"{CONF['package_name']}:id/{resource_id}"


def _get_last_element(_phone, _id):
    resource_id = get_resource_id(_id)
    elements = _phone(resourceId=resource_id)
    return elements[-1] if elements else None
