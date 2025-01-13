import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils.google_sheets import get_or_create_worksheet, save_to_google_sheet

# Extract job listings from the current page
def extract_jobs(driver):
    job_list = []
    try:
        # Locate all job containers
        job_list_elements = driver.find_elements(By.CSS_SELECTOR, 'div.job_result_two_pane')
        print(f"Found {len(job_list_elements)} job listings.")
        
        # Iterate over each job container
        for job_element in job_list_elements:
            try:
                # Job title
                job_title = job_element.find_element(By.CSS_SELECTOR, 'h2 a').text

                # Job URL
                job_url = job_element.find_element(By.CSS_SELECTOR, 'h2 a').get_attribute('href')

                # Company name
                company_name = job_element.find_element(By.CSS_SELECTOR, '[data-testid="job-card-company"]').text

                # Company location (used for work setting in some cases)
                location_element = job_element.find_element(By.CSS_SELECTOR, '[data-testid="job-card-location"]')
                company_location = location_element.text.strip()

                # Salary
                try:
                    salary = job_element.find_element(By.CSS_SELECTOR, 'div.mr-8 p.text-primary').text
                except NoSuchElementException:
                    salary = "N/A"

                # Work setting (e.g., Remote, On-site)
                try:
                    work_setting = location_element.text.split("•")[-1].strip()  # Extract after "•"
                except NoSuchElementException:
                    work_setting = "N/A"

                # Job type (e.g., Full-time, Part-time)
                try:
                    job_type = job_element.find_element(By.XPATH, ".//p[contains(text(), 'Full-time') or contains(text(), 'Part-time')]").text
                except NoSuchElementException:
                    job_type = "N/A"

                # Append to job_list
                job_list.append({
                    'title': job_title,
                    'company': company_name,
                    'pay': salary,
                    'job_type': job_type,
                    'work_setting': work_setting,
                    'url': job_url
                })
            except Exception as e:
                print(f"Error extracting data for a job: {e}")
    except Exception as e:
        print(f"Error extracting jobs from page: {e}")

    return job_list

# Main scraper logic
def scrape_ziprecruiter(driver, tab_name):
    worksheet = get_or_create_worksheet(tab_name)
    base_url = "https://www.ziprecruiter.com/jobs-search"
    query = "search=frontend+or+backend+or+full+stack+or+ai+or+python+or+typescript+or+javascript+or+web+developer"
    params = "location=United+States&refine_by_location_type=only_remote&days=1&refine_by_employment=employment_type%3Aall&refine_by_salary=&refine_by_salary_ceil=&lvk=qF-_MGKAqOTLN0zYIYInkQ.--NdvVZ0bl7"

    page_number = 1  # Start from the first page

    while True:
        # Dynamically build the page URL
        page_url = f"{base_url}?{query}&{params}&page={page_number}"
        print(f"Scraping page {page_number}: {page_url}")

        driver.get(page_url)
        time.sleep(3)  # Allow the page to load

        # Extract job listings from the current page
        jobs = extract_jobs(driver)
        if not jobs:
            print(f"No more jobs found on ZipRecruiter. Scraping complete at page {page_number}.")
            break

        # Save the extracted jobs to Google Sheets
        save_to_google_sheet(worksheet, jobs)
        print(f"All jobs saved to the '{tab_name}' tab.")

        print(f"Page {page_number} jobs processed.")
        page_number += 1  # Move to the next page

    print(f"Scraping completed for tab '{tab_name}'.")
