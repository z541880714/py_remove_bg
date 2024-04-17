import os.path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract

image = Image.open('../res/LYCB4C006YJ103.jpg')

if not os.path.exists('../out'):
    os.mkdir('../out')


def save(image):
    image.save('out/out.jpg')


gray_image = image.convert('L')
save(gray_image)

threshold = 100
binary_image = gray_image.point(lambda x: 255 if x > threshold else 0, '1')
save(binary_image)
