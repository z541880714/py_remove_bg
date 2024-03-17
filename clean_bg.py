# encoding='utf-8'
from rembg.bg import remove
from PIL import Image, ImageDraw, ImageFont
from os import path
import os

resolution = 2000  # 统一输出分辨率


def remove_bg(path_in):
    in_image = Image.open(path_in)
    return remove(in_image)


def logoImage():
    logo = Image.open('assets/logo2.png')
    x, y = logo.size
    logo = logo.resize((400, int(y / x * 400)))
    return logo


def handle_img(pic_name):
    no_bg = remove_bg(f'res/{pic_name}')
    x, y = no_bg.size
    max_size = max(x, y)
    rate = y / x
    x_ = x if rate < 1 else int(y / rate)
    y_ = y if rate > 1 else int(x * rate)

    x_margin = int(0.5 * (max_size - x_))
    y_marging = int(0.5 * (max_size - y_))

    logo = logoImage()

    new_img = Image.new('RGB', (max_size, max_size), (255, 255, 255))
    new_img.paste(no_bg, (0 + x_margin, 0 + y_marging, x_margin + x_, y_marging + y_), mask=no_bg)
    new_img = new_img.resize((resolution, resolution), Image.BILINEAR)
    new_img.paste(logo, (resolution - logo.width, 20, resolution, 20 + logo.height), mask=logo)

    draw = ImageDraw.Draw(new_img)
    font_style = ImageFont.truetype('arial.ttf', 50, encoding='utf-8')
    draw.text((20, resolution - 100), pic_name[:pic_name.index('.')], '#000000', font=font_style)
    new_img.save(f'./out/{pic_name}')


if __name__ == '__main__':
    if not path.exists('out/'):
        os.mkdir('out/')
    index = 1
    size = len(os.listdir('res'))
    for f in os.listdir('res'):
        print(f'正在处理:{f} 图片总数:{size},当前进度:{index}')
        index += 1
        handle_img(f)
