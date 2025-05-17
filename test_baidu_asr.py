from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '118912582'
API_KEY = 'xXndsrB91UREROXg6GAtY4Hg'
SECRET_KEY = 'sxSU0VsGRkla0gh1ie0cHCfAN3dYyVNW'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 识别本地文件
result = client.asr(get_file_content('audio.pcm'), 'pcm', 16000, {
    'dev_pid': 1537,  # 1537 表示普通话（支持简单英文）
})

print(result)  # 打印识别结果



