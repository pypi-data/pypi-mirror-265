import cv2
import numpy as np
import os


class colorcng:

    def __init__(self,path:str, mode: str = 'all') -> None:
        self.mode = mode.lower()
        self.path=path
        
    def cng_rgb(self,opt:str, img: np.ndarray, idx: int|str = 0) -> None:
        try:
            temp = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.imwrite(os.path.join(
                self.path,opt, 'images', f'RGB_{idx}.jpg'), temp)
        except Exception as e:
            print(f"An error ocurred : {e}")

    def cng_bgr(self,opt:str, img:np.ndarray, idx: int|str = 0) -> None:
        try:
            cv2.imwrite(os.path.join(
                self.path,opt, 'images', f'BGR_{idx}.jpg'), img)
        except Exception as e:
            print(f"An error ocurred : {e}")

    def cng_gray(self,opt:str, img:np.ndarray, idx: int|str = 0) -> None:
        try:
            temp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(
                self.path,opt, 'images', f'GRAY_{idx}.jpg'), temp)
        except Exception as e:
            print(f"An error ocurred : {e}")

    def cng_hsv(self,opt:str, img:np.ndarray, idx: int|str = 0) -> None:
        try:
            temp = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            cv2.imwrite(os.path.join(
                self.path,opt, 'images', f'HSV_{idx}.jpg'), temp)
        except Exception as e:
            print(f"An error ocurred : {e}")
    
    def cng_crcb(self,opt:str,img:np.ndarray,idx:int|str =0)->None:
        try:
            temp = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            cv2.imwrite(os.path.join(
                self.path,opt, 'images', f'CrCb_{idx}.jpg'), temp)
        except Exception as e:
            print(f"An error ocurred : {e}")
            
    def cng_lab(self,opt:str, img: np.ndarray, idx: int|str = 0) -> None:
        try:
            temp = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            cv2.imwrite(os.path.join(
                self.path,opt, 'images', f'LAB_{idx}.jpg'), temp)
        except Exception as e:
            print(f"An error ocurred : {e}")
    

    def execute(self,opt:str, file: str, idx: int|str = 0)->None:
        img = cv2.imread(filename=file)
        if (self.mode == 'all'):
            self.cng_rgb(opt=opt,img=img, idx=idx)
            self.cng_bgr(opt=opt,img=img, idx=idx)
            self.cng_gray(opt=opt,img=img, idx=idx)
            self.cng_hsv(opt=opt,img=img, idx=idx)
            self.cng_crcb(opt=opt,img=img,idx=idx)
            self.cng_lab(opt=opt,img=img,idx=idx)
        else:
            if (self.mode == 'rgb'):
                self.cng_rgb(opt=opt,img=img,idx=idx)
            elif (self.mode == 'bgr'):
                self.cng_bgr(opt=opt,img=img,idx=idx)
            elif (self.mode == 'gray'):
                self.cng_gray(opt=opt,img=img,idx=idx)
            elif(self.mode=='hsv'):
                self.cng_hsv(opt=opt,img=img,idx=idx)
            elif(self.mode=='crcb'):
                self.cng_crcb(opt=opt,img=img,idx=idx)
            elif(self.mode=='lab'):
                self.cng_lab(opt=opt,img=img,idx=idx)
            else:
                print("sorry you have input a wrong operation")
                exit()
            
