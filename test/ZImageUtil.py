import numpy
from PIL import Image
import cv2
import matplotlib.pyplot as plt


def img_pil_to_cv2(img):
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)


def img_cv2_to_pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def plt_show_cv2img(cv2img):
    plt.imshow(cv2.cvtColor(cv2img, cv2.COLOR_BGR2RGB))


def cv2_show(img, name=''):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
