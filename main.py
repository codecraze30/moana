from scrapers.indeed import scrape_indeed
from scrapers.ziprecruiter import scrape_ziprecruiter
from scrapers.rocketship import scrape_remoterocketship
from utils.driver import setup_driver

# Main script to execute scraping tasks
if __name__ == "__main__":
    # Setup the Selenium WebDriver
    driver = setup_driver()

    try:
        # Perform scraping for Indeed
        # scrape_indeed(driver, "Indeed1")

        # Perform scraping for Ziprecruiter
        # scrape_ziprecruiter(driver, "ZipRecruiter")

        # Perform scraping for Ziprecruiter
        scrape_remoterocketship("Rocket")


    finally:
        # Close the driver after scraping
        driver.quit()
