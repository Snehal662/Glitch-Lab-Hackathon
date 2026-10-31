
import screen_brightness_control as sbc

print("=" * 55)
print("AMBIENTFOCUS AI - DISPLAY DETECTION")
print("=" * 55)

try:
    monitors = sbc.list_monitors()

    print(f"\nDetected monitors: {len(monitors)}")

    for index, monitor in enumerate(monitors):
        print(f"\nMonitor {index}: {monitor}")

    print("\nDetailed monitor information:")

    info = sbc.list_monitors_info()

    for index, monitor in enumerate(info):
        print(f"\nMonitor {index}:")

        for key, value in monitor.items():
            print(f"{key}: {value}")

    print("\nCurrent brightness:")

    brightness = sbc.get_brightness()

    for index, value in enumerate(brightness):
        print(f"Monitor {index}: {value}%")

except Exception as error:
    print("\nDisplay detection failed.")
    print("Error:", repr(error))

print("\nDetection test completed.")
