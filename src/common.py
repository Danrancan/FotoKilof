# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

""" moduł z funkcjami ogólnego przeznaczenia """

import fnmatch
import os
import platform
import re
import urllib
from PIL import Image


def imagemagick_zip_find():
    """ searching zip file to download from ImageMagick website """
    url = 'https://imagemagick.org/script/download.php'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    response_data = response.read()
    match = re.search(r'ftp://ftp.imagemagick.org/pub/ImageMagick/binaries/ImageMagick-[0-9]+.[0-9]+.[0-9]+-[0-9]+portable-Q16-x64.zip', response_data)
    if match:
        print(match.group())
        result = match.group()
    else:
        result = None
    return result


def mouse_crop_calculation(file, size):
    """ przeliczenie pikseli podglądu  na piksele oryginału """
    # global file_in_path
    img = Image.open(file)
    x_orig = img.size[0]
    y_orig = img.size[1]

    # x_max, y_max - wymiary podglądu, znamy max czyli PREVIEW
    if x_orig > y_orig:
        # piksele podglądu, trzeba przeliczyć y_max podglądu
        x_max = size
        y_max = x_max*y_orig/x_orig
    elif y_orig > x_orig:
        # przeliczenie x
        y_max = size
        x_max = y_max*x_orig/y_orig
    elif y_orig == x_orig:
        x_max = size
        y_max = size

    dict_return = {}
    dict_return['x_max'] = x_max
    dict_return['y_max'] = y_max
    dict_return['x_orig'] = x_orig
    dict_return['y_orig'] = y_orig
    return dict_return


def spacja(sciezka):
    """ escaping space and special char in pathname """

    sciezka = os.path.normpath(sciezka)
    if platform.system() == "Windows":
        czy_spacja = re.search(" ", sciezka)
        if czy_spacja is not None:
            sciezka = '"' + sciezka + '"'
    else:
        path = os.path.splitext(sciezka)
        sciezka = re.escape(path[0]) + path[1]

    return sciezka

def list_of_images(cwd):
    """
    jpg and png images in cwd
    return sorted list
    """

    list_of_files = os.listdir(cwd)
    file_list = []
    pattern = "*.jpg"
    for file in list_of_files:
        if fnmatch.fnmatch(file, pattern):
            file_list.append(file)
    pattern = "*.png"
    for file in list_of_files:
        if fnmatch.fnmatch(file, pattern):
            file_list.append(file)

    file_list.sort()
    return file_list


def file_from_list_of_images(file_list, current_file, request):
    """return filename from file_list depends of request
    request: position on the list
    """
    if file_list:
        if request == "first":
            file = file_list[0]
        elif request == "previous":
            position = file_list.index(current_file)
            if position > 0:
                file = file_list[position - 1]
            else:
                file = None
        elif request == "next":
            position = file_list.index(current_file)
            if position <= len(file_list) - 2:
                file = file_list[position + 1]
            else:
                file = None
        elif request == "last":
            file = file_list[-1]
        else:
            file = None

    else:
        file = None

    if file == current_file:
        file = None
    return file

# EOF
