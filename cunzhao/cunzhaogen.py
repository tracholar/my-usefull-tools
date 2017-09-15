#coding:utf-8
# 标准寸照生成器

import os,sys
from PIL import Image

def imcp(im, N=4, M=2):
    padding = 30
    image = Image.new('RGB', (im.width*M+padding*(M-1), im.height*N+padding*(N-1)), (255,255,255))

    for i in range(M):
        for j in range(N):
            image.paste(im, box=(i*(im.width+padding), j*(im.height+padding)))
    return image

if __name__ == '__main__':
    im = Image.open(sys.argv[1])
    if 1.0 * im.width / im.height > 295.0/413:
        im0 = im.resize((295, int(1.0*im.height/im.width*295)))
    else:
        im0 = im.resize((int(1.0*im.width/im.height*413), 413))

    # 填充白色
    im1 = Image.new('RGB', (295,413), (255,255,255))
    im1.paste(im0, box=(im1.width - im0.width, im1.height-im0.height))

    image = imcp(im1, int(sys.argv[2]), int(sys.argv[3]))
    image.save(sys.argv[4])
