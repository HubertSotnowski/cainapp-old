import cv2


def calculate_pading(h, w):
    padding_w = 0
    padding_h = 0
    if int(h / 8) * 8 != h:
        padding_h = int(h / 8 + 1) * 8 - h
    if int(w / 8) * 8 != w:
        padding_w = int(w / 8 + 1) * 8 - w
    return padding_h, padding_w


print(calculate_pading(100, 100))


def getvideoinfo(filename):
    try:
        video = cv2.VideoCapture(filename)
        fps = video.get(cv2.CAP_PROP_FPS)
        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    except Exception as e:
        print("can't open video")
        print(e)
        quit()
    padding_h, padding_w = calculate_pading(height, width)
    return width, height, fps, frames, padding_h, padding_w
    Video.release()
