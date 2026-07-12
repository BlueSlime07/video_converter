#!/bin/sh

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root."
    exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
	echo "please insrall ffmpeg"
	exit 1
fi    

if ! command -v mkvmerge >/dev/null 2>&1; then
	echo "pleasd insrall mkvtoolnix"
	exit 1
fi 

install -m 755 converter.py /usr/bin/converter.py
chmod +x /usr/bin/converter.py
ln -sf /usr/bin/converter.py /usr/bin/video_converter

echo "Video Converter installed successfully."


if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "Please install ffmpeg."
    exit 1
fi