from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '118912582'
API_KEY = 'xXndsrB91UREROXg6GAtY4Hg'
SECRET_KEY = 'sxSU0VsGRkla0gh1ie0cHCfAN3dYyVNW'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

result = client.synthesis('哎呦，这声音听着真亲切！我正想说说我家小孙子呢。', 'zh', 1, {
    'vol': 5,
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('audio.wav', 'wb') as f:
        f.write(result)
