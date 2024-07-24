import requests
import json
import datetime
import os
import glob
import logging

# Imperva API details
IMPERVA_API_ID = 'your_imperva_api_id'
IMPERVA_API_KEY = 'your_imperva_api_key'
IMPERVA_API_URL = 'https://my.imperva.com/api/prov/v1/sites/list'

# Logging setup
log_folder = '/var/log/imperva'
log_file = os.path.join(log_folder, 'backup.log')
os.makedirs(log_folder, exist_ok=True)
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')

# Function to get site configuration from Imperva
def get_imperva_sites(api_id, api_key):
    headers = {
        'x-api-id': api_id,
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    response = requests.post(IMPERVA_API_URL, headers=headers)
    if response.status_code == 200:
        logging.info("Fetched Imperva sites successfully.")
        return response.json()
    else:
        logging.error(f"Error fetching Imperva sites: {response.status_code} - {response.text}")
        return None

# Function to save configuration to a file
def save_configuration_to_file(configuration, filename):
    with open(filename, 'w') as file:
        json.dump(configuration, file, indent=4)
    logging.info(f"Configuration saved to {filename}")

# Function to delete backups older than 7 days
def delete_old_backups(folder, days=7):
    now = datetime.datetime.now()
    for filename in glob.glob(os.path.join(folder, "imperva_site_configuration_backup_*.json")):
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        if (now - file_time).days > days:
            os.remove(filename)
            logging.info(f"Deleted old backup: {filename}")

def main():
    # Fetch Imperva site configuration
    configuration = get_imperva_sites(IMPERVA_API_ID, IMPERVA_API_KEY)
    if configuration:
        # Generate a filename with the current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        backup_folder = "/opt/imperva/backup"
        os.makedirs(backup_folder, exist_ok=True)
        filename = os.path.join(backup_folder, f"imperva_site_configuration_backup_{current_date}.json")
        # Save configuration to a file
        save_configuration_to_file(configuration, filename)
        # Delete old backups
        delete_old_backups(backup_folder)

if __name__ == '__main__':
    main()
