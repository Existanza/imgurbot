# written for Python version 3.4.1
__author__ = 'Deca'
# http://stackoverflow.com/questions/10945542/python3-urllib-image-retreval
# http://www.wykop.pl/link/1008101/masz-za-duzo-wolnego-czasu-zapraszam/
# http://pillow.readthedocs.org/en/latest/reference/Image.html
# http://blog.zeevgilovitz.com/detecting-dominant-colours-in-python/
import urllib.request
import string
import random
import os
import imghdr
from PIL import Image


n, a, t = 0, 0, 0
SIZE = 5             # length of the randomized image name; possible values: 5,7; default value: 5
DISK_SPACE_AVL = 1   # the maximum amount of disk space the program can use during its execution in GB; default value: 1
path = os.path.join(os.path.expanduser('~'), 'Desktop', 'WAZNE-MATURA') + '\\'


def random_img():
    '''Randoms an url.'''
    return ''.join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(SIZE)])


def open_image(tmp_path, extension):
    '''Finds the most common colour in the picture.'''
    if extension is 'gif':
        return True
    else:
        t_im = Image.open(tmp_path)
        t_im.save(path + 'tmp_v2.gif', 'GIF')
        t_im.close()
        n_im = Image.open(path + 'tmp_v2.gif')
        size_tuple = n_im.size
        new_l = int(size_tuple[0]/5*2)
        new_u = int(size_tuple[1]/5*2)
        new_r = int(size_tuple[0]/5*3)
        new_b = int(size_tuple[1]/5*3)
        colors = [0 for x in range(256)]
        i = new_l
        j = new_u
        while i < new_r:
            while j < new_b:
                xy_list = [i, j]
                pixel = n_im.getpixel(tuple(xy_list))
                colors[pixel] += 1
                j += 1
            i += 1
            j = new_u
        most_frequent_color = [0, 0]
        for i in range(256):
            if colors[i] > most_frequent_color[0]:
                most_frequent_color[1] = i
                most_frequent_color[0] = colors[i]
        pixel = -1
        while pixel != most_frequent_color[1]:
            i = random.randint(new_l, new_r)
            j = random.randint(new_u, new_b)
            xy_list = [i, j]
            pixel = n_im.getpixel(tuple(xy_list))
        most_frequent_color_tuple = (i, j)
        rgb_im = n_im.convert('RGB')
        rgb_tuple = rgb_im.getpixel(most_frequent_color_tuple)
        n_im.close()
        print(rgb_tuple)
        r, g, b = rgb_tuple
        rgb_im.close()
        if (r-5) > g and (r-5) > b and r > 50:
            return True
        else:
            return False


def get_img(imgurl):
    '''Finds a random image and downloads it if the image exists.'''
    global n, a, t
    a += 1
    fullurl = 'http://i.imgur.com/' + imgurl + '.gif'
    try:
        u = urllib.request.urlopen(fullurl)
    except BaseException as e:
        print("error: cannot retrieve image")
        print(e)
        return
    raw_data = u.read()
    u.close()
    if len(raw_data)/(1024 ** 2) >= 0.01:
        try:
            n += 1
            t += len(raw_data)/(1024 ** 2)
            ft = open(tmp_path,'wb')
            ft.write(raw_data)
            ft.close()
            ext = imghdr.what(tmp_path, raw_data)
            is_nsfw = open_image(tmp_path, ext)
            if not ext:
                ext = 'jpg'
            os.remove(path + 'tmp' + '.gif')
            if ext is not 'gif':
                os.remove(path + 'tmp_v2' + '.gif')
            fullurl = 'http://i.imgur.com/' + imgurl + '.' + ext
            print('\r', 'Try %d.' % a, is_nsfw, 'URL: {0}'.format(fullurl), ' saved %.2f MB, total %.2f MB' % (len(raw_data)/(1024 ** 2), t))
            if is_nsfw:
                if ext is 'gif':
                    save_path = path + 'gif' + '\\' + imgurl + '.' + ext
                else:
                    save_path = path + 'nsfw' + '\\' + imgurl + '.' + ext
            else:
                save_path = path + imgurl + '.' + ext
            f = open(save_path, 'wb')
            f.write(raw_data)
            f.close()
        except:
            print(' couldn\'t write to ' + path + imgurl)
    print('\r' + 'Try ' + str(a) + '.', end='')

if not os.path.exists(path):
    os.makedirs(path)
if not os.path.exists(path + '\\' + 'nsfw' + '\\'):
    os.makedirs(path + '\\' + 'nsfw' + '\\')
if not os.path.exists(path + '\\' + 'gif' + '\\'):
    os.makedirs(path + '\\' + 'gif' + '\\')

tmp_path = path + 'tmp' + '.gif'

random.seed()

while t < DISK_SPACE_AVL*1024:
    get_img(random_img())