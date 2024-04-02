from detector.detector import Detector
import numpy as np

class Runner:
    def __init__(self):
        self.detector = Detector()
        self.center = []
        self.wait = 0
        self.lms = []
    def __call__(self, frame):
        if self.wait > 0:
            self.wait -= 1
        else:
            lms = self.detector.run(frame)
            self.lms = lms
            self.save_center(lms)
            

        return self.lms

    def save_center(self, lms):
        if len(lms) > 0:
            x_center = lms[:, 0].mean()
            y_center = lms[:, 1].mean()
            if len(self.center) > 0:
                v = np.linalg.norm([self.center[0] - x_center, self.center[1] - y_center])
                print(v)
                if v < 10:
                    self.wait = 10
            self.center = [x_center, y_center]
        else:
            self.wait = 5