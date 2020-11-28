import cv2
import numpy
import os
import time

color_mode = ['YUV', 'BGR', 'RGB']

class VideoProcessor:
    def __init__(self, video_url, h=None, w=None, mode='RGB', fps=25, read_once=True):
        assert mode in color_mode, "VideoProcessor mode must be RGB or BGR"
        self.file_name, _ext = video_url.split('/')[-1].split('.')
        self.is_yuv = True if _ext == 'yuv' else False
        self.mode = mode
        self.read_once = read_once
        if self.is_yuv:
            print("Read I420 YUV format")
            assert (w is not None or h is not None), "Width and Height are required to read rawvideo"
            self.w = int(w)
            self.h = int(h)
            self.fps = fps
            self.frame_size = self.w * self.h
            self.frame_length = int((self.frame_size * 3) / 2)
            self.video_size = os.stat(video_url)[6]
            self.num_frames = int(self.video_size / self.frame_length)
            self.f = open(video_url, 'rb')
        else:
            self.cap = cv2.VideoCapture(video_url)
            self.num_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.vid_arr = []
        if self.read_once:
            for i in range(self.num_frames):
                if i % (self.num_frames/2) == 0:
                    print ("Video loading is {0}% done.".format((i / (self.num_frames / 10) * 10)))
                _, frame = self.read()
                self.vid_arr.append(frame)

    def read(self):
        if self.is_yuv:
            try:
                raw = self.f.read(self.frame_length)
                yuv = numpy.frombuffer(raw, dtype=numpy.uint8)
                yuv = yuv.reshape((int(self.h*1.5), self.w))
                frame = yuv
                if self.mode == 'RGB':
                    frame = cv2.cvtColor(frame, cv2.COLOR_YUV2RGB_I420)
                elif self.mode == 'BGR':
                    frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)
                return True, frame
            except:
                return False, None
        else:
            ret, frame = self.cap.read()
            if self.mode == 'RGB':
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return ret, frame

    def save_vid(self, vid_out_path):
        assert self.vid_arr != [], " VideoProcessor.vid_arr is empty"
        if self.is_yuv:
            print('YUV writer')
            f = open(vid_out_path, 'wb')
            for _, frame in enumerate(self.vid_arr):
                yuv_frame = frame
                if self.mode == 'RGB':
                    yuv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2YUV_I420)
                elif self.mode == 'BGR':
                    yuv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_I420)
                yuv_frame = yuv_frame.reshape((self.frame_length, ))
                binary_frame = yuv_frame.tostring()
                f.write(binary_frame)
            f.close()
        else:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(vid_out_path, fourcc, self.fps, (self.w, self.h))

            for frame in self.vid_arr:
                if self.mode == 'RGB':
                    out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                elif self.mode == 'BGR':
                    out.write(frame)
            out.release()

    def release(self):
        if self.is_yuv:
            self.f.close()
        else:
            self.cap.release()
