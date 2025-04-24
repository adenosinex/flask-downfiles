import os
import shutil
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from config import Config
from logger import Logger
from file_handler import FileHandler
from services import FileService
from utils import (
    delayed_task, 
    url_toid, 
    save_data,
    download_file
    
)
from services import create_hard_link_task


app = Flask(__name__)
CORS(app, supports_credentials=True)

# 初始化配置
Config.init_app()

# 加载数据存储
data_store = FileHandler.load_data_store()
file_service = FileService(data_store)
old_ids = FileHandler.get_existing_ids()

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
    file_path = os.path.join(Config.DOWNLOAD_FOLDER, file_name)

    if file_id in old_ids or os.path.exists(file_path):
        return jsonify({'error': '文件已存在'}), 400

    if  download_file(url, file_path):
        delayed_task(10, create_hard_link_task, file_id)()
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
    FileHandler.save_data(data_store)

    return jsonify({'message': '数据保存成功'}), 200

@app.route('/op', methods=['POST', 'GET'])
def operation():
    """
    操作路由 - 用于处理各种操作请求
    支持的操作类型：
    - refresh: 刷新硬链接
    - clean: 清理过期数据
    - status: 获取系统状态
    """
    op_type=request.args.get('type')
    if not op_type:
        return jsonify({'error': '未指定操作类型'}), 400
        
    if op_type == 'refresh':
        delayed_task(1, initialize_hard_links)()
        return jsonify({'message': '已触发硬链接刷新任务'}), 200
        
    elif op_type == 'copy':
        # TODO: 实现清理过期数据的功能
        initialize_hard_links()
        shutil.copytree(Config.LINK_FOLDER, Config.COPYDST_FOLDER, dirs_exist_ok=True)
        return jsonify({'op': 'copy ok'}), 501
    elif op_type == 'test':
        # TODO: 实现清理过期数据的功能
        # shutil.copytree(Config.LINK_FOLDER, Config.COPYDST_FOLDER, dirs_exist_ok=True)
        return jsonify({'op': 'test ok'}), 501
        
    elif op_type == 'status':
        status = {
            'download_count': len(old_ids),
            'today_files': len(FileHandler.get_today_ids()),
            'storage_size': FileHandler.get_storage_info()
        }
        return jsonify(status), 200
        
    return jsonify({'error': '不支持的操作类型'}), 400

def initialize_hard_links():
    """
    初始化所有下载文件的硬链接。
    """
    Logger.optimized_print("初始化硬链接任务...")
    today_ids = FileHandler.get_today_ids()
    for file_id in today_ids:
        file_service.create_hard_link_task(file_id)
    Logger.optimized_print("硬链接初始化完成。")

if __name__ == '__main__':
    delayed_task(3, initialize_hard_links)()
    app.run(debug=Config.DEBUG, port=Config.PORT, host=Config.HOST)