import os

from pptx import Presentation, util

prs = Presentation()
w = util.Cm(8)
h = util.Cm(8)
prs.slide_width = w * 3
prs.slide_height = h * 2
blank_slid = prs.slide_layouts[6]

res_dir = '../../res'
img_path_list = []
for name in os.listdir(res_dir):
    img_path_list.append(os.path.join(res_dir, name))

print(len(img_path_list), img_path_list)

index = 0

while index < len(img_path_list):
    slid = prs.slides.add_slide(blank_slid)
    i = 0
    while index < len(img_path_list) and i < 6:
        x = i % 3
        y = int(i / 3)
        slid.shapes.add_picture(img_path_list[index], w * x, h * y, w, h)
        index += 1
        i += 1

prs.save('../../out/test.pptx')
