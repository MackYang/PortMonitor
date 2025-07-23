#!/usr/bin/env python3
"""
Test script for notification positioning
"""

import time
import threading
from port_monitor import show_notification

def test_multiple_notifications():
    """Test multiple notifications displayed simultaneously"""
    
    # Test 1: Sequential notifications
    print("Testing sequential notifications...")
    for i in range(7):  # More than max_notifications to test limiting
        show_notification(f"Service {i+1}", "OK" if i % 2 == 0 else "Fail")
        time.sleep(0.1)  # Small delay to simulate real scenario
    
    time.sleep(2)
    
    # Test 2: Simultaneous notifications (threading)
    print("Testing simultaneous notifications...")
    threads = []
    for i in range(8):
        t = threading.Thread(target=lambda i=i: show_notification(f"Thread {i+1}", "Test"))
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    print("Test completed. Check notification positioning and overlaps.")

if __name__ == "__main__":
    test_multiple_notifications()
    
    # Keep the script running to see notifications
    time.sleep(10)
