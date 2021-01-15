import cv2
# import os
def map():
    size = (640,480)
    videowrite =cv2.VideoWriter('map_lend.mp4',-1,4,size)
    file ='map_lend'
    # dir = os.listdir(file)
    for i in range(1,163):
        for j in range(0,24):
            if i !=1 and (j<11 or j>15):
                temp = cv2.imread(file +'\\'+str(i)+'-'+str(j)+'.png')
                videowrite.write(temp)
                print(str(i)+'-'+str(j)+'done')
def plt():
    size = (640,480)
    videowrite =cv2.VideoWriter('plt_line_2.mp4',-1,5,size)
    file ='plt_line'
    # dir = os.listdir(file)
    for i in range(11,164):
        temp=cv2.imread(file +'\\'+str(i)+'.png')
        videowrite.write(temp)
        print(str(i)+'done')
plt()