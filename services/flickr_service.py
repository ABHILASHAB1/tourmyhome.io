import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class FlickrService:
    """
    A service class to interact with the Flickr API for fetching images.
    Useful for seeding a marketplace database with high-quality, relevant images.
    """
    
    BASE_URL = "https://www.flickr.com/services/rest/"
    
    def __init__(self):
        self.api_key = os.getenv("FLICKR_API_KEY")
        if not self.api_key or self.api_key == "your_api_key_here":
            print("WARNING: FLICKR_API_KEY is not set in .env. Image fetching will fail.")
            
    def search_images(self, keyword: str, count: int = 10, license: str = "4,5,6,9,10") -> List[Dict[str, str]]:
        """
        Search for images on Flickr based on a keyword.
        By default, it searches for Creative Commons licensed images to ensure safe usage.
        """
        if not self.api_key or self.api_key == "your_api_key_here":
            return []
            
        params = {
            "method": "flickr.photos.search",
            "api_key": self.api_key,
            "text": keyword,
            "format": "json",
            "nojsoncallback": "1",
            "per_page": count,
            "license": license, # Creative Commons licenses
            "sort": "relevance",
            "safe_search": "1",
            "extras": "url_m,url_l" # Request medium and large image URLs directly
        }
        
        try:
            print(f"Searching Flickr for '{keyword}'...")
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("stat") != "ok":
                print(f"Flickr API Error: {data.get('message')}")
                return []
                
            photos = data.get("photos", {}).get("photo", [])
            results = []
            
            for photo in photos:
                # Prefer large URL, fallback to medium
                img_url = photo.get("url_l") or photo.get("url_m")
                if img_url:
                    results.append({
                        "id": photo.get("id"),
                        "title": photo.get("title"),
                        "url": img_url
                    })
                    
            print(f"Successfully retrieved {len(results)} images for '{keyword}'.")
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"Network error while calling Flickr API: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
