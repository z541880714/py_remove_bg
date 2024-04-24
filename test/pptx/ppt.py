import os

from pptx import Presentation, util

prs = Presentation()
w = util.Cm(6)  # 每张图片的 宽度
h = util.Cm(6)  # 每张图片的高度

m = 4  # 每行图片的数量
n = 2  # 每列图片的数量

left = util.Cm(0.1)  # 左边预留的间隔
top = util.Cm(0.1)  # 顶部预留的间隔
right = util.Cm(0.1)  # 右边预留的间隔
bottom = util.Cm(0.1)  # 底部预留的间隔

padding_top = util.Cm(2)
padding_bottom = util.Cm(2)

prs.slide_width = (w + left + right) * m
prs.slide_height = (h + top + bottom) * n + padding_top + padding_bottom
blank_slid = prs.slide_layouts[6]

root = os.path.dirname(__file__)

res_dir = f'{root}/res'
out_dir = f'{root}/out'
if not os.path.exists(res_dir):
    os.mkdir(res_dir)

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

img_path_list = []
for name in os.listdir(res_dir):
    img_path_list.append(os.path.join(res_dir, name))

# print(len(img_path_list), img_path_list)

index = 0

while index < len(img_path_list):
    slid = prs.slides.add_slide(blank_slid)
    i = 0
    while index < len(img_path_list) and i < m * n:
        x = i % m
        y = int(i / m)
        slid.shapes.add_picture(img_path_list[index], (left + w + right) * x + left,
                                padding_top + (top + h + bottom) * y + top, w, h)
        index += 1
        i += 1

prs.save(f'{root}/out/test.pptx')
