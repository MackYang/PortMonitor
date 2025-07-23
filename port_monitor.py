import json
import socket
import tkinter as tk
from threading import Thread
import asyncio
import time

# Read configuration file
def read_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        ports = config.get("ports", {})
        
        # Validate port numbers
        validated_ports = {}
        for service_name, port in ports.items():
            try:
                port_num = int(port)
                if 1 <= port_num <= 65535:
                    validated_ports[service_name] = str(port_num)
                else:
                    print(f"Warning: Invalid port number {port} for {service_name}, skipping...")
            except ValueError:
                print(f"Warning: Invalid port format {port} for {service_name}, skipping...")
        
        return validated_ports
    except FileNotFoundError:
        print(f"Configuration file {config_path} not found")
        return {}
    except json.JSONDecodeError:
        print(f"Invalid JSON format in {config_path}")
        return {}

# Check port status
def check_port(host, port, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port, True
    except OSError:
        return port, False

# Global notification counter for positioning
notification_count = 0
max_notifications = 5  # Limit concurrent notifications

# Show notification window
def show_notification(title, message):
    global notification_count
    
    # Limit concurrent notifications
    if notification_count >= max_notifications:
        return
    
    def run():
        global notification_count
        notification_count += 1
        
        try:
            root = tk.Tk()
            root.title("")
            root.overrideredirect(True)  # Remove title bar
            root.attributes("-topmost", True)
            
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            window_width = 300
            window_height = 200  # Original height
            
            # Calculate position to avoid overlap
            notification_index = (notification_count - 1) % max_notifications
            position_right = int(screen_width - window_width - 10)
            position_down = int(screen_height - window_height - 50 - (notification_index * (window_height + 10)))
            root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

            # Set background color based on message
            bg_color = "#ffffff" 
            text_color = "#000000"
            
            root.configure(bg=bg_color)
            
            label = tk.Label(root, text=f"{title}\n{message}", font=("Arial", 12), 
                           bg=bg_color, fg=text_color, wraplength=280)
            label.pack(expand=True)

            # Bind click event, close window when clicked
            def close_window(event=None):
                root.destroy()
            
            root.bind("<Button-1>", close_window)
            label.bind("<Button-1>", close_window)

            # Auto close after 3 seconds
            def auto_close():
                if root.winfo_exists():
                    root.destroy()
            
            root.after(3000, auto_close)
            
            # Cleanup when window is destroyed
            def on_destroy():
                global notification_count
                notification_count = max(0, notification_count - 1)
            
            root.protocol("WM_DELETE_WINDOW", on_destroy)
            root.bind("<Destroy>", lambda e: on_destroy() if e.widget == root else None)
            
            root.mainloop()
            
        except Exception as e:
            print(f"Error showing notification: {e}")
        finally:
            notification_count = max(0, notification_count - 1)

    Thread(target=run, daemon=True).start()

# Create tray icon
def create_tray_icon():
    # Create a simple tray icon
    icon_image = tk.PhotoImage(width=64, height=64)
    icon_image.put("blue", to=(0,0,64,64))  # Blue background
    
    # Create tray window
    tray = tk.Toplevel()
    tray.withdraw()
    tray.iconphoto(True, icon_image)
    
    return tray

# Asynchronously check port status
async def async_check_port(host, port, timeout=3):
    try:
        # Add timeout to the connection attempt
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), 
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return port, True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError, asyncio.CancelledError):
        return port, False

# Main program logic
async def main_async():
    print("Port Monitor starting...")

    config_path = "config.json"
    ports_config = read_config(config_path)

    host = "127.0.0.1"

    if not ports_config:
        error_msg = "No valid port configuration found"
        print(error_msg)
        show_notification("Configuration Error", "Check config.json")
        return

    print(f"Monitoring {len(ports_config)} services: {', '.join(ports_config.keys())}")
    show_notification("Port Monitor", f"Monitoring {len(ports_config)} services")

    port_states = {service_name: None for service_name in ports_config.keys()}

    while True:
        port_results = {}  # Store port detection results

        # Create asynchronous task list - check all ports every time
        tasks = {
            asyncio.create_task(async_check_port(host, int(port))): service_name
            for service_name, port in ports_config.items()
        }

        # Wait for all tasks to complete and process results
        for task, service_name in tasks.items():
            try:
                port, is_open = await task
                port_results[service_name] = (port, is_open)
            except Exception as e:
                print(f"Error checking port for {service_name}: {e}")
                # Set port as failed when there's an exception
                port_results[service_name] = (ports_config[service_name], False)

        # Process detection results
        for service_name, (port, is_open) in port_results.items():
            current_state = "OK" if is_open else "Fail"
            previous_state = port_states[service_name]

            if previous_state is not None and previous_state != current_state:
                show_notification(f"{service_name}", current_state)

            port_states[service_name] = current_state

        await asyncio.sleep(2)  # Always check every 2 seconds

if __name__ == "__main__":
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\nPort Monitor stopped by user")
        show_notification("Port Monitor", "Stopped")
    except Exception as e:
        print(f"Unexpected error: {e}")
        show_notification("Port Monitor", "Error occurred")