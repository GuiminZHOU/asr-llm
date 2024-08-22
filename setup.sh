#!/bin/bash

# 定义变量
ALIYUN_AK_ID="{Aliyun AccessKey ID}"
ALIYUN_AK_SECRET="{Aliyun AccessKey Secret}"
APP_KEY="{Aliyun app key}"

# 检查audio文件夹是否存在，如果不存在则创建
if [ ! -d "audio" ]; then
    echo "Creating 'audio' directory..."
    mkdir audio
else
    echo "'audio' directory already exists."
fi

# 检查.env文件是否存在，如果不存在则创建
if [ ! -f "./.env" ]; then
    echo "Creating '.env' file..."
    touch .env
else
    echo "'.env' file already exists."
fi

# 创建.env文件并写入内容
echo "writing content to .env..."
echo -e "ALIYUN_AK_ID=${ALIYUN_AK_ID}\nALIYUN_AK_SECRET=${ALIYUN_AK_SECRET}\nAPP_KEY=${APP_KEY}" > .env

echo "init completed."