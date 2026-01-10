import requests

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

