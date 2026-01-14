import requests
from datetime import datetime
import os

class Downloader:
    # Choice between "Zip", "queens", "Tango"
    def cleanup(self, filename):
        os.remove(filename)


    def download_image(self, choice: str):
        """
        choice can be of: "Zip", "queens", "Tango"
        """

        REFERENCE_DATE = datetime(2026, 1, 9)
        if choice == "Zip":
            REFERENCE_NUMBER = 298
        elif choice == "queens":
            REFERENCE_NUMBER = 619
        elif choice == "Tango":
            REFERENCE_NUMBER = 459
        else:
            REFERENCE_NUMBER = 0

        today = datetime.now().date()
        today_dt = datetime.combine(today, datetime.min.time())

        days_diff = (today_dt - REFERENCE_DATE).days

        today_number = REFERENCE_NUMBER + days_diff

        base_url = f"https://tryhardguides.com/wp-content/uploads/2025/05/{choice}-answer-"
        image_url = f"{base_url}{today_number}.jpg"

        filename = f"zip_answer_{today_number}.png"

        print(f"Today's date: {today.strftime('%Y-%m-%d')}")
        print(f"LinkedIn ZIP Puzzle number: #{today_number}")
        print(f"Downloading from: {image_url}\n")


        success = download_helper(image_url, filename)
        
        if not success:
            print("\nTip: Try running again later – TryHardGuides usually uploads early in the day.")
            print("You can also check manually: https://tryhardguides.com/linkedin-zip-answer-today/")
            return None

        return filename

def download_helper(url, save_as):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=12)
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type:
                print(f"Warning: Response is not an image (Content-Type: {content_type})")
                return False
            
            with open(save_as, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Successfully saved: {save_as}")
            print(f"File size: {len(response.content) / 1024:.1f} KB")
            return True
        
        else:
            print(f"Failed – HTTP {response.status_code}")
            if response.status_code == 404:
                print("Puzzle image for today may not be uploaded yet.")
            return False
            
    except Exception as e:
        print(f"Download error: {e}")
        return False



