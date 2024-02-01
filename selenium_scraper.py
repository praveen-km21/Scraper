from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import os
from datetime import datetime

# Set up WebDriver
driver = webdriver.Chrome()
driver.implicitly_wait(10)

# The URL for LinkedIn job search results
# url = 'https://www.linkedin.com/jobs/search?keywords=Chatbot%20Development&location=United%20States&locationId=&geoId=103644278&f_TPR=r86400&f_JT=C&f_WT=2&position=1&pageNum=0'

url = input("Please enter a URL: \n")

# Navigate to the URL
driver.get(url)

# Initialize lists to store scraped data
job_titles = []
job_urls = []
company_names = []
company_urls = []

# Find all 'li' elements that represent job cards
job_listings = driver.find_elements(By.CSS_SELECTOR, 'ul.jobs-search__results-list li')

# Iterate over each listing and extract data
for listing in job_listings:
    # Extract the job title and URL
    try:
        job_title_element = listing.find_element(By.CSS_SELECTOR, 'h3.base-search-card__title')
        job_titles.append(job_title_element.text)
        job_url_element = listing.find_element(By.CSS_SELECTOR, 'a.base-card__full-link')
        job_urls.append(job_url_element.get_attribute('href'))
    except Exception as e:
        print("Error extracting job title and URL:", e)
        job_titles.append(None)
        job_urls.append(None)
    
    # Extract the company name and URL
    try:
        company_name_element = listing.find_element(By.CSS_SELECTOR, 'h4.base-search-card__subtitle')
        company_names.append(company_name_element.text)
        company_url_element = listing.find_element(By.CSS_SELECTOR, 'a.hidden-nested-link')
        company_urls.append(company_url_element.get_attribute('href'))
    except Exception as e:
        print("Error extracting company name and URL:", e)
        company_names.append(None)
        company_urls.append(None)

# Close the WebDriver
driver.quit()

# Create a DataFrame from the scraped data
jobs_df = pd.DataFrame({
    'Job Title': job_titles,
    'Job URL': job_urls,
    'Company Name': company_names,
    'Company URL': company_urls
})

# Display the DataFrame
print(jobs_df)

current_date = datetime.now().strftime("%d-%m-%Y")

# Define the base directory and the new folder name
base_directory = "D:/scraper/scraped_data"
new_folder = os.path.join(base_directory, current_date)

# Create the new folder if it doesn't exist
if not os.path.exists(new_folder):
    os.makedirs(new_folder)
# Save the DataFrame to an Excel file
# Prompt user for a file name
file_name = input("Please enter a file name for the Excel file (without extension): ")
jobs_df.to_excel(os.path.join(new_folder, f"{file_name}.xlsx"), index=False)
print(f"Data saved to {file_name}.xlsx")
