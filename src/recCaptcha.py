from cv2 import *
import numpy as np
from sklearn.cluster import KMeans
import os
from PIL import Image
import pytesseract

def charSegment(img, saveDir):
    h, w = img.shape
    pointset = np.zeros([1,2])
#    bg = np.full([h, w], 255)

    for i in range(0, h):
        for j in range(0, w):
            if img[i, j] < 100:
                #circle(bg, (j, i), 1, (0, 0, 0), -1)
                point = np.zeros([1, 2])
                point[0][0] = i
                point[0][1] = j
                pointset = np.row_stack((pointset, point))
    pointset = pointset[1:, :]
    kmeans = KMeans(n_clusters=4).fit(pointset)
    p_pre = kmeans.cluster_centers_  
    # sort the cluster centers by second column
    a_arg = np.argsort(p_pre[:, 1])

#    for k in range(0, 4):
#        circle(img, (int(p[k][1]), int(p[k][0])), 2, (0, 0, 0), -1)
#    imshow('a', img)
#    waitKey(0)
#    print pointset

    labels = kmeans.labels_
    p0 = np.zeros([1,2])
    p1 = np.zeros([1,2])
    p2 = np.zeros([1,2])
    p3 = np.zeros([1,2])
    for k in range(0, len(labels)):
        if labels[k] == 0:
            p0 = np.row_stack((p0, pointset[k]))      
        elif labels[k] == 1:
            p1 = np.row_stack((p1, pointset[k]))    
        elif labels[k] == 2:
            p2 = np.row_stack((p2, pointset[k]))
        elif labels[k] == 3:
            p3 = np.row_stack((p3, pointset[k]))
    p0 = p0[1:, :]
    p1 = p1[1:, :]
    p2 = p2[1:, :]
    p3 = p3[1:, :]
    k = 0
    p_all = [p0, p1, p2, p3]
    pnew = []

    pnew.append(p_all[a_arg[0]])
    pnew.append(p_all[a_arg[1]])
    pnew.append(p_all[a_arg[2]])
    pnew.append(p_all[a_arg[3]])
    
    if not os.path.exists(saveDir):
        os.mkdir(saveDir)
        
    white = [255, 255, 255]
    for pi in [pnew[0], pnew[1], pnew[2], pnew[3]]:
        xmax = int(pi[:, 1].max())
        xmin = int(pi[:, 1].min())
        ymax = int(pi[:, 0].max())
        ymin = int(pi[:, 0].min())
        
        Img_pi = img[ymin:(ymin+ymax-ymin), xmin:(xmin+xmax-xmin)]
        Img_pi = copyMakeBorder(Img_pi, 5, 5, 5, 5, BORDER_CONSTANT, value = white)
        imgName = 'p'+ str(k) + '.jpg'
        k+=1
        savePath = os.path.join(saveDir, imgName)
        imwrite(savePath, Img_pi)
#    rectangle(imgRGB, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)
#    imshow('img', imgRGB)
#    waitKey(0)
    #print p0, '\n', p1, '\n', p2, '\n', p3

if __name__=='__main__':
    img = imread('Captcha/4.jpg', 0)
    _, img = threshold(img, 100, 255, THRESH_BINARY)
    #imwrite('Captcha_threshold/1.jpg', img)
    charSegment(img, 'Captcha_Split')
    
    
    # ocr recognition
    d = []
    for file in os.listdir('Captcha_Split'):
        filepath = os.path.join('Captcha_Split', file)
        pytesseract.pytesseract.run_tesseract(filepath, 'out', config='-psm 10')
        f = open('out.txt', 'rb')
        d.append((f.readline())[0])
    print d