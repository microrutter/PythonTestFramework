# PythonTestFramework

Currently creating documentation for this test suite using pycco. These are found in the docs folder


## Switches

-v = verbose so it will print out what it is doing

--junit-xml = prints out an xml report for junit mainly used for jenkins can be left out when running locally

-m = this is the mark lookup and will look for anything that matches the string after it

      e.g If you have marked a test with @pytest.mark.me to run just this test you would use -m me

--workers = This will run tests in parallel so if you put 4 after it it will run four tests at once

--html = this is just used to create an html report

-p used to tell pytest config to ignore things currently used to not print out warnings

--browser = which browser would you like to use (chrome and firefox for local options)

--url = what url would you like to hit

--ip = for selenium grid ignore if running locally

## pipenv ##

Have moved this project from requirements.txt to pipenv 
