
import screen_brightness_control as sbc
import time

MONITOR = 0
TEST_BRIGHTNESS = 70

print("=" * 55)
print("AMBIENTFOCUS AI - HARDWARE BRIGHTNESS TEST")
print("=" * 55)

try:
    # Read original brightness
    original = sbc.get_brightness(display=MONITOR)[0]

    print(f"\nOriginal brightness: {original}%")

    # Change actual monitor brightness
    print(f"Changing brightness to {TEST_BRIGHTNESS}%...")

    sbc.set_brightness(TEST_BRIGHTNESS, display=MONITOR)

    time.sleep(2)

    # Verify brightness
    current = sbc.get_brightness(display=MONITOR)[0]

    print(f"Current brightness: {current}%")

    if current == TEST_BRIGHTNESS:
        print("\nSUCCESS: Brightness changed successfully!")
    else:
        print("\nWARNING: Requested brightness was not confirmed.")

    print("\nKeep the test brightness for 10 seconds.")
    time.sleep(10)

    # Restore original brightness
    print("\nRestoring original brightness...")

    sbc.set_brightness(original, display=MONITOR)

    time.sleep(2)

    restored = sbc.get_brightness(display=MONITOR)[0]

    print(f"Restored brightness: {restored}%")

except Exception as error:
    print("\nBRIGHTNESS CONTROL FAILED")
    print("Error:", repr(error))

print("\nHardware test completed.")
