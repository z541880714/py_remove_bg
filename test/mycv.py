import cv2
import numpy as np

image = cv2.imread('../res/APHB428627-M215-CmanChen.jpg')
shap = image.shape
print('shape: ', shap, 'type of shap: ', type(shap), shap[0], shap[1], shap[2])
h, w, l = shap
print('h: ', h, 'w: ', w, ' l:', l)

# image 结构 ..
print(len(image), len(image[0]), len(image[0][0]))

# 灰度图
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 根据stack overflow上的一个解答，cv2.imshow()后面需要跟随者cv2.waitKey(period)函数，
# 这个函数可以使图像持续显示给定的一段时间period(ms)，否则，图片将无法显示。
# 例如：waitKey(0)将持续显示图片直到有按键被按下（这一设置很适合用于显示图片）；
# waitKey(25)将使图片显示25ms，之后图片窗口将会自动关闭。
# 如果你将它置于一个读取图片的loop中，那么它将逐帧显示图片
# cv2.imshow('image.jpg', gray_img)
# cv2.waitKey(0)

cv2.imwrite('../out/111_output.png', gray_img)

### 负片转换,   图片的 通道拆分, 与组合..

b, g, r = cv2.split(image)

print('type b: ', type(b), 'shape b: ', b.shape)

b = 255 - b
g = 255 - g
r = 255 - r

negative = np.zeros((h, w, 3))

negative[:, :, 0] = b
negative[:, :, 1] = g
negative[:, :, 2] = r

cv2.imwrite('../out/111_negative.png', negative)
