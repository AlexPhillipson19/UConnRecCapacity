# this program opens the specific web page for the data, and actually runs the Javascript function using Selenium.
# this is necessary because the web page is dynamically updated using a Javascript function, and does not show
# a static value

from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup

# the URL we want to pull data from
URL = "https://app.safespace.io/api/display/live-occupancy/86fb9e11?view=percent"

# Specifying the driver's location that Selenium uses
driver = webdriver.Chrome(r"C:\Webdriver\bin\chromedriver.exe")
driver.get(URL)

# Wait for page to fully render //this was recommended by a StackOverflow responder
sleep(5)

# Pulling the updated (post-Javascript function) html from the simulated web page
soup = BeautifulSoup(driver.page_source, "html.parser")

# Finds and prints/returns the appropriate variable for our needs (in this case, a percentage)
print(soup.find("span", {"id": "occupancyPct"}).text)


# driver.quit() # closes the simulated web page
driver.quit()