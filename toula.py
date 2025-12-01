# toula.py
# randomizes inputs
# sets +/- 'polarity'

import time
import random
from pynput import keyboard

try:
    import vgamepad as vg
    VGAMEPAD_AVAILABLE = True
except ImportError:
    VGAMEPAD_AVAILABLE = False
    print("✗ vgamepad not available")
    print("  Install: pip install vgamepad")
    print("  Also needs ViGEmBus driver: https://github.com/ViGEm/ViGEmBus/releases")

class VirtualControllerRandomizer:
    def __init__(self, min_inputs=1, max_inputs=5, input_delay=0.3, hotkey='<f9>'):
        """
        Virtual controller randomizer - games think it's a real controller!
        
        Args:
            min_inputs: Minimum number of random inputs per trigger
            max_inputs: Maximum number of random inputs per trigger
            input_delay: Delay between each input (seconds)
            hotkey: Key to trigger randomization (default F9)
        """
        self.min_inputs = min_inputs
        self.max_inputs = max_inputs
        self.input_delay = input_delay
        self.hotkey = hotkey
        self.running = False
        self.listener = None
        self.gamepad = None
        
    def connect(self):
        """Create virtual Xbox controller"""
        if not VGAMEPAD_AVAILABLE:
            return False
        
        try:
            # Create virtual Xbox 360 controller
            self.gamepad = vg.VX360Gamepad()
            print("✓ Virtual Xbox controller created!")
            print("  Windows will see this as a real controller")
            return True
        except Exception as e:
            print(f"✗ Failed to create virtual controller: {e}")
            print("\nYou need to install ViGEmBus driver:")
            print("  1. Download from: https://github.com/ViGEm/ViGEmBus/releases")
            print("  2. Install ViGEmBus_Setup_x64.exe")
            print("  3. Restart your PC")
            print("  4. Run this script again")
            return False
    
    def disconnect(self):
        """Remove virtual controller"""
        if self.gamepad:
            # Reset all buttons before disconnecting
            self.gamepad.reset()
            self.gamepad.update()
            time.sleep(0.1)
            del self.gamepad
            print("Virtual controller removed")
    
    def inject_random_inputs(self, count=None):
        """
        Send random up/down d-pad presses via virtual controller
        
        Args:
            count: Number of inputs (random if None)
        """
        if not self.gamepad:
            print("Virtual controller not connected!")
            return
        
        if count is None:
            count = random.randint(self.min_inputs, self.max_inputs)
        print("SETTING INPUT DELAY AT TOP OF INJECT_RANDOM_INPUTS")
        
        self.input_delay = 0.05
        print(f"\n🎲 CHAOS ENGAGED - Injecting {count} random selection(s)...")
        for i in range(count):
            #direction = random.choice(['up', 'down'])
            direction = 'down'

            # Press d-pad direction
            if direction == 'up':
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
                self.gamepad.update()
                symbol = "↑"
            else:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
                self.gamepad.update()
                symbol = "↓"
            
            time.sleep(0.05)  # Hold button briefly
            
            # Release button
            self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            self.gamepad.update()
            
            print(f"  [{i+1}/{count}] {symbol}")
            
            if i < count - 1:
                time.sleep(self.input_delay)
                self.input_delay += (self.input_delay * 0.2)
                if self.input_delay >= 0.75:
                    self.input_delay = 0.75
        
        print("✓ Random selection complete!\n")
    
    def on_press(self, key):
        """Callback for key press events"""
        try:
            # Check if it's the hotkey
            if hasattr(key, 'name') and key.name == self.hotkey.strip('<>'):
                print(f">>> {self.hotkey.upper()} PRESSED <<<")
                self.inject_random_inputs()
            elif str(key) == self.hotkey:
                print(f">>> {self.hotkey.upper()} PRESSED <<<")
                self.inject_random_inputs()
        except Exception as e:
            pass
    
    def run(self):
        """Start listening for hotkey"""
        if not self.gamepad:
            print("Virtual controller not connected! Call connect() first.")
            return
        
        self.running = True
        
        print("\n" + "="*50)
        print("🎮 Hades Menu Randomizer - Virtual Controller")
        print("="*50)
        print(f"Press {self.hotkey.upper()} to inject {self.min_inputs}-{self.max_inputs} random selections")
        print("Virtual controller is active - Hades will see it as real!")
        print("Press Ctrl+C to exit")
        print("="*50 + "\n")
        
        try:
            # Start keyboard listener
            with keyboard.Listener(on_press=self.on_press) as self.listener:
                self.listener.join()
                
        except KeyboardInterrupt:
            print("\n\nStopping randomizer...")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            self.running = False
    
    def stop(self):
        """Stop listening"""
        self.running = False
        if self.listener:
            self.listener.stop()


# Standalone usage
if __name__ == "__main__":
    print("\n🎮 Hades Menu Randomizer - Virtual Controller Edition")
    print("by oyok for SGB2025")
    
    if not VGAMEPAD_AVAILABLE:
        print("\nSetup Required:")
        print("  1. pip install vgamepad")
        print("  2. Install ViGEmBus driver from:")
        print("     https://github.com/ViGEm/ViGEmBus/releases")
        print("     (Download and run ViGEmBus_Setup_x64.exe)")
        print("  3. Restart your PC")
        print("  4. Run this script again")
        exit(1)
    
    # Create randomizer
    randomizer = VirtualControllerRandomizer(
        min_inputs=10,      # Minimum random selections
        max_inputs=20,      # Maximum random selections  
        input_delay=0.05,   # Delay between inputs (seconds)
        hotkey='<f9>'      # Hotkey to trigger randomization
    )
    
    if randomizer.connect():
        print("\n💡 TIP: In Hades, you might see TWO controllers now.")
        print("   Make sure you're using your real controller for gameplay!")
        print("   The virtual one is just for randomization.\n")
        
        randomizer.run()
        randomizer.disconnect()
    else:
        print("\nFailed to create virtual controller. See setup instructions above.")
