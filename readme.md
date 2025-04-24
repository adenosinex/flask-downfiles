# Downfile Server

一个基于 Flask 的文件下载和管理服务器，支持文件下载、元数据管理和硬链接创建。

## 主要功能

### 1. 文件下载 (`/download`)
- **方法**: POST
- **功能**: 下载视频文件并创建硬链接
- **参数**: 
```json
{
    "url": "视频文件的URL"
}
```
- **响应示例**:
```json
{
    "message": "文件下载成功",
    "file_id": "123456789"
}
```

### 2. 元数据保存 (`/save`)
- **方法**: POST
- **功能**: 保存文件相关的元数据信息
- **参数**:
```json
{
    "data": {
        "id": "文件ID",
        "now": "时间戳",
        "其他元数据..."
    }
}
```
- **响应示例**:
```json
{
    "message": "数据保存成功"
}
```

### 3. 系统操作 (`/op`)
- **方法**: POST, GET
- **功能**: 提供各种系统操作接口
- **参数**: `type` (查询参数)

#### 支持的操作类型：

1. **刷新硬链接** (`type=refresh`)
   - 刷新所有文件的硬链接
   ```json
   {
       "message": "已触发硬链接刷新任务"
   }
   ```

2. **复制文件** (`type=copy`)
   - 将链接文件复制到目标目录
   ```json
   {
       "op": "copy ok"
   }
   ```

3. **获取状态** (`type=status`)
   - 获取系统运行状态
   ```json
   {
       "download_count": 10,
       "today_files": 5,
       "storage_size": {
           "downloads": {"size": 1024, "files": 10},
           "links": {"size": 1024, "files": 10}
       }
   }
   ```

## 使用示例

### 下载文件
```bash
curl -X POST http://localhost:9090/download \
     -H "Content-Type: application/json" \
     -d '{"url": "http://example.com/video.mp4"}'
```

### 保存元数据
```bash
curl -X POST http://localhost:9090/save \
     -H "Content-Type: application/json" \
     -d '{"data": {"id": "123456", "now": "2024-04-24 12:00:00"}}'
```

### 执行系统操作
```bash
# 刷新硬链接
curl "http://localhost:9090/op?type=refresh"

# 获取系统状态
curl "http://localhost:9090/op?type=status"
```

## 配置说明

项目配置通过 config.py 文件管理，主要配置项包括：

- `DOWNLOAD_FOLDER`: 下载文件存储目录
- `LINK_FOLDER`: 硬链接存储目录
- `DATA_FILE`: 数据文件路径
- `PORT`: 服务器端口 (默认: 9090)
- `HOST`: 服务器地址 (默认: '0.0.0.0')

## 注意事项

1. 确保系统有足够的存储空间
2. 文件 ID 自动从 URL 中提取
3. 所有 API 返回 JSON 格式数据
4. 支持跨域请求 (CORS)