const recordBtn = document.querySelector(".record-btn")
const player = document.querySelector(".audio-player")
const download = document.querySelector('#download')
if (navigator.mediaDevices.getUserMedia) {
    let audioChunks = []
    // 约束属性
    const constraints = {
        // 音频约束
        audio: {
            sampleRate: 16000, // 采样率
            sampleSize: 16, // 每个采样点大小的位数
            channelCount: 1, // 通道数
            volume: 1, // 从 0（静音）到 1（最大音量）取值，被用作每个样本值的乘数
            echoCancellation: true, // 开启回音消除
            noiseSuppression: true, // 开启降噪功能
        },
        // 视频约束
        video: false
    }
    // 请求获取音频流
    navigator.mediaDevices.getUserMedia(constraints)
        .catch(err => serverLog("ERROR mediaDevices.getUserMedia: ${err}"))
        .then(stream => {// 在此处理音频流
            // 创建 MediaRecorder 实例;
            const mediaRecorder = new MediaRecorder(stream)
            // 点击按钮
            recordBtn.onclick = () => {
                if (mediaRecorder.state === "recording") {
                    // 录制完成后停止
                    mediaRecorder.stop()
                    recordBtn.textContent = "录音结束"
                }
                else {
                    // 开始录制
                    mediaRecorder.start()
                    recordBtn.textContent = "录音中..."
                }
            }
            mediaRecorder.ondataavailable = e => {
                audioChunks.push(e.data)
            }
            // 结束事件
            mediaRecorder.onstop = e => {
                // 将录制的数据组装成 Blob（binary large object） 对象（一个不可修改的存储二进制数据的容器）
                const blob = new Blob(audioChunks, { type: 'audio/mp4' })
                audioChunks = []
                const audioURL = window.URL.createObjectURL(blob)
                // 赋值给一个 <audio> 元素的 src 属性进行播放
                player.src = audioURL
                // 添加下载功能
                download.innerHTML = '下载'
                download.href = audioURL
            }
        },
            () => {
                console.error("授权失败！");
            }
        );
} else {
    console.error("该浏览器不支持 getUserMedia！");
}
