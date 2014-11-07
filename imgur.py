# written for Python version 3.4.1
__author__ = 'Deca'
# http://stackoverflow.com/questions/10945542/python3-urllib-image-retreval
# http://www.wykop.pl/link/1008101/masz-za-duzo-wolnego-czasu-zapraszam/
import urllib.request
import string
import random
import os
import imghdr

n, a, t = 0, 0, 0
SIZE = 5             # length of the randomized image name; possible values: 5,7; default value: 5
DISK_SPACE_AVL = 1   # the maximum amount of disk space the program can use during its execution in GB; default value: 1
path = os.path.join(os.path.expanduser('~'), 'Desktop', 'WAZNE-MATURA') + '\\'

def random_img():
    '''Randoms an url,'''
    return ''.join([random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(SIZE)])

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
            ft = open(path + 'tmp' + '.gif','wb')
            ft.write(raw_data)
            ft.close()
            ext = imghdr.what(path + 'tmp' + '.gif', raw_data)
            if not ext:
                ext = 'jpg'
            os.remove(path + 'tmp' + '.gif')
            fullurl = 'http://i.imgur.com/' + imgurl + '.' + ext
            print('\r', 'Try %d.' % a, 'Retrieved: {0}'.format(fullurl), ' saved %.2f MB, total %.2f MB' % (len(raw_data)/(1024 ** 2), t) )
            f = open(path + imgurl + '.' + ext,'wb')
            f.write(raw_data)
            f.close()
        except:
            print('couldn\'t write to' + path + imgurl + '.gif')
    print('\r' + 'Try ' + str(a) + '.', end='')

if not os.path.exists(path):
    os.makedirs(path)

while t < DISK_SPACE_AVL*1024:
    get_img(random_img())