from selenium import webdriver

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "localhost:8988")
    driver = webdriver.Chrome(options=options)
    return driver