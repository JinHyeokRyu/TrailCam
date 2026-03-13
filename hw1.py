import cv2 as cv
import numpy as np
import time

video = cv.VideoCapture(0)

if video.isOpened():
    # frame settings
    fps = 10
    wait_msec = int(1 / fps * 1000)

    # record settings
    video_recorder = cv.VideoWriter()
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    record_path = './data'
    recording = False
    
    # alpha blending settings
    blend_mode = False
    prev_img = None
    alpha = 0.5

    while True:
        valid, img = video.read()
        if not valid:
            break
        
        # blend
        if blend_mode and prev_img is not None:
            img = (alpha * prev_img + (1 - alpha) * img).astype(np.uint8)
        
        prev_img = img.copy()

        # record
        if recording:
            video_recorder.write(img)
            cv.putText(img, 'Recording...', (10, 30), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))

        cv.imshow('Video Player', img)


        key = cv.waitKey(wait_msec)
        
        if key == ord(' '):
            recording = not recording

            # start recording
            if recording and not video_recorder.isOpened():
                h, w, _ = img.shape
                video_recorder.open(f"{record_path}/video_{time.strftime('%Y%m%d%H%M%S')}.avi", fourcc, fps, (w, h))

            # save video file
            elif not recording:
                video_recorder.release()
                print('recorded!')

        elif key == ord('t'):
            blend_mode = not blend_mode

        elif key == 27:
            break