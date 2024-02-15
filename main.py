import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# URL of the Fortnite player profile
url = 'https://fortnitetracker.com/profile/all/2024%20rxlin'

# Function to scrape rank data from the URL using Selenium
def scrape_rank_data():
    try:
        # Configure Chrome WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        # Wait for the rank element to be visible
        rank_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.profile-rank__value'))
        )
        rank_progress_element = driver.find_element_by_css_selector('.profile-rank-progress')
        # Extract rank and progress text
        rank = rank_element.text.strip()
        rank_progress = rank_progress_element.text.strip()
        # Close the WebDriver
        driver.quit()
        return rank, rank_progress
    except Exception as e:
        print(f"An error occurred: {e}")
        return "N/A", "N/A"

# Function to create or update a GitHub Gist
def create_or_update_gist(rank_data, gist_url):
    try:
        # Gist data
        gist_data = {
            "description": "Fortnite Player Rank Data",
            "public": True,
            "files": {
                "rank.txt": {
                    "content": rank_data
                }
            }
        }
        # If Gist URL is provided, extract Gist ID
        gist_id = gist_url.split('/')[-1]
        # Gist API endpoint
        gist_api_url = f"https://api.github.com/gists/{gist_id}"
        # If GIST_ID environment variable exists, update the existing Gist
        response = requests.patch(gist_api_url, json=gist_data)
        # Check response status
        if response.status_code == 200:
            print(f"Gist updated successfully. Gist ID: {gist_id}")
            return gist_id
        else:
            print(f"Failed to update Gist. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Main function
def main():
    # Gist URL
    gist_url = 'https://gist.github.com/DeveloperRadleighPompei/75c476a3fc46d5402e33e3134cc0dc16'
    while True:
        # Scrape rank data
        rank, rank_progress = scrape_rank_data()
        # Format rank data
        rank_data = f"Rank: {rank}\nProgress: {rank_progress}"
        # Update Gist with rank data
        create_or_update_gist(rank_data, gist_url)
        # Wait for some time before scraping again (e.g., every hour)
        time.sleep(3600)

if __name__ == "__main__":
    main()
