# 🚩 QA Challenges
**Situation**:
Install an app (MyObservatory from Hong Kong Observatory) from google play store/apple
store. We want to automate the 9-day forecast page for the app in Android and/or IOS.

**Tech stacks**:
You can use any language (Python is preferred) or tools you feel comfortable with to
complete the tasks (task 1 + task 2).

**Task 1**:
Automate the App UI for below test case:
Check the 9th day’s weather forecast from 9-day forecast screen

**Task 2**:
The information from Task 1 (9-day forecast) is from Hong Kong Observatory API


## 📦 Environment Prepare
- **Python 3.9.2**
- **Python pip requirements**
```commandline
pip install -r requirements.txt
```
- **install atx-agent**
```commandline
python -m uiautomator2 init
```
- **start weditor**
```commandline
python -m weditor
```


## 🌟 Prerequisites
- **install myobservatory app**
```commandline
adb install resource/MyObservatory_5.9.apk
```
- **grant all permissions required by the app**


## Run test
- **ui test**
```commandline
pytest tests/cases/test_weather_forecast_ui.py -v -s
```
- **api test**
```commandline
pytest tests/cases/test_weather_forecast_api.py -v -s
```