# DS4 Touchpad Randomizer with LED Control
# Direct hidapi implementation to bypass import issues

import time
import random
import pyautogui
import struct

try:
    import hid
    HID_AVAILABLE = True
except:
    HID_AVAILABLE = False

class DS4Controller:
    # DS4 USB identifiers
    VENDOR_ID = 0x054C
    PRODUCT_IDS = [0x05C4, 0x09CC, 0x0BA0]  # Original, Slim, V2
    
    def __init__(self):
        self.device = None
        self.product_id = None
        
    def connect(self):
        """Find and connect to DS4 controller"""
        if not HID_AVAILABLE:
            print("✗ hid module not available")
            return False
        
        try:
            # Try to find DS4
            for pid in self.PRODUCT_IDS:
                try:
                    self.device = hid.device()
                    self.device.open(self.VENDOR_ID, pid)
                    self.product_id = pid
                    
                    manufacturer = self.device.get_manufacturer_string()
                    product = self.device.get_product_string()
                    
                    print(f"✓ DS4 Connected!")
                    print(f"  {manufacturer} {product}")
                    
                    # Set non-blocking mode
                    self.device.set_nonblocking(1)
                    
                    return True
                except:
                    continue
            
            print("✗ No DS4 controller found")
            print("  Make sure it's plugged in via USB")
            return False
            
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from controller"""
        if self.device:
            self.device.close()
            print("DS4 disconnected")
    
    def set_led_color(self, r, g, b):
        """
        Set the DS4 LED color
        
        Args:
            r, g, b: RGB values 0-255
        """
        if not self.device:
            return False
        
        try:
            # DS4 USB LED command
            # Format varies by model, this works for most
            report = bytearray(32)
            report[0] = 0x05  # Report ID
            report[1] = 0xFF  # ??
            report[4] = 0x00  # rumble right
            report[5] = 0x00  # rumble left  
            report[6] = r     # Red
            report[7] = g     # Green
            report[8] = b     # Blue
            
            self.device.write(bytes(report))
            return True
            
        except Exception as e:
            print(f"LED error: {e}")
            return False
    
    def read_input(self):
        """
        Read controller state
        Returns dict with button states
        """
        if not self.device:
            return None
        
        try:
            data = self.device.read(64)
            if not data or len(data) < 10:
                return None
            
            # Parse DS4 input report
            # Button mapping for USB mode
            buttons = {
                'touchpad': bool(data[7] & 0x02),  # Touchpad click
                'triangle': bool(data[5] & 0x80),
                'circle': bool(data[5] & 0x40),
                'cross': bool(data[5] & 0x20),
                'square': bool(data[5] & 0x10),
            }
            
            return buttons
            
        except Exception as e:
            return None


class TouchpadRandomizerLED:
    def __init__(self, min_inputs=1, max_inputs=5, input_delay=0.3):
        self.controller = DS4Controller()
        self.min_inputs = min_inputs
        self.max_inputs = max_inputs
        self.input_delay = input_delay
        self.running = False
        self.touchpad_was_pressed = False
        
        # LED colors for different states
        self.color_idle = (0, 0, 50)      # Blue when idle
        self.color_active = (50, 0, 50)   # Purple when randomizing
        self.color_complete = (0, 50, 0)  # Green when complete
    
    def connect(self):
        """Connect to DS4"""
        if not HID_AVAILABLE:
            print("\n⚠️  hid module not available!")
            print("This means hidapi.dll is missing on your system.")
            print("\nTry:")
            print("  1. Download hidapi.dll from: https://github.com/libusb/hidapi/releases")
            print("  2. Place it in C:\\Windows\\System32\\")
            print("  OR use the pygame version for basic functionality")
            return False
        
        return self.controller.connect()
    
    def disconnect(self):
        """Disconnect and reset LED"""
        if self.controller.device:
            # Reset to blue on exit
            self.controller.set_led_color(0, 0, 50)
            time.sleep(0.1)
        self.controller.disconnect()
    
    def inject_random_inputs(self, count=None):
        """Inject random menu selections with LED feedback"""
        if count is None:
            count = random.randint(self.min_inputs, self.max_inputs)
        
        # Set LED to active color
        self.controller.set_led_color(*self.color_active)
        
        print(f"\n🎲 CHAOS ENGAGED - Injecting {count} random selection(s)...")
        
        for i in range(count):
            direction = random.choice(['up', 'down'])
            pyautogui.press(direction)
            
            symbol = "↑" if direction == "up" else "↓"
            print(f"  [{i+1}/{count}] {symbol}")
            
            if i < count - 1:
                time.sleep(self.input_delay)
        
        # Flash green
        self.controller.set_led_color(*self.color_complete)
        time.sleep(0.3)
        self.controller.set_led_color(*self.color_idle)
        
        print("✓ Random selection complete!\n")
    
    def run(self):
        """Main loop"""
        if not self.controller.device:
            print("Controller not connected!")
            return
        
        # Set initial LED color
        self.controller.set_led_color(*self.color_idle)
        
        print("\n" + "="*50)
        print("🎮 DS4 Touchpad Randomizer with LED Control!")
        print("="*50)
        print(f"Press TOUCHPAD to inject {self.min_inputs}-{self.max_inputs} random selections")
        print("LED: Blue=idle, Purple=randomizing, Green=complete")
        print("Press Ctrl+C to exit")
        print("="*50 + "\n")
        
        self.running = True
        
        try:
            while self.running:
                buttons = self.controller.read_input()
                
                if buttons:
                    touchpad_pressed = buttons.get('touchpad', False)
                    
                    # Detect rising edge
                    if touchpad_pressed and not self.touchpad_was_pressed:
                        print(">>> TOUCHPAD PRESSED <<<")
                        self.inject_random_inputs()
                    
                    self.touchpad_was_pressed = touchpad_pressed
                
                time.sleep(0.01)  # 100Hz polling
                
        except KeyboardInterrupt:
            print("\n\nStopping randomizer...")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            self.running = False


# Main
if __name__ == "__main__":
    print("\n🎮 Hades Menu Randomizer - DS4 LED Edition")
    print("by oyok for SGB2025\n")
    
    randomizer = TouchpadRandomizerLED(
        min_inputs=1,
        max_inputs=5,
        input_delay=0.3
    )
    
    if randomizer.connect():
        randomizer.run()
        randomizer.disconnect()
    else:
        print("\nFailed to connect to DS4")
        print("\nIf you keep getting hidapi errors, we may need to:")
        print("  1. Download hidapi.dll manually")
        print("  2. Use a different library")
        print("  3. Try the pygame version (no LED control though)")