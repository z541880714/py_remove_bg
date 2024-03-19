# encoding='utf-8'
from PIL import Image, ImageDraw, ImageFont
from os import path
import os

resolution = 1024  # 统一输出分辨率
logo_size = 200
logo_margin = 20
font_size = 50
out_dir = 'out_serial_num/'

if not path.exists(out_dir):
    os.mkdir(out_dir)
if not path.exists('res/'):
    os.mkdir('res/')


def handle_img(pic_name):
    no_bg = Image.open(f'res/{pic_name}').convert('RGB')
    x, y = no_bg.size
    max_size = max(x, y)
    rate = y / x
    x_ = x if rate < 1 else int(round(y / rate))
    y_ = y if rate > 1 else int(round(x * rate))
    x_margin = int(0.5 * (max_size - x_))
    y_margin = int(0.5 * (max_size - y_))
    new_img = Image.new('RGB', (max_size, max_size), (255, 255, 255))
    box = (x_margin, y_margin, x_margin + x_, y_margin + y_)
    # print(f'max size: {max_size}, origin size: {(x, y)}, box size: {box},  margin:{(x_margin, y_margin)}')
    new_img.paste(no_bg, box, mask=None)
    new_img = new_img.resize((resolution, resolution), Image.BILINEAR)
    draw = ImageDraw.Draw(new_img)
    font_style = ImageFont.truetype('arial.ttf', font_size, encoding='utf-8')
    draw.text((20, resolution - font_size - 20), pic_name[:pic_name.index('.')], '#000000', font=font_style)
    new_img.save(f'{out_dir}/{pic_name}')


if __name__ == '__main__':
    index = 1
    size = len(os.listdir('res'))
    for f in os.listdir('res'):
        print(f'正在处理:{f} 图片总数:{size},当前进度:{index}')
        index += 1
        # remove_background(f)
        handle_img(f)
