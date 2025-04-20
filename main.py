import os
import json
import re
import requests
import threading
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
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

# 保存数据到文件
def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(data_store, f)

# 下载文件
def download_file(url, file_path):
    headers={'User-Agent':\
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',\
         }
    headers['Referer']=url
    response = requests.get(url, stream=True, headers=headers)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    return False

# 创建硬链接
def create_hard_link(source, target):
    if os.path.exists(target):
        os.remove(target)
    os.link(source, target)

# 定时任务触发器
def delayed_task(delay, task, *args, **kwargs):
    def wrapper():
        threading.Timer(delay, task, args, kwargs).start()
    return wrapper

def make_valid_windows_filename(filename):
    # 定义 Windows 文件名中不允许的特殊字符的正则表达式
    pattern = r'[\\/*?:"<>|]'
    # 使用空字符串替换特殊字符
    valid_filename = re.sub(pattern, '', filename)
    return valid_filename

@app.route('/axios' )
def file_axios():
    return send_file( 'static/axios.min.js' )
def url_toid(url):
    # 简单的URL到ID映射
    if 'vid' in url or 'video' in url:
        vid=re.findall(r'vid=(\d{19})',url)
        if vid:
            vid=vid[-1]
            print('rec2 ',url)
            return vid
# 路由：下载文件
@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    
    file_id = url_toid(url)
    if not file_id:
        return jsonify({'error': '无法从 URL 提取文件 ID'}), 400

    if not url or not file_id:
        return jsonify({'error': '缺少参数 url 或 id'}), 400

    # 提取文件名并设置目标路径
    file_name = f"{file_id}.mp4"
    file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

    # 下载文件
    if download_file(url, file_path):
        # 保存文件信息到数据存储
        

        # 延迟触发硬链接任务
        delayed_task(3, create_hard_link_task, file_id)()

        return jsonify({'message': '文件下载成功', 'file_id': file_id}), 200
    else:
        return jsonify({'error': '文件下载失败'}), 500

# 路由：保存数据
@app.route('/save', methods=['POST'])
def save():
    data = request.json
    
    metadata = data.get('data')
    if not metadata.get('now') or not ':' in  metadata.get('now'):
        return jsonify({'error': '缺少参数 now'}), 400
    
    file_id = metadata.get('id') if metadata else None

    if not file_id or not metadata:
        return jsonify({'error': '缺少参数 id 或 metadata'}), 400

    # 保存数据
    data_store[file_id] = metadata
    save_data()

    return jsonify({'message': '数据保存成功'}), 200

# 硬链接任务
def create_hard_link_task(file_id):
    if file_id not in data_store:
        print(f"文件 ID {file_id} 不存在")
        return
    t=data_store[file_id]
    file_name = data_store[file_id]['file_name']
    filename = make_valid_windows_filename(file_name)
    source = os.path.join(DOWNLOAD_FOLDER, file_id + '.mp4')
    target = os.path.join(LINK_FOLDER, file_name)

    if os.path.exists(source):
        create_hard_link(source, target)
        print(f"硬链接已创建: {target}")
    else:
        print(f"源文件不存在: {source}")

# 主函数
if __name__ == '__main__':
    app.run(debug=True,port=9090,host='0.0.0.0')