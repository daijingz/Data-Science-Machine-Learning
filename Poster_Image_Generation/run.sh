#!/bin/bash

# 确保 Python 脚本文件存在
if [ ! -f image_Generation.py ]; then
    echo "Error: image_Generation.py not found!"
    exit 1
fi

# 运行 Python 脚本
python image_Generation.py