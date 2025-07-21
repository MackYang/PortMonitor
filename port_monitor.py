import json
import socket
import tkinter as tk
from threading import Thread
import asyncio
import time

# 读取配置文件
def read_config(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config.get("ports", {})

# 检查端口状态
def check_port(host, port, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port, True
    except OSError:
        return port, False

# 显示通知窗口
def show_notification(title, message):
    def run():
        root = tk.Tk()
        root.title("")
        root.overrideredirect(True)  # 去掉标题栏
        root.attributes("-topmost", True)
        

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 300
        window_height = 200  
        position_right = int(screen_width - window_width - 10)
        position_down = int(screen_height - window_height - 50)
        root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        label = tk.Label(root, text=f"{title}\n{message}", font=("Arial", 14))  # 修改文本显示格式
        label.pack(expand=True)

        # 绑定点击事件，点击时关闭窗口
        root.bind("<Button-1>", lambda event: root.destroy())

        root.after(5000, root.destroy)  # 5秒后关闭
        root.mainloop()

    Thread(target=run).start()

# 创建托盘图标
def create_tray_icon():
    # 创建一个简单的托盘图标
    icon_image = tk.PhotoImage(width=64, height=64)
    icon_image.put("blue", to=(0,0,64,64))  # 蓝色背景
    
    # 创建托盘窗口
    tray = tk.Toplevel()
    tray.withdraw()
    tray.iconphoto(True, icon_image)
    
    return tray

# 异步检查端口状态
async def async_check_port(host, port, timeout=3):
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.close()
        await writer.wait_closed()
        return port, True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return port, False

# 主程序逻辑
async def main_async():
    show_notification("Port Monitor", "Running...")

    config_path = "config.json"
    ports_config = read_config(config_path)

    host = "127.0.0.1"

    if not ports_config:
        print("未找到端口配置")
        return

    port_states = {service_name: None for service_name in ports_config.keys()}

    while True:
        port_results = {}  # 存储端口检测结果

        # 创建异步任务列表
        tasks = {
            asyncio.create_task(async_check_port(host, int(port))): service_name
            for service_name, port in ports_config.items()
            if port_states[service_name] is None or port_states[service_name] == "Fail"
        }

        # 等待所有任务完成并处理结果
        for task, service_name in tasks.items():
            try:
                port, is_open = await task
                port_results[service_name] = (port, is_open)
            except Exception as e:
                print(f"Error checking port for {service_name}: {e}")

        # 处理检测结果
        for service_name, (port, is_open) in port_results.items():
            current_state = "OK" if is_open else "Fail"
            previous_state = port_states[service_name]

            if previous_state is not None and previous_state != current_state:
                show_notification(f"{service_name}", current_state)

            port_states[service_name] = current_state

        await asyncio.sleep(2)  # 始终保持2秒检测一次

if __name__ == "__main__":
    asyncio.run(main_async())