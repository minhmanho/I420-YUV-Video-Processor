# I420-YUV-Video-Processor
This Video Processor can help you to read I420 YUV video format.

Sample code:

vid_in = '1280x720_Johnny_50.yuv'
vid_out = 'video_out.yuv'
video_processor1 = VideoProcessor(vid_in, h=720, w=1280, mode='RGB', read_once=True)

for i, frame in enumerate(video_processor1.vid_arr):
    cv2.imshow('Frame', frame)
    cv2.imwrite('images/' + str(i) + '.jpg', frame)
    print(frame.shape)
    cv2.waitKey(0)
video_processor1.save_vid(vid_out)
video_processor1.release()

video_processor2 = VideoProcessor(vid_in, h=720, w=1280, mode='BGR', read_once=False)
while True:
    _, frame = video_processor2.read()
    if frame is None:
        break
    cv2.imshow('Frame', frame)
    cv2.waitKey(1)
video_processor2.release()

