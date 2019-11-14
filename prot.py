# -*- coding: utf8 -*-

import os
from builtins import reversed

import pytesseract
from PIL import Image
from wand.image import Image as WImage
from wand.color import Color as WColor

INPUT = './input'
OUTPUT = './output'
FORMAT_IMG = 'png'
FORMAT_TEXT = 'txt'


def convertPDFtoImg(file, dir_output):
    input_file = INPUT + '/' + file
    with WImage(filename=input_file, resolution=120) as source:
        source.format = FORMAT_IMG
        source.background_color = WColor("white")
        source.alpha_channel = False
        images = source.sequence
        pages = len(images)
        for i in range(pages):
            n = i + 1
            page_image_name = file[:-4] + '_' + str(n) + '.' + FORMAT_IMG
            WImage(images[i]).save(filename=dir_output + '/' + page_image_name)
            print('create IMG -', page_image_name)


def imgtoTxt(list_img_files, dir_output):
    out_txt_file = dir_output + '/' + list_img_files[0][:-6] + '.' + FORMAT_TEXT
    f = open(out_txt_file, "a")
    for img_file in list_img_files:
        img = Image.open(dir_output + '/' + img_file)
        print('ocr -', img_file)
        try:
            if 'Rotate: 270' in pytesseract.image_to_osd(img):
                img.rotate(90)
                print('rotate', img_file)
        except pytesseract.pytesseract.TesseractError:
            print('Ошибка pytesseract.image_to_osd')
        text = str((pytesseract.image_to_string(img, lang='rus')))
        text = text.replace('-\n', '')
        f.write(text)
    f.close()


def init_list_files(dir_init, format_file):
    list_files = [dir_init + '/' + img for img in os.listdir(dir_init) if img.endswith('.' + format_file)]
    list_files.sort(key=lambda x: os.path.getmtime(x))
    list_files = [x.replace(dir_init + '/', '') for x in list_files]
    return list_files


list_input_files = init_list_files(INPUT, 'pdf')

if not os.path.exists(OUTPUT):
    os.mkdir(OUTPUT)
for file in list_input_files:
    print('start work -', file)
    dir_output = OUTPUT + '/' + file[:-4]
    if not os.path.exists(dir_output):
        os.mkdir(dir_output)
    print('direct output - ', dir_output)
    #convertPDFtoImg(file, dir_output)
    list_img_files = init_list_files(dir_output, 'png')
    imgtoTxt(list_img_files, dir_output)
