# encoding='utf-8'
import numpy
from rembg.bg import remove
from PIL import Image, ImageDraw, ImageFont
from os import path
import os
from transparent_background import Remover

remover = Remover()


def process_bg(img):
    img = remover.process(img, type='[0, 0, 0]', threshold=0.6)
    img = remover.process(img, type='rgba')
    return img


resolution = 1024  # 统一输出分辨率
logo_size = 200
logo_margin = 10
if not path.exists('out/'):
    os.mkdir('out/')
if not path.exists('res/'):
    os.mkdir('res/')


def remove_bg(path_in):
    in_image = Image.open(path_in)
    return remove(in_image)


def logoImage():
    logo = Image.open('assets/logo2.png')
    x, y = logo.size
    logo = logo.resize((logo_size, int(y / x * logo_size)))
    return logo


def handle_img(pic_name):
    img_path = f'res/{pic_name}'
    img = Image.open(img_path).convert("RGB")
    no_bg = process_bg(img)
    x, y = no_bg.size
    max_size = max(x, y)
    rate = y / x
    x_ = x if rate < 1 else int(numpy.round(y / rate))
    y_ = y if rate > 1 else int(numpy.round(x * rate))
    x_margin = int(numpy.floor(0.5 * (max_size - x_)))
    y_margin = int(numpy.floor(0.5 * (max_size - y_)))
    logo = logoImage()
    new_img = Image.new('RGB', (max_size, max_size), (255, 255, 255))
    box = (x_margin, y_margin,
           min(x_margin + x, max_size - x_margin),
           min(x_margin + y, max_size - y_margin))
    new_img.paste(no_bg, box, mask=no_bg)
    new_img = new_img.resize((resolution, resolution), Image.BILINEAR)
    new_img.paste(logo, (resolution - logo.width, logo_margin, resolution, logo_margin + logo.height),
                  mask=logo)
    draw = ImageDraw.Draw(new_img)
    font_style = ImageFont.truetype('arial.ttf', 30, encoding='utf-8')
    draw.text((20, resolution - 50), pic_name[:pic_name.index('.')], '#000000', font=font_style)
    new_img.save(f'./out/{pic_name}')


def remove_background(img_name):
    img_in_path = f'res/{img_name}'
    img_out_path = f'out/{img_name}'
    os.system(f"python -m backgroundremover.cmd.cli -i {img_in_path} -o {img_out_path}")


if __name__ == '__main__':
    index = 1
    size = len(os.listdir('res'))
    for f in os.listdir('res'):
        # if not f == 'ATHB430290-F776-IvyZhang.jpg':
        #     continue
        print(f'正在处理:{f} 图片总数:{size},当前进度:{index}')
        index += 1
        # remove_background(f)
        handle_img(f)
