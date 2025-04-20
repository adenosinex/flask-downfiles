# 使用官方 Python 基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到容器中
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

 
# 暴露 Flask 默认端口
EXPOSE 9090

# 启动应用
CMD ["python", "main.py"]