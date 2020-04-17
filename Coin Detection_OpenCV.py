import numpy as np
import cv2
  
# Using cv2.imread() method 
def read_image():
    
    global img
    img = cv2.imread('capstone_coins.png',cv2.IMREAD_GRAYSCALE)
    global original_image
    original_image = cv2.imread('capstone_coins.png',1)


def draw_circles(original_image):
    global circles
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 0.9, 150,param1=50,param2=27,minRadius=60,maxRadius=120)
    print(circles)

    circles = np.uint16(np.around(circles))
    count=1
    
    for i in circles[0,:]:
        
        # draw the outer circle
        cv2.circle(original_image,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(original_image,(i[0],i[1]),2,(0,0,255),3)
        # cv2.putText(original_image, str(count),(i[0],i[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2)
        count += 1

'''Function Calls'''
pic=read_image()
draw=draw_circles(original_image)         


def get_radii(circles):
    global radius
    radius=[]
    for coord in circles[0,:]:
        radius.append(coord[2])
    return radius

def av_pix(img,circles,size):
    global av_val
    av_val=[]
    for coords in circles[0,:]:
        col=np.mean(img[coords[1]-size:coords[1]+size,coords[0]-size:coords[0]+size])
        av_val.append(col)
    return av_val

def classification_coins(bright_val,radii):
    global values 
    values=[]
    for a,b in zip(bright_val,radii):
        if a > 150 and b > 110:
            values.append(10)
        elif a > 150 and b <= 110:
            values.append(5)
        elif a < 150 and b > 110:
            values.append(2)
        elif a < 150 and b < 110:
            values.append(1)    
    return values

def show_image():
    count_2 = 0
    for i in circles[0,:]:
        
        cv2.putText(original_image, str(values[count_2]) + 'p',(i[0],i[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2)
        count_2 += 1
    cv2.putText(original_image, 'ESTIMATED TOTAL VALUE: ' + str(sum(values)) + 'p', (200,100), cv2.FONT_HERSHEY_SIMPLEX, 1.3, 255)
    global img
    img = cv2.GaussianBlur(img,(5,5),0)
    cv2.imshow('Detected Coins',original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



'''Function Calls'''

radii=get_radii(circles)
print(radii)

get_bright=av_pix(img, circles, 20)
print(get_bright)

classified=classification_coins(get_bright,radii)
print(classified)

z=show_image()