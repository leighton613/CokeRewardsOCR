
from matplotlib import pyplot as plt
import copy
import numpy as np
import cv2

# reference: http://stackoverflow.com/a/23556997
def circle2binary(img_name, text_max=250, text_min=100, px_threshold=100,
                dilate_iter=23, debug=True):
    """
    From cap circle detect and locate text region, and convert to binary img
    img_name     :: str  :: source file
    text_max     :: int  :: max height of a character
    text_min     :: int  :: min width of a character
    px_threshold :: int  :: pixel value to detect
    dilate_iter  :: int  :: iteration number of dilate
    debug        :: bool :: True then plot process
    :r: void
    """
    # open img
    img = cv2.imread('./test image/'+img_name)


    # preprocessing (threshold + dilate)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_threshold = cv2.threshold(gray, px_threshold, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    dilated = cv2.dilate(img_threshold, kernel, iterations=dilate_iter)

    # find contour
    dilated2 = copy.copy(dilated)
    _, contours, hierarchy = cv2.findContours(dilated2, cv2.RETR_EXTERNAL,
                                              cv2.CHAIN_APPROX_TC89_KCOS)
    def adp_enhance(gray):
        """
        control mean to be within 190-210, 200
        """
        enhance_threshold = 100

        def enhance(gray, threshold=enhance_threshold):
            """
            White bg, black text
            """
            _, im_threshold = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
            mean = np.mean(im_threshold)
            return mean, im_threshold
        

        flag = 1
        while flag:
            mean, im_threshold = enhance(gray, threshold=enhance_threshold)
            diff = mean - 195 # empirical value
            if abs(diff) <= 3: break
            elif mean > 0:     # should increase threshold
                enhance_threshold += 1
            else:
                enhance_threshold -= 1
        return im_threshold
            
            
    
    



    # filter contours and plot
    num_cnt = 0
    flag = True
    for cnt in contours:
        # get rectagular bounding contour
        [x, y, w, h] = list(cv2.boundingRect(cnt))

        if h > text_max and w > text_max: continue
        if h < text_min or  w < text_min: continue

        num_cnt += 1
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,255), 2)
        output_name = './test image/'+ img_name.split('.')[0] + '-'+ str(num_cnt) + '.jpg'
        flag *= cv2.imwrite(output_name, adp_enhance(gray[y:y+h, x:x+w]))


    # write
    print 'Num of contours found:', num_cnt
    output_name = './test image/'+img_name.split('.')[0]+'-td.jpg'
    flag *= cv2.imwrite(output_name, img)


    # plot debug
    if debug == True:
        plt.subplot(1,3,1)
        plt.title("original")
        plt.imshow(img, cmap='gray')

        plt.subplot(1,3,2)
        plt.title("threshold")
        plt.imshow(img_threshold, cmap='gray')

        plt.subplot(1,3,3)
        plt.title("dilated")
        plt.imshow(dilated, cmap='gray')

    return flag