from logger import Logger
from config import Config
from utils import create_hard_link, download_file, make_valid_windows_filename
import os

class FileService:
    def __init__(self, data_store):
        self.data_store = data_store
    
    def create_hard_link_task(self, file_id):
        """创建硬链接任务"""
        if file_id not in self.data_store:
            Logger.optimized_print(f"文件 ID {file_id} 不存在")
            return
            
        file_name = self.data_store[file_id]['file_name']
        filename = make_valid_windows_filename(file_name)
        source = os.path.join(Config.DOWNLOAD_FOLDER, f"{file_id}.mp4")
        target = os.path.join(Config.LINK_FOLDER, filename)
        
        if os.path.exists(target):
            Logger.optimized_print(f"硬链接已存在: {target}")
            return
            
        if os.path.exists(source):
            create_hard_link(source, target)
            Logger.optimized_print(f"硬链接已创建: {target}")
        else:
            Logger.optimized_print(f"源文件不存在: {source}")

create_hard_link_task=FileService(Config.DATA_FILE).create_hard_link_task
