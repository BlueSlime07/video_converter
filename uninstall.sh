#!/bin/sh

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root."
    exit 1
fi

rm -f /usr/bin/video_converter
rm -f /usr/bin/converter.py

echo "Video Converter uninstalled successfully."