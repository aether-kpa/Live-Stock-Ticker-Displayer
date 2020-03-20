
import constants
import requests
import subprocess
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


# Take out annoying top bar in Chrome that warns it's being used under automation
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Driver is made outside of class because it needs to stay in scope for Chrome windows to remain open
chrome = webdriver.Chrome(options=options)


class StockScreener:

    def __init__(self, driver: webdriver.Chrome):

        # Variables passed through constructor
        self.driver = driver

        # Variables decided on startup
        self.zoom = "75%"
        self.stocksPerRow = 3
        self.windowWidth = 0
        self.windowHeight = 0
        self.os = ""
        self.monitorWidth = 0
        self.monitorHeight = 0

        # Variables changed during program's runtime
        self.query = "Google"
        self.currentWindow = ""

        # Constants
        self.INDEXES = ("Dow Jones Industrial Average", "Nasdaq", "S & P 500")
        self.GOOGLE_LINK = "https://www.google.com"
        self.GOOGLE_LINK_FOR_QUERY = "https://www.google.com/search?q="

    def run(self):

        self.driver.set_window_size(300, 400)
        self.driver.set_window_position(0, 0)

        self.driver.get(self.GOOGLE_LINK_FOR_QUERY + self.query)
        self.driver.execute_script("window.scrollTo(200, 200)")
        self.driver.execute_script("document.body.style.zoom='" + self.zoom + "'")

        time.sleep(3)

        self.currentWindow = self.driver.current_window_handle

        link = self.driver.find_element_by_partial_link_text("Google")

        action = ActionChains(self.driver)
        action.key_down(Keys.SHIFT).perform()

        link.click()

        action.key_up(Keys.SHIFT).perform()

        self.driver.get(self.GOOGLE_LINK_FOR_QUERY + self.INDEXES[0])

        # time.sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.set_window_size(300, 400)
        self.driver.set_window_position(300, 0)

        self.driver.get(self.GOOGLE_LINK_FOR_QUERY + self.INDEXES[1])

    def openWindows(self):
        pass

    def setMonitorResolution(self):

        if self.os == "Mac":
            command = subprocess.Popen(["system_profiler", "SPDisplaysDataType"],
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # Run Bash command
            stdout, stderr = command.communicate()

            stdout = str(stdout)
            stdout = stdout[stdout.find("Resolution"): stdout.find("Framebuffer")]  # Use Regex to get values
            self.monitorWidth, self.monitorHeight = re.findall('\d+', stdout)

            # MAKE RESOLUTION GETTER FOR WINDOWS AND LINUX

    def setOperatingSystem(self):
        self.os = "Mac"


    #switch to new window handle
    # set the size and pos of the new widow using the handle

    #Figure out biggest mover from open
    #Open windows and anchor them properly
    #switch tabs
    #Configuring drivers will be annoying


screener = StockScreener(chrome)

screener.setOperatingSystem()
screener.setMonitorResolution()
screener.run()