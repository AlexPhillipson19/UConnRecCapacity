# this program opens the specific web page for the data, and actually runs the Javascript function using Selenium.
# this is necessary because the web page is dynamically updated using a Javascript function, and does not show
# a static value

import csv
import sys
import time
import datetime
import schedule
from time import sleep, ctime

import selenium
from schedule import Scheduler
from selenium import webdriver
from bs4 import BeautifulSoup

# Initialize our scheduler
from selenium.common.exceptions import InvalidArgumentException, WebDriverException

sched = Scheduler()

# the URL we want to pull data from
URL = "https://app.safespace.io/api/display/live-occupancy/86fb9e11?view=percent"


def writeData():
    # Specifying the driver's location that Selenium uses
    driver = webdriver.Chrome(r"C:\Webdriver\bin\chromedriver.exe")  # We are using Chrome, so that's where we path to

    # Make sure desired Web Page is online/able to be reached.
    try:
        driver.get(URL)
    except InvalidArgumentException or WebDriverException:
        sys.exit(1)

    # Wait for page to fully render //this was recommended by StackOverflow user MendelG
    sleep(5)

    # Pulling the updated (post-Javascript function) html from the simulated web page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Finds and sets the appropriate variable for our needs
    result = soup.find("span", {"id": "occupancyPct"}).text
    result = result[:-1]  # in this case, removes % sign from output

    # driver.quit() # closes the simulated web page
    driver.quit()

    # writes to the csv file
    with open('testData1.csv', mode='a') as csv_file:  # Opens the designated .csv file ; the mode parameter 'a'
        # allows us to append the current file instead of making a new one

        fieldnames = ['Date/Time', 'Percentage']  # In our case, we will not use this
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)  # Set up the writing func

        writer.writerow({'Date/Time': ctime(), 'Percentage': result})  # Writes the row. In this case, the first
        # column is the time, and the second column is our data

        print('Successfully printed')  # Used for Debug


# Call the function once at program execution
writeData()

# Note that Schedule starts the timer AFTER its do() function fully executes, which means if the do() function does not
# instantly execute, there will be a delay. This is why we have our time set to 282 instead of 300 seconds; this is a
# rough estimate that writeData() takes about 18 seconds to run completely
schedule.every(282).seconds.do(writeData)

# schedule.every(30).seconds.do(writeData) # Used for testing

# Runs our scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
