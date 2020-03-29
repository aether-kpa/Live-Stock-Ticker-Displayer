
import constants
import requests
import subprocess
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


class StockScreener:

    def __init__(self, driver: webdriver.Chrome, stocks: tuple, indexes: tuple, key: str, zoom: str, time: float,
                 monitorWidth: int, monitorHeight: int):

        assert len(stocks) > 0  # Make sure at least one stock is in the list

        # Variables passed through constructor
        self.driver = driver
        self.stocks = stocks  # Stocks in watchlist
        self.indexes = indexes  # Indexes in watchlist
        self.zoom = zoom
        self.sleepTime = time

        # Variables decided on startup
        self.stocksPerRow = 3
        self.numberOfBiggestMoversDisplayed = 3  # Number of biggest movers that can be displayed on monitor
        self.windowWidth = 500
        self.windowHeight = 475
        self.os = ""
        self.monitorWidth = monitorWidth
        self.monitorHeight = monitorHeight
        self.percentChanges = {}  # Dictionary of percent change from close to open corresponding to stock
        self.biggestMovers = []  # List of biggest movers that will be shown onscreen

        # Constants
        self.GOOGLE_LINK = "https://www.google.com"
        self.GOOGLE_LINK_FOR_QUERY = "https://www.google.com/search?q="
        self.KEY = key  # Use IEX instead of AlphaVantage because IEX gives us 50,000 free monthly API calls :)

    # Main function
    def run(self) -> None:

        self.openWindows()
        self.positionAndSizeWindows()

        # Switch to each window and search for a stock
        for index in range(len(self.stocks)):
            self.driver.switch_to.window(self.driver.window_handles[index])
            self.driver.get(self.GOOGLE_LINK_FOR_QUERY + self.stocks[index])

        self.changeView()

    def openWindows(self) -> None:

        action = ActionChains(self.driver)

        self.driver.get(self.GOOGLE_LINK_FOR_QUERY + "Google")
        link = self.driver.find_element_by_partial_link_text("Google")

        # Click + Shift on a link to make new windows
        for stock in self.stocks:
            action.key_down(Keys.SHIFT).perform()
            link.click()
            action.key_up(Keys.SHIFT).perform()

            time.sleep(self.sleepTime)

    # Position the windows and make them the appropriate size
    def positionAndSizeWindows(self) -> None:

        currentX = 0
        currentY = 0

        for window in self.driver.window_handles:

            self.driver.switch_to.window(window)
            self.driver.set_window_size(self.windowWidth, self.windowHeight)  # 500 x 375 is minimum size for Chrome
            self.driver.set_window_position(currentX, currentY)

            currentX += self.windowWidth

            if currentX + self.windowWidth > self.monitorWidth:
                currentX = 0
                currentY += self.windowHeight

    # Scroll and zoom in on window to make chart fit screen
    def changeView(self) -> None:

        for window in self.driver.window_handles:
            self.driver.switch_to.window(window)

            self.driver.execute_script("document.body.style.zoom='" + self.zoom + "'")

            element = self.driver.find_element_by_class_name("aviV4d")  # aviV4d = class Google uses for their charts
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def setMonitorResolution(self) -> None:  # Is all this extra work really needed?

        if self.os == "Mac":
            command = subprocess.Popen(["system_profiler", "SPDisplaysDataType"],
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # Run Bash command
            stdout, stderr = command.communicate()

            stdout = str(stdout)
            stdout = stdout[stdout.find("Resolution"): stdout.find("Framebuffer")]  # Use Regex to get values
            self.monitorWidth, self.monitorHeight = re.findall('\d+', stdout)

            # MAKE RESOLUTION GETTER FOR WINDOWS AND LINUX

    def setOperatingSystem(self) -> None:  # Is all this extra work really needed?
        self.os = "Mac"

        # GET OS FOR OTHER OS's

    # Store overnight percent change for each stock in watchlist
    def setPercentChanges(self) -> None:

        for stock in self.stocks:
            json = requests.get("https://cloud.iexapis.com/stable/stock/" + stock + "/quote?token=" + self.KEY).json()

            previousClose = float(json["previousClose"])
            open = float(json["open"])

            percentChange = (open - previousClose) / previousClose

            self.percentChanges.update({stock: percentChange})

    # From the dictionary created above, get the tickers for the N biggest changes
    def setBiggestMovers(self) -> None:

        for count in range(self.numberOfBiggestMoversDisplayed):
            maximum = 0

            for key, value in self.percentChanges.items():
                if abs(value) > maximum:
                    if key not in self.biggestMovers:  # If the ticker wasn't already found to be the biggest mover
                        maximum = value
                        stock = key

            self.biggestMovers.append(stock)

    #switch to new window handle
    # set the size and pos of the new widow using the handle

    #Figure out biggest mover from open
    #Open windows and anchor them properly
    #switch tabs
    #Configuring drivers will be annoying
    #Write out resolution and OS to JSON file
    #Set up Tools


    # Flow -> Determine number of windows to open -> Determine where they should be opened -> Open windows, calculate stocks we can fit, if number of stocks in watchlist is greater than ones we can fit determine biggest movers and make new windows for those, for the other ones make them cycle through

# -------------------------------------------------------------------------------------------------------------------

PATH = True
onRaspberryPi = False

watchlist =  ("BA", "AMZN", "AAPL", "TWTR", "F", "GM")
indexes = ("Dow Jones Industrial Average", "Nasdaq", "S & P 500")

# Take out annoying top bar in Chrome that warns it's being used under automation
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Driver is made outside of class because it needs to stay in scope for Chrome windows to remain open
if PATH:
    chrome = webdriver.Chrome(options=options)
else:
    chrome = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", options=options)

if onRaspberryPi:
    screener = StockScreener(chrome,
                             watchlist,
                             indexes,
                             constants.iexKey, "75%", 1, 1680, 1050)
else:
    screener = StockScreener(chrome,
                             watchlist,
                             indexes,
                             constants.iexKey, "75%", 0, 1440, 900)


#screener.setOperatingSystem()
#screener.setMonitorResolution()
screener.run()
#screener.setPercentChanges()
#screener.setBiggestMovers()
