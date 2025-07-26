import cv2
import numpy as np



class lecteur:
    def __init__(self):
        self.x=0
        self.y=0
        self.im= cv2.imread("32.png")
        self.tb= self.im[self.x,self.y]

    def lire(self):
        while True:
            print(self.tb)
            self.x += 1
            if self.x == 64:
                print("oklm")
                self.x=0
                self.y += 1
            if self.y == 64:
                print('dose')
                self.y=0
            self.tb = self.im[self.x, self.y]
            if self.x==64 and self.y==64:
                break
            
cs=lecteur()
cs.lire()