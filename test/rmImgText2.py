from PIL import Image
import cv2
import numpy as np
from ZImageUtil import img_pil_to_cv2, img_cv2_to_pil
import matplotlib.pyplot as plt

img = cv2.imread('../res/ATHB430295-F776-IvyZhang.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

######## distanceTransform 用法 ###########################################
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# ishow = img.copy()
# ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#
# kernel = np.ones((3, 3), np.uint8)
# opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)  # 进行开运算
# dis_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
# ret, fore = cv2.threshold(dis_transform, 0.7 * dis_transform.max(), 255, 0)
#
# plt.subplot(1, 3, 1)
# plt.imshow(ishow)
# plt.axis('off')
#
# plt.subplot(1, 3, 2)
# plt.imshow(dis_transform)
# plt.axis('off')
#
# plt.subplot(1, 3, 3)
# plt.imshow(fore)
# plt.axis('off')
#
# plt.show()

###################################################

##########获取图的边界#######################

k = np.ones((3, 3), np.uint8)
e = cv2.erode(img, k)
f = cv2.subtract(img, e)  # 两图相减
f2 = cv2.threshold(f, 140, 255, cv2.THRESH_BINARY)[1]

opening = cv2.morphologyEx(f, cv2.MORPH_ERODE, k, iterations=2)  # 进行开运算

# 绘制子图
# plt.subplot(2, 3, 5) 和 plt.subplot(235) 是效果是一样的

plt.subplot(111), plt.imshow(opening, ), plt.title("f2")

plt.show()

#########################################################
