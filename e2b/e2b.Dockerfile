# You can use most of the Debian based images
FROM ubuntu:22.04

# Install the ffmpeg tool/
RUN apt update \
    && apt install -y ffmpeg
