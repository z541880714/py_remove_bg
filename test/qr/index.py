# encode='utf-8'
import qrcode

img = qrcode.make(data='hello 123123')
img.save('test.png')
