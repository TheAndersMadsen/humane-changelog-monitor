import json
import re
import time
from datetime import datetime

import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

def get_latest_update(url):
    """
    Retrieves the latest update from the specified URL.

    Args:
        url (str): The URL to fetch the latest update from.

    Returns:
        str: The text content of the latest update.
    """
    response = requests.get(url, verify=False)  # Send a GET request to the specified URL
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    return response.json()["pageProps"]["content"]  # Extract the update content from the JSON response

def post_update(webhook_url, update):
    """
    Posts an update to the specified webhook URL.

    Args:
        webhook_url (str): The URL of the webhook to post the update to.
        update (dict): The update content to be posted.
    """
    requests.post(webhook_url, json=update)  # Send a POST request to the webhook URL with the update content

def load_posted_updates(filename):
    """
    Loads the previously posted updates from a JSON file.

    Args:
        filename (str): The name of the JSON file to load posted updates from.

    Returns:
        list: A list of previously posted update dates.
    """
    try:
        with open(filename, "r") as file:  # Open the JSON file in read mode
            return json.load(file)  # Load the contents of the file as a list
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist

def save_posted_updates(filename, posted_updates):
    """
    Saves the list of posted update dates to a JSON file.

    Args:
        filename (str): The name of the JSON file to save posted updates to.
        posted_updates (list): A list of posted update dates.
    """
    with open(filename, "w") as file:  # Open the JSON file in write mode
        json.dump(posted_updates, file)  # Write the list of posted updates to the file

def parse_update_content(content):
    """
    Parses the update content and extracts relevant information.

    Args:
        content (str): The raw update content.

    Returns:
        list: A list of dictionaries representing the parsed updates.
    """
    pattern = r'<h2>(.*?)</h2>(.*?)(?=<h2>|$)'  # Regular expression pattern to match update sections
    matches = re.findall(pattern, content, re.DOTALL)  # Find all matches of the pattern in the content

    updates = []
    for match in matches:
        date = match[0]  # Extract the date from the matched section
        update_content = ""
        update_sections = re.findall(r'<li>(?:<strong>(.*?)</strong>)?(.*?)</li>', match[1], re.DOTALL)  # Find all update items within the section

        for section in update_sections:
            title = section[0].replace("&#x26;", "&").replace(";", "").strip()  # Extract the title and replace HTML entities
            if title:
                update_content += f"{title}\n"  # Add the title to the update content

            content = re.sub(r'<.*?>', '', section[1]).strip()  # Remove HTML tags from the content
            if content:
                update_content += f"- {content.replace('&#x26;', '&').replace(';', '')}\n"  # Add the content as a bullet point
            else:
                updates = re.findall(r'<li>(.*?)</li>', section[1])  # Find individual update items
                for update in updates:
                    update_content += f"- {update.replace('&#x26;', '&').replace(';', '')}\n"  # Add each update item as a bullet point

        if update_content:
            updates.append({"date": date, "content": update_content})  # Append the parsed update to the list of updates

    return updates

def main(webhook_url, updates_url, check_interval=600):
    """
    Main function that continuously checks for updates and posts them to the webhook.

    Args:
        webhook_url (str): The URL of the webhook to post updates to.
        updates_url (str): The URL to fetch updates from.
        check_interval (int, optional): The interval (in seconds) between each update check. Defaults to 600.
    """
    posted_updates_file = "posted_updates.json"  # File to store posted update dates
    posted_updates = load_posted_updates(posted_updates_file)  # Load previously posted update dates

    while True:
        try:
            latest_update_content = get_latest_update(updates_url)  # Retrieve the latest update content
            updates = parse_update_content(latest_update_content)  # Parse the update content

            for update in updates:
                date = update["date"]  # Extract the date from the update
                if date not in posted_updates:  # Check if the update has not been posted before
                    post_update(webhook_url, {"content": f"**{date}**\n{update['content']}"})  # Post the update to the webhook
                    posted_updates.append(date)  # Add the date to the list of posted updates
                    save_posted_updates(posted_updates_file, posted_updates)  # Save the updated list of posted updates

        except Exception as e:
            print(f"An error occurred: {e}")  # Print any errors that occur

        time.sleep(check_interval)  # Wait for the specified interval before checking for updates again

if __name__ == "__main__":
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")  # Get the Discord webhook URL from .env file
    updates_url = os.getenv("HUMANE_CHANGELOG_URL")  # Get the Humane changelog URL from .env file
    main(webhook_url, updates_url)  # Call the main function with the retrieved URLs