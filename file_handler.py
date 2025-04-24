import json
import os
from config import Config

class FileHandler:
    @staticmethod
    def load_data_store():
        """加载数据存储"""
        if os.path.exists(Config.DATA_FILE):
            with open(Config.DATA_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    @staticmethod
    def save_data(data_store):
        """保存数据到文件"""
        with open(Config.DATA_FILE, 'w') as f:
            json.dump(data_store, f)
    
    @staticmethod
    def get_existing_ids():
        """获取已存在的文件ID集合"""
        old_ids = set()
        for root, _, files in os.walk('./downloads'):
            for file in files:
                old_ids.add(file.split('.')[0])
        return old_ids
    @staticmethod
    def get_today_ids():
        """获取已存在的文件ID集合"""
        old_ids = set()
        for root, _, files in os.walk(Config.DOWNLOAD_FOLDER):
            for file in files:
                old_ids.add(file.split('.')[0])
        return old_ids
    
    @staticmethod
    def get_storage_info():
        """获取存储信息"""
        storage_info = {
            'downloads': {
                'size': 0,
                'files': 0
            },
            'links': {
                'size': 0,
                'files': 0
            }
        }
        
        # 统计下载目录
        for root, _, files in os.walk(Config.DOWNLOAD_FOLDER):
            for file in files:
                file_path = os.path.join(root, file)
                storage_info['downloads']['size'] += os.path.getsize(file_path)
                storage_info['downloads']['files'] += 1
                
        # 统计硬链接目录
        for root, _, files in os.walk(Config.LINK_FOLDER):
            for file in files:
                file_path = os.path.join(root, file)
                storage_info['links']['size'] += os.path.getsize(file_path)
                storage_info['links']['files'] += 1
                
        return storage_info