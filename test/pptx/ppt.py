import os

from pptx import Presentation, util

prs = Presentation()
w = util.Cm(8)  # 每张图片的 宽度
h = util.Cm(8)  # 每张图片的高度

m = 3  # 每行图片的数量
n = 2  # 每列图片的数量

prs.slide_width = w * m
prs.slide_height = h * n
blank_slid = prs.slide_layouts[6]

root = os.path.dirname(__file__)

res_dir = f'{root}/res'
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
        slid.shapes.add_picture(img_path_list[index], w * x, h * y, w, h)
        index += 1
        i += 1

prs.save(f'{root}/out/test.pptx')
