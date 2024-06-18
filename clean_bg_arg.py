# encoding=utf-8

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from transparent_background import Remover
import argparse

remover = Remover()
resolution = 1024  # 统一输出分辨率
logo_size = 200
logo_margin = 10


def areaFilter(minArea, inputImage):
    # Perform an area filter on the binary blobs:
    componentsNumber, labeledImage, componentStats, componentCentroids = \
        cv2.connectedComponentsWithStats(inputImage, connectivity=4)
    # Get the indices/labels of the remaining components based on the area stat
    # (skip the background component at index 0)
    remainingComponentLabels = [i for i in range(
        1, componentsNumber) if componentStats[i][4] >= minArea]
    # Filter the labeled pixels based on the remaining labels,
    # assign pixel intensity to 255 (uint8) for the remaining pixels
    filteredImage = np.where(
        np.isin(labeledImage, remainingComponentLabels) == True, 255, 0).astype('uint8')
    return filteredImage


# 把图像生成 二进制 黑白图片, 黑色的位置为 255, 其它的颜色为 0,  可以设置一个 0-255 的一个阈值. 阈值以上的 为255, 阈值以下的为0
def binaryImage(inputImage, threshold_=0.75):
    # Conversion to CMYK (just the K channel):
    # Convert to float and divide by 255:
    imgFloat = inputImage / 255.0
    # Calculate channel K:
    kChannel = 1 - np.max(imgFloat, axis=2)
    # Convert back to uint 8:
    kChannel = (255 * kChannel).astype(np.uint8)
    binaryThresh = int(255 * threshold_)
    _, binaryImage = cv2.threshold(
        kChannel, binaryThresh, 255, cv2.THRESH_BINARY)
    binaryImage = areaFilter(100, binaryImage)
    # Use a little bit of morphology to clean the mask:
    # Set kernel (structuring element) size:
    kernelSize = 3
    # Set morph operation iterations:
    opIterations = 2
    # Get the structuring element:
    morphKernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (kernelSize, kernelSize))
    # Perform closing:
    img_binary = cv2.morphologyEx(binaryImage, cv2.MORPH_CLOSE, morphKernel, None, None, opIterations,
                                  cv2.BORDER_REFLECT101)
    return img_binary


#  f"python -m backgroundremover.cmd.cli -i {img_in_path} -o {img_out_path}")
def process_bg(img):
    img_ = remover.process(img, type='rgba')
    return img_


def logoImage(logo_path):
    logo = Image.open(logo_path)
    x, y = logo.size
    logo = logo.resize((logo_size, int(y / x * logo_size)))
    new_img = Image.new('RGB', (logo_size, logo_size), (255, 255, 255))
    new_img.paste(logo, (0, 0), mask=logo)
    return new_img


def joint(no_bg, logo_path=None, sizeinfo=None, sn='', has_mask=False):
    print("text:", sn)
    print("logo:", logo_path)
    x, y = no_bg.size
    max_size = 950
    rate = min(max_size / x, max_size / y)
    x_ = int(rate * x)
    y_ = int(rate * y)
    no_bg = no_bg.resize((x_, y_), Image.BILINEAR)
    x_margin = int(0.5 * (resolution - x_))
    y_margin = int(0.5 * (resolution - y_))
    new_img = Image.new('RGB', (resolution, resolution), (255, 255, 255))
    new_img.paste(no_bg, (x_margin, y_margin),
                  mask=no_bg if has_mask else None)

    if logo_path is not None:
        logo = logoImage(logo_path)
        new_img.paste(logo, (resolution - logo.width, logo_margin))
    if len(sn) > 0:
        draw = ImageDraw.Draw(new_img)
        font_style = ImageFont.truetype('arial.ttf', 50, encoding='utf-8')
        draw.text((20, resolution - 70), sn, '#000000', font=font_style)

    if sizeinfo is not None:
        draw = ImageDraw.Draw(new_img)
        font_size = 45
        font_style = ImageFont.truetype(
            'arial.ttf', font_size, encoding='utf-8')
        w = font_size * len(sizeinfo)
        draw.text(((resolution - w * 0.5) / 2, resolution - font_size - 80), sizeinfo,
                  '#000000', font=font_style, align='center')
    return new_img


# 获取最大 区域的坐标
def split_max_rec(image):
    # 灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)

    #   cv2.findContours() 函数来查找物体轮廓
    #   cv2.RETR_EXTERNAL 只检测外轮廓
    # 	cv2.CHAIN_APPROX_SIMPLE 压缩水平方向 ，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需要4个点来保存轮廓信息
    # 返回两个值，一个是轮廓本身，一个是每条轮廓对应的属性
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(image, contours, -1, (0, 0, 255), 2)
    # cv2.imshow("img", image)
    # cv2.waitKey(0)
    dot = []  # 用来保存所有轮廓返回的坐标点。
    for c in contours:
        # 找到边界坐标
        min_list = []  # 保存单个轮廓的信息，x,y,w,h,area。 x,y 为起始点坐标
        x, y, w, h = cv2.boundingRect(c)  # 计算点集最外面的矩形边界
        min_list.append(x)
        min_list.append(y)
        min_list.append(w)
        min_list.append(h)
        min_list.append(w * h)  # 把轮廓面积也添加到 dot 中
        dot.append(min_list)

    # 找出最大矩形的 x,y,w,h,area
    max_area = 0  # 把第一个矩形面积当作最大矩形面积
    x, y, w, h = [0, 0, 0, 0]
    for inlist in dot:
        area = inlist[4]
        if area >= max_area:
            x, y, w, h = inlist[:-1]
            max_area = area
    return x - 10, y - 10, w + 20, h + 20


def handle_img_2(input_path, logo_path=None, sn='', sizeinfo=None):
    img = Image.open(input_path).convert("RGB")
    origin_data = cv2.imread(input_path)
    rec = split_max_rec(origin_data)
    area = rec[2] * rec[3]
    if area > 2000000:
        img = img.crop((rec[0], rec[1], rec[0] + rec[2], rec[1] + rec[3]))
    no_bg = process_bg(img)
    new_img = joint(no_bg, logo_path, sizeinfo, sn, True)
    return new_img


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='原始图片路径')
    parser.add_argument('output', type=str, help='处理后的图片路径')
    parser.add_argument('--logo', type=str, default="", help="logo文件的路径")
    parser.add_argument('--sn', type=str, default='', help="是否在底部添加文件名")
    parser.add_argument('--sizeinfo', type=str, default="", help='尺寸信息内容')
    args = parser.parse_args()

    out_dir = args.output
    logo_path = args.logo if args.logo != '' else None
    size_info = args.sizeinfo if args.sizeinfo != '' else None
    img = handle_img_2(args.input, logo_path, args.sn, size_info)
    img.save(args.output)
