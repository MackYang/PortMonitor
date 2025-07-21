# Port Monitor

## 项目简介
Port Monitor 是一个用于监控本地端口状态的工具。它可以定期检查指定端口是否可用，并在端口状态发生变化时通过通知窗口提醒用户。

## 功能
- 定期检查端口状态（默认每 2 秒一次）。
- 支持异步端口检测，性能高效。
- 在端口状态变化时显示通知窗口。
- 支持通过配置文件 `config.json` 指定需要监控的端口。

## 使用方法

### 1. 配置文件
确保项目目录下存在 `config.json` 文件，格式如下：
```json
{
  "ports": {
    "Service A": "5000",
    "Service B": "5011",
    "Service C": "5012"
  }
}
```
- 键为服务名称，值为对应的端口号。

### 2. 运行程序
#### 直接运行
使用 Python 运行脚本：
```bash
python port_monitor.py
```

#### 打包为可执行文件
使用以下命令将程序打包为单个可执行文件：
```bash
pyinstaller --onefile --noconsole --add-data "config.json;." port_monitor.py
```
- `--noconsole` 参数确保程序在后台运行，不显示控制台窗口。
- `--add-data` 参数确保配置文件与可执行文件在同一目录下。

### 3. 运行可执行文件
双击生成的 `.exe` 文件即可运行。

## 注意事项
- 确保 `config.json` 文件与可执行文件位于同一目录。
- 程序运行时会在屏幕右下角显示通知窗口，点击通知窗口可关闭。

## 依赖
- Python 3.7 或更高版本
- 必要的 Python 库：
  - `asyncio`
  - `tkinter`
  - `socket`

## 贡献
欢迎提交问题和功能请求！

## 其他语言版本
- [English Version](./README_EN.md)
