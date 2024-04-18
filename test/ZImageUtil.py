import numpy
from PIL import Image
import cv2
import matplotlib.pyplot as plt


def img_pil_to_cv2(img):
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)


def img_cv2_to_pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def cv2_show(img, name=''):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def plt_show(imgs: []):
    size = len(imgs)
    print('size: ' , size)
    for index, it in enumerate(imgs):
        print('index: ', index)
        plt.subplot(1, size, index + 1)
        plt.imshow(cv2.cvtColor(it, cv2.COLOR_BGR2RGB))
    plt.show()
