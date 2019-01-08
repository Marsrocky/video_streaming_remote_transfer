import cv2
import time
import requests
import numpy as np

server_IP = '127.0.0.1'
port = 5000
video_length = 4 # seconds
video_num = 3
ctr = 0

fps = 25
video_size = (1280, 720)

r = requests.get('http://'+server_IP+':'+str(port)+'/video_feed', stream=True)
if(r.status_code == 200):
    # Initialize videowriter
    # codec: *'XVID' saves more space
    video_name = ''.join(['data/', str(ctr), '.avi'])
    out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('M','J','P','G'), fps, video_size)

    # Receive streaming
    bytes = bytes()
    start_time = time.time()
    for chunk in r.iter_content(chunk_size=1024*10):
        bytes += chunk
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            # show streaming
            # cv2.imshow('frame', frame)

            # save video to file
            out.write(frame)

            if time.time() - start_time > video_length:
                out.release()
                print ('[LOG] {} successfully saved'.format(video_name))
                ctr += 1
                if ctr == video_num:    # stop
                    cv2.destroyAllWindows()
                    exit(0)
                else:   # next video clip
                    video_name = ''.join(['data/', str(ctr), '.avi'])
                    out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('M','J','P','G'), fps, video_size)
                    start_time = time.time()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                out.release()
                cv2.destroyAllWindows()
                exit(0)

else:
    print("Received unexpected status code {}".format(r.status_code))