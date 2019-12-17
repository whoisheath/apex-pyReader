try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

print(pytesseract.image_to_string(Image.open('game_test01.png')))
