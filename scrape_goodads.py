import os
import json
from playwright.sync_api import sync_playwright

def scrape_and_screenshot(url, folder):
    # Ensure the output folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Initialize Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the given URL
        page.goto(url)

        # Wait for the page to load the necessary content
        page.wait_for_selector('.ad-card')

        # Extract all ad cards on the page
        ad_cards = page.query_selector_all('.ad-card')

        # Prepare the JSON data structure
        data = []
        print("Found ", len(ad_cards), " ad cards")
        for i, ad_card in enumerate(ad_cards):
            brand = ad_card.query_selector('.facebook_brand').inner_text() if ad_card.query_selector('.facebook_brand') else 'Unknown'
            cta_button = ad_card.query_selector('.cta_button .text-block-2').inner_text() if ad_card.query_selector('.cta_button .text-block-2') else 'Unknown'

            # Define screenshot file path
            screenshot_path = os.path.join(folder, f'ad_card_{i + 1}.png')
            ad_card = page.locator(".ad-card").nth(i)
            ad_card.scroll_into_view_if_needed()
            ad_card.screenshot(path=screenshot_path)
            data.append({
                "brand_name": brand,
                "screenshot_path": screenshot_path,
                "cta_button_text": cta_button
            })

        # Save the JSON data to a file
        json_file = os.path.join(folder, "ad_data.json")
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)

        # Close the browser
        browser.close()

        print(f"All screenshots and data saved to {folder}.")

if __name__ == "__main__":
    url = "https://www.greatads.co/?format-new=Image&platform-new=FB%20%26%20IG"
    output_folder = "./ad_screenshots"
    scrape_and_screenshot(url, output_folder)
