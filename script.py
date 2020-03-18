from selenium import webdriver

driver = webdriver.Firefox()

driver.set_window_size(200, 200)

driver.get("https://www.google.com")