# video_streaming_remote_transfer
Transfer video streaming via flask and opencv
-----------
### Objective
This tool is for remote video streaming, which is designed to collect video dataset. It can automatically obtain `n` clips with `m` time length.

### Server
- app.py: start a flask server
- parameters: PORT

### Client
- client.py: get video streaming by specific timer and fps
- parameters: SERVER_IP, SERVER_PORT, VIDEO_LENGTH, VIDEO_NUM, FPS
