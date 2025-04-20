使用 Docker CLI
构建镜像：
docker build -t downfile-server .
运行容器：
docker run -d -p 9090:9090 -v ${PWD}/downloads:/app/downloads -v ${PWD}/links:/app/links -v ${PWD}/data.json:/app/data.json downfile-server
使用 Docker Compose
构建并启动服务：
docker-compose up --build -d
停止服务：
docker-compose down
5. 验证
访问 http://localhost:9090，确认 Flask 应用已成功运行