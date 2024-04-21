# coding:utf8
import os.path
import sys

import cv2
import numpy as np

sys.path.append(os.path.abspath('util'))
from util.ZImageUtil import plt_show


def reserveBlackColor(img):
    """
    由于文字,log 为黑色 只保留黑色
    :param img:
    :return:
    """

    img = 255 - img
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    l_black = np.array([0, 0, 215])
    h_black = np.array([180, 30, 255])
    mask = cv2.inRange(hsv, l_black, h_black)
    res = cv2.bitwise_or(img, img, mask=mask)
    return res


# 去掉黑色, 先取反, 去掉白色, 在取反即可.
def dropBlackColor(img):
    gray = cv2.cvtColor(255 - img, cv2.COLOR_BGR2GRAY)
    sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 1, ksize=3)
    ret, binary = cv2.threshold(sobel, 150, 255, cv2.THRESH_BINARY)
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 80))
    dilation = cv2.dilate(binary, element1, iterations=1)
    dilation1 = cv2.dilate(dilation, element1, iterations=1)
    dilation2 = cv2.cvtColor(dilation1, cv2.COLOR_GRAY2RGB)
    l_white = np.array([0, 0, 0])
    h_white = np.array([255, 255, 255])
    mask = cv2.inRange(img, l_white, h_white)
    result = cv2.bitwise_or(img, dilation2, mask=mask)
    # plt_show(img, gray, sobel, binary, dilation)
    return result


def preprocess(gray):
    kernel = np.ones((4, 4), np.uint8)
    e = cv2.erode(gray, kernel)
    f = cv2.subtract(gray, e)
    # 1. Sobel算子，x方向求梯度
    sobel = cv2.Sobel(f, cv2.CV_8U, 1, 0, ksize=3)
    # 2. 二值化
    ret, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

    # 3. 膨胀和腐蚀操作的核函数
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 9))
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))

    # 4. 膨胀一次，让轮廓突出
    dilation = cv2.dilate(binary, element2, iterations=1)

    # 5. 腐蚀一次，去掉细节，如表格线等。注意这里去掉的是竖直的线
    erosion = cv2.erode(dilation, element1, iterations=1)

    # 6. 再次膨胀，让轮廓明显一些
    dilation2 = cv2.dilate(erosion, element2, iterations=3)

    # 7. 存储中间图片
    # cv2.imwrite("binary.png", binary)
    # cv2.imwrite("dilation.png", dilation)
    # cv2.imwrite("erosion.png", erosion)
    # cv2.imwrite("dilation2.png", dilation2)

    return dilation2


def findTextRegion(img):
    t_size = 1024
    w = img.shape[0]
    h = img.shape[1]
    print('img size: ', img.shape)
    # 计算出 区域后, 还要还原尺寸.
    scale_w = w / t_size
    scale_h = h / t_size
    img_resize = cv2.resize(img, (t_size, t_size))
    region = []
    # 1. 查找轮廓
    contours, hierarchy = cv2.findContours(img_resize, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 2. 筛选那些面积小的
    for i in range(len(contours)):
        cnt = contours[i]
        # 计算该轮廓的面积
        area = cv2.contourArea(cnt)
        # 面积小的都筛选掉
        if area < 5000:
            continue
        # 轮廓近似，作用很小
        epsilon = 0.001 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # 找到最小的矩形，该矩形可能有方向
        rect = cv2.minAreaRect(cnt)

        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int32(box)
        p_center = np.sum(box, axis=0) / 4
        # 到边缘的距离 靠中心的 h_min * w_min 的值越大.
        h_min = min(p_center[1], abs(t_size - p_center[1]))
        w_min = min(p_center[0], abs(t_size - p_center[0]))
        print('box: ', type(box), box.shape, box, ' center:', p_center, ' h_min * w_min: ', h_min * w_min)

        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])

        # 筛选那些太细的矩形，留下扁的
        if height > width * 1.2:
            continue
        if h_min * w_min > 40000:
            continue
        box[:, 0] = np.int32(box[:, 0] * scale_w)
        box[:, 1] = np.int32(box[:, 1] * scale_h)
        region.append(box)
    return region


def detect(img):
    bw = reserveBlackColor(img)
    # 1.  转化成灰度图
    gray = cv2.cvtColor(bw, cv2.COLOR_BGR2GRAY)
    # 2. 形态学变换的预处理，得到可以查找矩形的图片
    dilation = preprocess(gray)
    # 3. 查找和筛选文字区域
    region = findTextRegion(dilation)

    # 4. 用绿线画出这些找到的轮廓
    # for box in region:
    #     cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
    # plt_show(img)

    # 4.1 将轮廓内的 黑色 替换成 白色
    for box in region:
        x_min = np.min(box[:, 0])
        x_max = np.max(box[:, 0])
        y_min = np.min(box[:, 1])
        y_max = np.max(box[:, 1])
        merge = dropBlackColor(img[y_min:y_max, x_min:x_max])
        img[y_min:y_max, x_min:x_max] = merge
    return img


if __name__ == '__main__':
    if not os.path.exists('resLogo'):
        os.mkdir('resLogo')
    if not os.path.exists('outLogo'):
        os.mkdir('outLogo')
    # 读取文件
    root = os.path.abspath('resLogo')

    for filename in os.listdir(root):
        # if "LYCB4C006YJ103" in filename:
        print('file name: ', filename)
        image_path = f'{root}/{filename}'
        img = cv2.imread(image_path)
        img = cv2.resize(img, (1024, 1024))
        img = detect(img)
        cv2.imwrite(f'outLogo/{filename}', img)
        # plt_show(img)
