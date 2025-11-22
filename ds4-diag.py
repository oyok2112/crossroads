# DS4 Connection Diagnostic
# Let's figure out why your controller isn't being detected

import sys

print("🔍 DS4 Connection Diagnostic\n")
print("="*50)

# Test 1: Check if pydualsense is installed
print("\n[1] Checking pydualsense installation...")
try:
    import pydualsense
    print("✓ pydualsense is installed")
    print(f"  Version: {pydualsense.__version__ if hasattr(pydualsense, '__version__') else 'unknown'}")
except ImportError as e:
    print(f"✗ pydualsense not found: {e}")
    print("  Run: pip install pydualsense")
    sys.exit(1)

# Test 2: Check for HID library
print("\n[2] Checking HID library...")
try:
    import hid
    print("✓ hidapi is available")
except ImportError:
    print("✗ hidapi not found")
    print("  This might be the issue!")
    print("  Try: pip install hidapi")

# Test 3: List all HID devices
print("\n[3] Scanning for HID devices...")
try:
    import hid
    devices = hid.enumerate()
    
    print(f"Found {len(devices)} HID device(s):")
    
    ds4_found = False
    for device in devices:
        vendor_id = device['vendor_id']
        product_id = device['product_id']
        manufacturer = device['manufacturer_string']
        product = device['product_string']
        
        # DS4 Vendor ID is 0x054C (Sony)
        # DS4 Product IDs: 0x05C4 (original), 0x09CC (slim), 0x0BA0 (v2)
        is_ds4 = (vendor_id == 0x054C and 
                  product_id in [0x05C4, 0x09CC, 0x0BA0])
        
        if is_ds4 or 'sony' in manufacturer.lower() or 'wireless' in product.lower():
            print(f"\n  🎮 CONTROLLER FOUND:")
            print(f"     Vendor:  {manufacturer} (0x{vendor_id:04X})")
            print(f"     Product: {product} (0x{product_id:04X})")
            print(f"     Path:    {device['path']}")
            ds4_found = True
        
    if not ds4_found:
        print("\n  ⚠️  No DualShock 4 controller detected")
        print("     Your controller might be:")
        print("     - Not in the right mode")
        print("     - Using a different driver")
        print("     - Connected via Steam's driver")
        
except Exception as e:
    print(f"✗ Error scanning devices: {e}")

# Test 4: Try different DS4 libraries
print("\n[4] Testing alternative libraries...")

# Try pygame
try:
    import pygame
    pygame.init()
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    print(f"✓ pygame detects {joystick_count} joystick(s)")
    
    if joystick_count > 0:
        for i in range(joystick_count):
            joy = pygame.joystick.Joystick(i)
            joy.init()
            print(f"  Joystick {i}: {joy.get_name()}")
    
    pygame.quit()
except ImportError:
    print("  pygame not installed (optional)")
except Exception as e:
    print(f"  pygame error: {e}")

# Try inputs library  
try:
    import inputs
    devices = inputs.devices
    print(f"✓ inputs library detects {len(devices)} device(s)")
    for device in devices:
        print(f"  {device}")
except ImportError:
    print("  inputs library not installed (optional)")
except Exception as e:
    print(f"  inputs error: {e}")

# Test 5: Try actually connecting with pydualsense
print("\n[5] Attempting pydualsense connection...")
try:
    from pydualsense import pydualsense
    
    ds = pydualsense()
    ds.init()
    
    print("✓✓✓ SUCCESS! Controller connected via pydualsense!")
    print("    Your controller works, the issue is elsewhere")
    
    # Try to read some state
    state = ds.state
    print(f"    Battery level: {state.battery}")
    
    ds.close()
    
except Exception as e:
    print(f"✗ Failed to connect: {e}")
    print("\n💡 Troubleshooting suggestions:")
    print("   1. Try unplugging and replugging the USB cable")
    print("   2. Try a different USB port")
    print("   3. Close Steam (it might be capturing the controller)")
    print("   4. On Windows, you might need DS4Windows uninstalled")
    print("   5. Try Bluetooth instead of USB (or vice versa)")

print("\n" + "="*50)
print("Diagnostic complete!\n")

# Platform-specific tips
import platform
os_name = platform.system()
print(f"Platform: {os_name}")

if os_name == "Windows":
    print("\n💡 Windows Tips:")
    print("   - Close DS4Windows if running")
    print("   - Close Steam if running")
    print("   - Make sure no other programs are using the controller")
    print("   - Try: pip install --upgrade pydualsense")
elif os_name == "Linux":
    print("\n💡 Linux Tips:")
    print("   - You might need: sudo apt-get install libhidapi-dev")
    print("   - Check permissions: ls -l /dev/hidraw*")
    print("   - May need to run with sudo (not ideal but tests connection)")
elif os_name == "Darwin":
    print("\n💡 Mac Tips:")
    print("   - Try: brew install hidapi")
    print("   - Pair via Bluetooth might work better than USB")

print()