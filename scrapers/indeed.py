import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils.google_sheets import get_or_create_worksheet, save_to_google_sheet

# Extract job details for each job listing
def enrich_job_details(driver, job):
    try:
        driver.get(job['url'])
        time.sleep(2)
        try:
            pay_element = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Pay"] span')
            job['pay'] = pay_element.text
        except NoSuchElementException:
            job['pay'] = "N/A"
        try:
            job_type_element = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Job type"] span')
            job['job_type'] = job_type_element.text
        except NoSuchElementException:
            job['job_type'] = "N/A"
        try:
            work_setting_element = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Work setting"] span')
            job['work_setting'] = work_setting_element.text
        except NoSuchElementException:
            job['work_setting'] = "N/A"
    except Exception as e:
        print(f"Error enriching job details: {e}")


# Extract job listings from the current page
def extract_jobs(driver):
    job_list = []
    try:
        job_list_elements = driver.find_elements(By.CSS_SELECTOR, 'li.css-1ac2h1w')
        print(f"Found {len(job_list_elements)} job listings.")
        for job_element in job_list_elements:
            try:
                job_url = job_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                job_title = job_element.find_element(By.CSS_SELECTOR, 'a span').text
                company_name = job_element.find_element(By.CSS_SELECTOR, 'span[data-testid="company-name"]').text
                job_list.append({'title': job_title, 'company': company_name, 'url': job_url})
            except NoSuchElementException:
                continue
    except Exception as e:
        print(f"Error extracting jobs: {e}")
    return job_list


# Main scraper logic
def scrape_indeed(driver, tab_name):
    worksheet = get_or_create_worksheet(tab_name)  # Creates or retrieves the specified worksheet

    base_url = "https://www.indeed.com/jobs"
    query = "q=frontend+or+backend+or+full+stack+or+ai+or+python+or+typescript+or+javascript+or+web+developer"
    params = "sc=0kf%3Aattr%28DSQF7%29%3B&fromage=7"
    start = 0
    page_number = 1

    while True:
        page_url = f"{base_url}?{query}&{params}&start={start}"
        driver.get(page_url)
        time.sleep(3)

        jobs = extract_jobs(driver)
        if not jobs:
            print("No more jobs found. Scraping complete.")
            break

        for job in jobs:
            enrich_job_details(driver, job)

        save_to_google_sheet(worksheet, jobs)
        print(f"Page {page_number} jobs processed for tab '{tab_name}'.")

        start += 10  # Move to the next page
        page_number += 1

    print(f"Scraping completed for tab '{tab_name}'.")
