
import constants
import requests
import subprocess
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

stocksPerRow = 3
zoom = "75%"

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

indexes = ("Dow Jones Industrial Average", "Nasdaq", "S & P 500")

command = subprocess.Popen(["system_profiler", "SPDisplaysDataType"],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout, stderr = command.communicate()

stdout = str(stdout)
stdout = stdout[stdout.find("Resolution"): stdout.find("Framebuffer")]
width, height = re.findall('\d+', stdout)

driver = webdriver.Chrome(options=options)
driver.set_window_size(300, 400)

driver.set_window_position(250, 250)

driver.get("https://www.google.com/search?q=" + indexes[0])
driver.execute_script("window.scrollTo(200, 200)")
driver.execute_script("document.body.style.zoom='" + zoom + "'")

time.sleep(2)

driver.get("https://www.google.com/search?q=" + indexes[1])

#Figure out biggest mover from open
#Open windows and anchor them properly
#switch tabs
#Make Windows version, Linux for getting resolutuon
#Configuring drivers will be annoying
