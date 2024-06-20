# encoding=utf-8
import os

import qrcode
import argparse
import cv2
import numpy as np


def resize(img, size_t):
    h, w, _ = img.shape
    print('w:', w, ' h :', h)

    h_t = size_t if h > w else int(size_t * h / w)
    w_t = int(h_t * w / h)
    return cv2.resize(img, (w_t, h_t))


parser = argparse.ArgumentParser()
parser.add_argument("str", type=str, help="二维码的字符串内容")
parser.add_argument("output", type=str, help="二维码文件输出路径")
parser.add_argument("--logoPath", type=str, default='', help="logo文件路径")

args = parser.parse_args()

str = args.str
output = args.output
os.makedirs(os.path.dirname(output), exist_ok=True)
print("qr str:", str, ' output:', output)

img = qrcode.make(data=str)
img.save(output)

if len(args.logoPath) > 0 and os.path.exists(args.logoPath):
    # 将logo 放入 二维码中间.
    crImg = cv2.imdecode(np.fromfile(output, dtype=np.uint8), cv2.IMREAD_COLOR)
    crImg = cv2.resize(crImg, (500, 500))
    print('crImg shape:', crImg.shape)

    logo = cv2.imdecode(np.fromfile(args.logoPath, dtype=np.uint8), cv2.IMREAD_COLOR)

    logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
    ret, logo_mask = cv2.threshold(logo_gray, 20, 255, cv2.THRESH_BINARY)

    mask_inv = cv2.bitwise_not(logo_mask)
    logo_bg = cv2.cvtColor(mask_inv, cv2.COLOR_GRAY2BGR)
    logo_fg = cv2.bitwise_and(logo, logo, mask=logo_mask)
    logo = cv2.add(logo_bg, logo_fg)

    target_size = 120
    logo = resize(logo, target_size)

    h, w, _ = logo.shape
    left = (500 - w) // 2
    top = (500 - h) // 2
    crImg[top: top + h, left:left + w] = logo
    cv2.imencode('.jpg', crImg)[1].tofile(output)
