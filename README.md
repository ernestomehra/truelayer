# truelayer - api automation project

## Overview

This test automation suite, is created using pytest framework to automate APIs: 

- `https://api.wheretheiss.at/v1/satellites/<id>/positions`
- `https://api.wheretheiss.at/v1/satellites/<id>/tle`

## How to setup locally and run tests? 
Pre-Requisites:
- Python version 3.5+ installed.
- Git is configured
- MacOS v10.5+

Steps:

- Take a clone of the repo: `git clone git@github.com:ernestomehra/truelayer.git`
- CD into the project root, and create a virtual environment using: `python3 -m venv venv`
- Activate the environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- In the terminal, run command `pytest -s` to run all tests in side the `test/` dir 

Note: To create an HTML report for every test run, run `pytest --html=report-html` I have committed an example 
report.html, this should not be committed to the repo on a live project, only here for the demo purpose.

### Custom Test Suites:

To run custom test classes, simply run pytest <path to the testfile.py> For eg: pytest tests/test_positions.py would 
run test classes inside this file only.

## Issues found while working with the API endpoints:

1. No documented detail around the timestamp timezone - it is GMT, found by watching the headers returned/hit and trial.
2. Time Zones are not easy to decode; these are epoch times.
3. While trying negative tests, using the POST http\ method for a request where only GET is required, we do not see an 
intuitive error. The error received is: 
`
{
   "error": "authorization required",
   "status": 401
}`

4. According to the documentation, the positions are returned up to 10 timestamps, but the detail is returned for 
more than 10 i.e. 20 timestamps as well. So, this test will explicitly fail in my test suite, to indicate an issue. 

5. Suppose, the timestamp is set at 0.90 , the result is returned for the timestamp 0, although I think it should be 
rounded off to 1. 
   
   
## Future Enhancements for the framework
   
1. Implement a more interactive, data-driven reporting approach.
2. Implement markers for the individual tests, that will help execution for smoke, sanity and regression tests.
3. Implement performance testing for both the API endpoints, using an open source tool like blazemeter or locus.py
