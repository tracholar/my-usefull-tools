#coding:utf-8
"""
标准寸照生成器
"""

import os,sys,re
import argparse
from PIL import Image

def imcp(im, N=2, M=4, padding = 10):
    image = Image.new('RGB', (im.width*M+padding*(M-1), im.height*N+padding*(N-1)), (255,255,255))

    for i in range(M):
        for j in range(N):
            image.paste(im, box=(i*(im.width+padding), j*(im.height+padding) ))
    return image

def convert_image(fname, N=2, M=4, padding = 10):
    """将fname对应的图片转换为寸照,格式为 `N`x`M`

    Parameters
    ----------
    fname : str
        输入文件名
    N : int
        行数
    M : int
        列数

    Returns
    -------
    Image

    """
    im = Image.open(fname)
    if 1.0 * im.width / im.height > 295.0/413:
        im0 = im.resize((295, int(1.0*im.height/im.width*295)))
    else:
        im0 = im.resize((int(1.0*im.width/im.height*413), 413))

    # 填充白色
    im1 = Image.new('RGB', (295,413), (255,255,255))
    im1.paste(im0, box=(im1.width - im0.width, im1.height-im0.height))

    image = imcp(im1, N, M, padding = padding)

    return image

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('originFile', help='原始图片文件路径')
    parser.add_argument('-o', '--outputFile', help='输出图片文件路径')
    parser.add_argument('-n', '--column', type=int, default=2, help='输出列数')
    parser.add_argument('-m', '--row', type=int, default=4, help='输出行数')
    parser.add_argument('-p', '--padding', type=int, default=20, help='空白像素')

    args = parser.parse_args()

    if args.outputFile is None:
        args.outputFile = args.originFile + '.png'

    image = convert_image(args.originFile, args.column, args.row, args.padding)
    image.save(args.outputFile)
