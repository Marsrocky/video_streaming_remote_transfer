import cv2
import time
import requests
import numpy as np

server_IP = '127.0.0.1'
port = 5000
video_length = 5 # seconds
video_num = 5
ctr = 0

fps = 10
video_size = (1280, 720)

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
# Define the fps to be equal to 10. Also frame size is passed.
# cap height/width should be checked in the server side

start_time = time.time()
# Initialize videowriter
# codec: *'XVID' saves more space
video_name = ''.join(['data/', str(ctr), '.avi'])
out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('M','J','P','G'), fps, video_size)

r = requests.get('http://'+server_IP+':'+str(port)+'/video_feed', stream=True)
if(r.status_code == 200):
    # Receive streaming
    bytes = bytes()
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
                print ('[LOG] {} successfully saved'.format(video_name))
                ctr += 1
                if ctr == video_num:    # stop
                    out.release()
                    cv2.destroyAllWindows()
                    exit(0)
                else:   # next video clip
                    out.release()
                    video_name = ''.join(['data/', str(ctr), '.avi'])
                    out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('M','J','P','G'), 10, video_size)
                    start_time = time.time()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                out.release()
                cv2.destroyAllWindows()
                exit(0)

else:
    print("Received unexpected status code {}".format(r.status_code))