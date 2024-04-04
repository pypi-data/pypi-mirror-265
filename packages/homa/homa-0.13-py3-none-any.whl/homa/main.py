import cv2
import numpy
from typing import List
from .helpers import collection
from .helpers import danger

from .classes.Repository import Repository


def path(directory: str) -> None:
    Repository.directory = directory


def write(key: str, filename: str) -> None:
    cv2.imwrite(
        filename=filename,
        img=Repository.images[key]
    )


def save(key: str, filename: str) -> None:
    write(key, filename)


def image(filename: str, key: str | None = None, color: bool = True) -> None:
    # TODO: add no extension in the file
    if key is None:
        key = filename

    Repository.images[key] = cv2.imread(filename, int(color))
    return Repository.images[key]


def show(key: any = None) -> None:
    # TODO: add functionality to distinguish between camera and images

    if key is not None and not isinstance(key, str):
        Repository.imshow(f"Window #{Repository.get_counter()}", key)

    elif key is None:
        for key, image in Repository.images.items():
            Repository.imshow(key, image)

    elif key is not None:
        if key in Repository.images:
            Repository.imshow(key, Repository.images[key])
        else:
            danger(f"No image found with key {key}")

    cv2.waitKey(0)


def camera():
    capture = cv2.VideoCapture()
    _, frame = capture.read()
    Repository.camera_frame = frame


def stack(keys: List[str], new_key: str, axis: int):
    Repository.images[new_key] = numpy.concatenate(
        collection(keys).map(lambda key: Repository.images[key]),
        axis=axis
    )


def vstack(keys: List[str], new_key: str) -> None:
    stack(keys, new_key, 1)


def hstack(keys: List[str] | str, new_key: str | None = None):
    if isinstance(keys, str) and new_key is None:
        hstack([keys], keys)
        return

    stack(keys, new_key, 0)


def blur(key: str, kernel: int | List[int] = (7, 7), new_key: str | None = None):
    if new_key is None:
        new_key = key

    if isinstance(kernel, int):
        kernel = (kernel, kernel)

    Repository.images[new_key] = cv2.blur(
        Repository.images[key],
        kernel
    )


def sigma(x: float = 0, y: float = 0):
    Repository.sigmaX = x
    Repository.sigmaY = y


def gaussian(key: str, kernel: None | List[int] = None, new_key: str | None = None):
    if new_key is None:
        new_key = key

    if isinstance(kernel, int):
        kernel = (kernel, kernel)

    Repository.images[new_key] = cv2.GaussianBlur(
        Repository.images[key],
        kernel,
        sigmaX=Repository.sigmaX,
        sigmaY=Repository.sigmaY
    )
