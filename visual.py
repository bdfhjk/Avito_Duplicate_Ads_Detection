import pandas as pd
import numpy as np

import cv2

IMG_WIDTH  = 208
IMG_HEIGHT = 156 
NUM_IMAGES = 9

def show_new_set(set1, set2, isdup, gen_method):

    combo_w = 0
    combo_image = np.zeros((2 * IMG_HEIGHT, NUM_IMAGES * IMG_WIDTH, 3), np.uint8)

    if not isinstance(set1, basestring):
        return

    if not isinstance(set2, basestring):
        return

    if len(set1) == 0 or len(set2) == 0:
        print( "one has no images" )
        return

    for s1 in set1.split(","):
        s1 = s1.strip()
        idx = s1[-2:]
        path = 'input/images/Images_%s/%s/%s.jpg' % ( idx[0], idx, s1 )
        if idx[0] == '0':
            path = 'input/images/Images_%s/%s/%s.jpg' % ( idx[0], idx[1], s1 )

        #print("Attempt load %s"%(path))
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if img is None:
            return
        h = img.shape[0]
        w = img.shape[1]
        #print(w,h)
        if h<1 or w<1 or img is None:
            print("Corrupt file %s"%(path))
            continue

        combo_image[0:h, combo_w:combo_w+w] = img  # copy the obj into the combo image
        combo_w += IMG_WIDTH

    combo_w = 0
    for s2 in set2.split(","):
        s2 = s2.strip()
        idx = s2[-2:]
        path = 'input/images/Images_%s/%s/%s.jpg' % ( idx[0], idx, s2 )
        if idx[0] == '0':
            path = 'input/images/Images_%s/%s/%s.jpg' % ( idx[0], idx[1], s2 )
        #print("Attempt load %s"%(path))
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if img is None:
            return
        h = img.shape[0]
        w = img.shape[1]
        #print(w,h)
        if h<1 or w<1 or img is None:
            print("Corrupt file %s"%(path))
            continue
        combo_image[IMG_HEIGHT:IMG_HEIGHT+h, combo_w:combo_w+w] = img  # copy the obj into the combo image
        combo_w += IMG_WIDTH

    dupped = 'NotDup'
    if isdup:
        dupped = 'Dup'

    cv2.imshow('%s:%d, %s vs %s' % (dupped, gen_method, set1, set2), combo_image)

    print("Showing images")
    cv2.waitKey()
    cv2.destroyAllWindows()


df = pd.read_csv("input/merged.csv", encoding="utf-8")

with_images = 0
without_images = 0
isdupc = 0
isndupc = 0

for i, row in df.head(1000).iterrows():
    if i % 100 == 0:
        print("Processing " + str(i))
    set1 = row['images_array_x']
    set2 = row['images_array_y']
    isdup = row['isDuplicate']
    genmethod = row['generationMethod']

    show_new_set(set1, set2, isdup, genmethod)

    if (not isinstance(set1, basestring)) or (not isinstance(set2, basestring)):
        without_images = without_images + 1
    else:
        with_images = with_images + 1
       
    if isdup:
        isdupc = isdupc + 1
    else:
        isndupc = isndupc + 1  


print "With images: " + str(with_images)
print "Without images: " + str(without_images)
print "-----"
print "Duplicates: " + str(isdupc)
print "Not duplicates: " + str(isndupc)
