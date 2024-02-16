import os
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
        # Wait for the rank elements to be visible
        rank_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#overview > div.trn-grid.trn-grid__sidebar-right > aside > div.trn-grid.trn-grid--vertical > div.profile-current-ranks.trn-card.trn-card--no-overflow > div > div:nth-child(1) > div.profile-rank__container > div > div.profile-rank__value'))
        )
        rank_progress_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#overview > div.trn-grid.trn-grid__sidebar-right > aside > div.trn-grid.trn-grid--vertical > div.profile-current-ranks.trn-card.trn-card--no-overflow > div > div:nth-child(1) > div.profile-rank__container > div > div.profile-rank-progress'))
        )
        rank_image_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#overview > div.trn-grid.trn-grid__sidebar-right > aside > div.trn-grid.trn-grid--vertical > div.profile-current-ranks.trn-card.trn-card--no-overflow > div > div:nth-child(1) > div.profile-rank__container > img")))
        # Extract rank and progress text
        rank = rank_element.text.strip()
        rank_progress = rank_progress_element.text.strip()
        rank_image = rank_image_element.get_attribute("src")  # Get the 'src' attribute of the image element
        number_rank = float(rank_progress.strip('%'))
        # Close the WebDriver
        driver.quit()
        return rank, rank_progress, rank_image, number_rank
    except Exception as e:
        print(f"An error occurred: {e}")
        return "N/A", "N/A", "N/A", "N/A"  # Return default values in case of error

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
        # Gist URL
        gist_id = gist_url.split('/')[-1]
        # Gist API endpoint
        gist_api_url = f"https://api.github.com/gists/{gist_id}"
        # Personal Access Token
        token = "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"  # Use environment variable for token
        headers = {'Authorization': f'token {token}'}
        
        # Check if the Gist already exists
        response = requests.get(gist_api_url, headers=headers)
        if response.status_code == 200:  # Gist exists, update it
            response = requests.patch(gist_api_url, headers=headers, json=gist_data)
            print(f"Gist updated successfully. Gist ID: {gist_id}")
            return gist_id
        elif response.status_code == 404:  # Gist doesn't exist, create it
            response = requests.post("https://api.github.com/gists", headers=headers, json=gist_data)
            print(f"Gist created successfully. Gist ID: {gist_id}")
            return gist_id
        else:
            print(f"Failed to create/update Gist. Status code: {response.status_code}")
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
        rank, rank_progress, rank_image, number_rank = scrape_rank_data()
        # Format rank data
        rank_data = f"Rank: {rank}\nProgress: {rank_progress}\nRank Image: {rank_image}\nNumber Rank: {number_rank}"
        # Update Gist with rank data
        create_or_update_gist(rank_data, gist_url)
        # Wait for some time before scraping again (e.g., every hour)
        time.sleep(3600)  # Wait for an hour

if __name__ == "__main__":
    main()
