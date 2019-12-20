try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import PIL.ImageOps
import pygsheets
from datetime import datetime

gc = pygsheets.authorize(service_file='client_secret.json')

wb = gc.open('Apex Data -- The Bois')

sheet = wb[0]

index_to_start = sheet.get_values(start='B3', end='B1000', returnas='cells')

working_range = sheet.get_values(start='A3', end='AB1000', returnas='cells')

games_played = 0

for row in index_to_start:
    for cell in row:
        if(cell.value != ''):
            games_played += 1

input_row = games_played

# start game
working_range[input_row][0].value = input_row + 1

now = datetime.now()

working_range[input_row][1].value = now.strftime("%m/%d/%Y %H:%M:%S")


# game end
game_end = input("did the game end? \n")
now1 = datetime.now()
working_range[input_row][2].value = now1.strftime("%m/%d/%Y %H:%M:%S")
landed = input('third partied? y or n \n')

if(landed == 'y'):
    working_range[input_row][6].value = "Yes"
elif(landed == 'n'):
    working_range[input_row][6].value = "No"

game_mode = input("game mode? c or r \n")

if(game_mode == 'r'):
    working_range[input_row][7].value = "Ranked"
elif(game_mode == 'c'):
    working_range[input_row][7].value = "Casual"

screenshot_path = input('path to screenshot \n')
print(screenshot_path[1:-1])
    


#-----------------------#
#                       #
#   Start Image Work    #
#                       #
#-----------------------#

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

image = Image.open(screenshot_path[1:-1])

width, height = image.size

left = 100
top = height / 4
right = 2200
bottom = 3 * height / 4

cropped_image = image.crop((left, top, right, bottom))

inverted_image = PIL.ImageOps.invert(cropped_image.convert("RGB"))

image_text = pytesseract.image_to_string(inverted_image)

heath = image_text.find('cloolis')
devon = image_text.find('DEVIS2012')
cam = image_text.find('el_smithereens')

heath_stats = image_text[heath:heath+36]
cam_stats = image_text[cam:cam+36]
devon_stats = image_text[devon:devon+38]

data = {}
heath_data = {}
cam_data = {}
devon_data = {}

# Heath damage column s = 19 + 1
# Heath Kills column t = 20 + 1

# devon damage I = 9 + 1
# devon kills J = 10 + 1

# cameron damage N = 14
# cameron kills O = 15

def get_heath_stats():
    if(heath != -1):
        # kills
        working_range[input_row][19].value = int(heath_stats[15:18])
        heath_data['Kills'] = int(heath_stats[15:18])

        # damage
        working_range[input_row][18].value = int(heath_stats[32:38])
        heath_data['Damage'] = int(heath_stats[32:38])

        data['Heath'] = heath_data
    else:
        print("heath's data not found... :(")

def get_devon_stats():
    if(devon != -1):
        # kills
        working_range[input_row][9].value = int(devon_stats[17:20])
        devon_data['Kills'] = int(devon_stats[17:20])

        # damage
        working_range[input_row][8].value = int(devon_stats[34:39])
        devon_data['Damage'] = int(devon_stats[34:39])
        data['Devon'] = devon_data
    else:
        print("devon's data not found... :(")

def get_cam_stats():
    if(cam != -1):
        # kills
        working_range[input_row][14].value = int(cam_stats[15:18])
        cam_data['Kills'] = int(cam_stats[15:18])

        # damage
        working_range[input_row][13].value = int(cam_stats[32:38])
        cam_data['Damage'] = int(cam_stats[32:38])

        data['Cameron'] = cam_data
    else:
        print("cam's data not found... :(")

def get_the_bois_stats():
    get_heath_stats()
    get_devon_stats()
    get_cam_stats()
    print(data)
    
get_the_bois_stats()