import os
import re
import json
import requests
import threading

# 保存数据到文件
def save_data(data_store, data_file):
    """
    将数据存储到指定的 JSON 文件中。

    :param data_store: 要保存的数据字典
    :param data_file: 数据文件路径
    """
    with open(data_file, 'w') as f:
        json.dump(data_store, f)

# 下载文件
def download_file(url, file_path):
    """
    从指定的 URL 下载文件并保存到目标路径。

    :param url: 文件的下载 URL
    :param file_path: 保存文件的目标路径
    :return: 下载成功返回 True，否则返回 False
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Referer': url
    }
    response = requests.get(url, stream=True, headers=headers)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    return False

# 创建硬链接
def create_hard_link(source, target):
    """
    创建硬链接，如果目标文件已存在则先删除。

    :param source: 源文件路径
    :param target: 硬链接目标路径
    """
    if os.path.exists(target):
        os.remove(target)
    os.link(source, target)

# 定时任务触发器
def delayed_task(delay, task, *args, **kwargs):
    """
    延迟执行指定任务。

    :param delay: 延迟时间（秒）
    :param task: 要执行的任务函数
    :param args: 任务函数的参数
    :param kwargs: 任务函数的关键字参数
    """
    def wrapper():
        threading.Timer(delay, task, args, kwargs).start()
    return wrapper

# 生成有效的 Windows 文件名
def make_valid_windows_filename(filename):
    """
    将文件名中的非法字符替换为空字符串，生成有效的 Windows 文件名。

    :param filename: 原始文件名
    :return: 有效的文件名
    """
    pattern = r'[\\/*?:"<>|]'
    valid_filename = re.sub(pattern, '', filename)
    return valid_filename

# 从 URL 提取文件 ID
def url_toid(url):
    """
    从 URL 中提取文件 ID。

    :param url: 文件的 URL
    :return: 提取的文件 ID，如果无法提取则返回 None
    """
    if 'vid' in url or 'video' in url:
        vid = re.findall(r'vid=(\d{19})', url)
        if vid:
            return vid[-1]
    return None