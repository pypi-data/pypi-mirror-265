import numpy as np
import cv2
from runner.runner import Runner
import time
import psutil, os

class FPS:
    def __init__(self):
        self.num = 0
        self.fps = 0
        self.s = time.time()

    def __call__(self):
        if time.time() - self.s < 1:
            self.num += 1
            return -1
        else:
            self.fps = self.num
            self.num = 0
            self.s = time.time()
            return self.fps
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    run = Runner()
    fps = FPS()
    process = psutil.Process(os.getpid())
    process.nice(psutil.HIGH_PRIORITY_CLASS)
    c = 0
    while True:
        #time.sleep(1)
        _, frame = cap.read()
    
        lms = run(frame)
        
        
        fff = fps()
        if fff != -1:
            print(fff)
        #print('FPS: ', )
        
        for lm in lms:
            for x,y in lm:
                cv2.circle(frame, (x, y), 5, (0,255,0))
        cv2.imshow('window', frame)

        if cv2.waitKey(1) > -1:
            break
    cv2.destroyAllWindows()

