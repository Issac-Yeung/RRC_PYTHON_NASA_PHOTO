
import urllib.request
from menu import Menu
from requests import get
import json
from PIL import Image
from io import BytesIO
import requests
class NASAPhoto:
    PAGE_SIZE = 10
    API_KEY = "d6tVV5VdFFfyRJy40d7o8OpW0nnX6LLOSdSLMvvL"

    def __init__(self):
        self.prevent_refresh = False

        rover_names = self.getAllRovers()
        self.photo_options = [(name, lambda n=name: self.loadPhoto(n.lower())) for name in rover_names]
        self.photo_options.append(("Exit", Menu.CLOSE))

        self.main_menu = Menu(
            title="NASA Mars Photo",
            message="Choose one of the available rovers (try Curiosity):",
            refresh=self.checkChoice,
            auto_clear=True)
        self.main_menu.set_prompt(">")

    def checkChoice(self):
        self.main_menu.set_options(self.photo_options)
        self.main_menu.set_message("Choose one of the available rovers (try Curiosity): ")

    def loadPhoto(self, rover_name=None):
        INPUT_DATE_MESSAGE = "Please enter a date in the following format: YYYY-MM-DD (if you chose Curisouity, try 2015-06-03 or 2020-01-01) -> "
        self.main_menu.auto_clear = False
        
        if rover_name:
            date = input(INPUT_DATE_MESSAGE)
            print(f"You selected rover {rover_name} with date {date}.")
            photos = self.getPhoto(rover_name, date)
            self.displayPhotosMenu(photos, date)
            
        self.main_menu.prevent_refresh = True

    def displayPhotosMenu(self, photos, earth_date, current_page=0):
        total_pages = (len(photos) - 1) // NASAPhoto.PAGE_SIZE + 1
        current_photos = photos[current_page * NASAPhoto.PAGE_SIZE: (current_page + 1) * NASAPhoto.PAGE_SIZE]

        options = [(f"{photo['img_src']}", lambda: self.openPhoto(photo)) for photo in current_photos]

        # Check if we have more pages after the current one
        if current_page < total_pages - 1:
            options.append(("<Next set of photos>", lambda: photo_menu.close() or self.displayPhotosMenu(photos, earth_date, current_page + 1)))

        # Check if we have previous pages before the current one
        if current_page > 0:
            options.append(("<Previous set of photos>", lambda: photo_menu.close() or self.displayPhotosMenu(photos, earth_date, current_page - 1)))

        options.append(("<Return to main menu>", lambda: photo_menu.close() or self.main_menu.open()))

        photo_menu = Menu(options=options, title=f'Page {current_page + 1}/{total_pages}: {len(photos)} photos available for {earth_date}. Choose one to view', auto_clear=True)
        photo_menu.open()
    
    def close(self):
        self._exit = True
    
    def run(self):
        self.main_menu.open()
    
    def getPhoto(self, rover_name, earth_date):
        self.url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/{rover_name}/photos?earth_date={earth_date}&api_key={NASAPhoto.API_KEY}';
        response = urllib.request.urlopen(self.url)
        astros = json.loads(response.read())
        return astros["photos"]

    def getAllRovers(self):
        url_rovers = f"https://api.nasa.gov/mars-photos/api/v1/rovers?api_key={NASAPhoto.API_KEY}"
        data = get(url_rovers).json()  
        return [rover['name'] for rover in data['rovers']]
        
    
    def openPhoto(self, photo):
        img_url = photo['img_src']
        response = requests.get(img_url)
        image = Image.open(BytesIO(response.content))
        image.show()

if __name__ == "__main__":
    NASAPhoto().run()

