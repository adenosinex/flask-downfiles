import os
import json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from utils import save_data, download_file, create_hard_link, delayed_task, make_valid_windows_filename, url_toid

app = Flask(__name__)
CORS(app, supports_credentials=True)

# 配置
DOWNLOAD_FOLDER = './downloads'
LINK_FOLDER = './links'
DATA_FILE = './data.json'

# 确保文件夹存在
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(LINK_FOLDER, exist_ok=True)

# 加载或初始化数据存储
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        data_store = json.load(f)
else:
    data_store = {}

@app.route('/axios')
def file_axios():
    """
    提供静态文件 axios.min.js 的访问路径。
    """
    return send_file('static/axios.min.js')

@app.route('/download', methods=['POST'])
def download():
    """
    下载文件并保存到指定目录，同时延迟触发硬链接任务。
    """
    data = request.json
    url = data.get('url')
    file_id = url_toid(url)

    if not file_id:
        return jsonify({'error': '无法从 URL 提取文件 ID'}), 400

    file_name = f"{file_id}.mp4"
    file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

    if download_file(url, file_path):
        delayed_task(3, create_hard_link_task, file_id)()
        return jsonify({'message': '文件下载成功', 'file_id': file_id}), 200
    else:
        return jsonify({'error': '文件下载失败'}), 500

@app.route('/save', methods=['POST'])
def save():
    """
    保存文件的元数据到数据存储。
    """
    data = request.json
    metadata = data.get('data')

    if not metadata.get('now') or ':' not in metadata.get('now'):
        return jsonify({'error': '缺少参数 now'}), 400

    file_id = metadata.get('id') if metadata else None

    if not file_id or not metadata:
        return jsonify({'error': '缺少参数 id 或 metadata'}), 400

    data_store[file_id] = metadata
    save_data(data_store, DATA_FILE)

    return jsonify({'message': '数据保存成功'}), 200

def create_hard_link_task(file_id):
    """
    创建硬链接任务。
    """
    if file_id not in data_store:
        print(f"文件 ID {file_id} 不存在")
        return

    file_name = data_store[file_id]['file_name']
    filename = make_valid_windows_filename(file_name)
    source = os.path.join(DOWNLOAD_FOLDER, f"{file_id}.mp4")
    target = os.path.join(LINK_FOLDER, filename)

    if os.path.exists(source):
        create_hard_link(source, target)
        print(f"硬链接已创建: {target}")
    else:
        print(f"源文件不存在: {source}")

def initialize_hard_links():
    """
    程序启动时对所有已下载文件的 file_id 执行 create_hard_link_task。
    """
    print("初始化硬链接任务...")
    for file_id in data_store.keys():
        create_hard_link_task(file_id)
    print("硬链接初始化完成。")

if __name__ == '__main__':
    # 程序启动时初始化硬链接
     
    delayed_task(3, initialize_hard_links)()
    # 启动 Flask 应用
    app.run(debug=True, port=9090, host='0.0.0.0')