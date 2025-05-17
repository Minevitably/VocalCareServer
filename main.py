from flask import Flask, request, jsonify, send_file
from io import BytesIO
from loguru import logger
from server import ServerAPI

app = Flask(__name__)

# 初始化服务
api_service = ServerAPI()

@app.route('/api/initialize_session', methods=['POST'])
def initialize_session():
    """
    初始化会话API端点
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({"error": "user_id is required"}), 400

        audio_data = api_service.handle_new_client_connection(user_id)
        return send_file(
            BytesIO(audio_data),
            mimetype='audio/mp3',  # MP3 格式
            as_attachment=False
        )

    except Exception as e:
        logger.error(f"API error in initialize_session: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/process_audio', methods=['POST'])
def process_audio():
    """
    处理音频API端点
    """
    try:
        # 获取用户ID
        user_id = request.form.get('user_id')
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400

        # 获取音频文件
        if 'audio' not in request.files:
            return jsonify({"error": "audio file is required"}), 400

        audio_file = request.files['audio']
        audio_data = audio_file.read()

        # 记录音频信息
        logger.debug(f"Received audio file: {audio_file.filename}, size: {len(audio_data)} bytes")

        # 处理音频并返回 MP3
        reply_audio = api_service.handle_user_audio(user_id, audio_data)
        return send_file(
            BytesIO(reply_audio),
            mimetype='audio/mp3',  # MP3 格式
            as_attachment=False
        )

    except Exception as e:
        logger.error(f"API error in process_audio: {e}")
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)