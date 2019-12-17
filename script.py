try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import PIL.ImageOps
import pygsheets

gc = pygsheets.authorize(service_file='client_secret.json')

wb = gc.open('Apex Data -- The Bois')

sheet = wb.worksheet_by_title('Game Data')

cell_list = sheet.get_values(start='B3', end='B1000', returnas='cells')

games_played = 0

for row in cell_list:
    for cell in row:
        if(cell.value != ''):
            games_played += 1

input_row = games_played + 1

print(sheet[34][2]) # can't access cells in a row greater than index of 34, so greater than row 33 lol what

#-----------------------#
#                       #
#   Start Image Work    #
#                       #
#-----------------------#

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

image = Image.open(r'images\\game_with_devon.png')

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
        sheet[input_row][21] = int(heath_stats[15:18])

        # damage
        sheet[input_row][20] = int(heath_stats[32:38])
        # sheet[input_row][20] = int(heath_stats[15:18])
        # heath_data['Kills'] = int(heath_stats[15:18])
        # heath_data['Damage'] = int(heath_stats[32:38])
        # data['Heath'] = heath_data
    else:
        print("heath's data not found... :(")

def get_devon_stats():
    if(devon != -1):
        # print(devon_stats)
        devon_data['Kills'] = int(devon_stats[17:20])
        devon_data['Damage'] = int(devon_stats[34:39])
        data['Devon'] = devon_data
    else:
        print("devon's data not found... :(")

def get_cam_stats():
    if(cam != -1):
        cam_data['Kills'] = int(cam_stats[15:18])
        cam_data['Damage'] = int(cam_stats[32:38])
        data['Cameron'] = cam_data
    else:
        print("cam's data not found... :(")

def get_the_bois_stats():
    get_heath_stats()
    get_devon_stats()
    get_cam_stats()
    print(data)
    
# get_the_bois_stats()