from PIL import Image

im = Image.open('game_test.png')

width, height = im.size

left = 100
top = height / 4
right = 2200
bottom = 3 * height / 4

im1 = im.crop((left, top, right, bottom))

im1.show()