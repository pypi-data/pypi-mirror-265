from ..helpers import is_colab


class RepositoryWrapper:
    def __init__(self):
        self.sigmaX = 0
        self.sigmaY = 0

        self.directory = "./"
        self.images = {}
        self.cameras = {}
        self.window_counter = 0

        if is_colab():
            from google.colab.patches import cv2_imshow as imshow
        else:
            from cv2 import imshow

        self.imshow = imshow

    def get_counter(self):
        self.window_counter += 1
        return self.window_counter

    def __getattr__(self, name: str) -> any:
        pass


Repository = RepositoryWrapper()
