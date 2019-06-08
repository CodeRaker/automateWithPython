# pip install pytesseract <-- this is only the api to tesseract

from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # tell where tesseract is, must install first

img = Image.open("C:\\Users\\LoL\Desktop\\symantectest.jpg")
print(pytesseract.image_to_string(img))
