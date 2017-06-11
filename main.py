import shutil
import os

import struct
import imghdr

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory



def get_sourc_path():
    path = 'AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets'
    return os.path.join(os.path.expandvars("%userprofile%"), path)


def copy_images(src, dst, mobile=False):
    os.chdir(dst)
    src_files = os.listdir(src)
    count = get_counter(dst)

    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        width, height = get_image_size(full_file_name)
        if not mobile and (height / width > 1):
            continue
        
        if width > 700 and height > 700:
            shutil.copy(full_file_name, dst)
            os.rename(file_name, '{}.jpg'.format(count))
            count +=1


def get_counter(dst):
    count = 0
    names = os.listdir(dst)
    if len(names)==0:
        return 1
    
    for name in names:
        if get_int(name) > count:
            count = get_int(name)
    return count+1


def get_int(filename):
    "return file name without extension"
    name = os.path.splitext(filename)[0]
    try:
        return int(name)
    except:
        return 0
    
            

            
# This function from stackoverflow
# link  : stackoverflow.com/questions/8032642/how-to-obtain-image-size-using-standard-python-class-without-using-external-lib
# tanks : Fred the Fantastic

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height

class Program:
    def __init__(self):
        pass
    

if __name__ == '__main__':
    root = tk.Tk()
    src = get_sourc_path()
    dst = askdirectory(initialdir="%desktop%", title='Select your pictures folder')
    copy_images(src, dst)
    exit()