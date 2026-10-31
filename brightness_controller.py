
import time
import screen_brightness_control as sbc


class BrightnessController:
    """
    Controls actual monitor brightness through Windows display APIs.
    """

    def __init__(
        self,
        display=0,
        min_brightness=20,
        max_brightness=100
    ):
        self.display = display
        self.min_brightness = min_brightness
        self.max_brightness = max_brightness

        self.original_brightness = None

        self._validate_monitor()

    def _validate_monitor(self):
        """Check whether the selected monitor is accessible."""

        monitors = sbc.list_monitors()

        if not monitors:
            raise RuntimeError("No compatible monitors detected.")

        if self.display >= len(monitors) or self.display < 0:
            raise ValueError(
                f"Invalid monitor index: {self.display}"
            )

        self.original_brightness = self.get_brightness()

        print(f"Connected monitor: {monitors[self.display]}")
        print(
            f"Initial brightness: "
            f"{self.original_brightness}%"
        )

    def get_brightness(self):
        """Read current hardware brightness."""

        values = sbc.get_brightness(display=self.display)

        if not values:
            raise RuntimeError("Unable to read monitor brightness.")

        return int(values[0])

    def set_brightness(self, brightness):
        """Set actual hardware brightness."""

        brightness = int(round(brightness))

        brightness = max(
            self.min_brightness,
            min(self.max_brightness, brightness)
        )

        sbc.set_brightness(
            brightness,
            display=self.display
        )

        return self.get_brightness()

    def smooth_transition(self, target, duration=2.0, steps=10):
        """
        Gradually change brightness instead of making
        sudden brightness jumps.
        """

        target = max(
            self.min_brightness,
            min(self.max_brightness, int(target))
        )

        current = self.get_brightness()

        if steps <= 0:
            raise ValueError("Steps must be greater than zero.")

        delay = duration / steps

        for step in range(1, steps + 1):

            new_value = current + (
                (target - current) * step / steps
            )

            self.set_brightness(round(new_value))

            time.sleep(delay)

        return self.get_brightness()

    def restore_original(self):
        """Restore brightness captured during initialization."""

        if self.original_brightness is None:
            raise RuntimeError("Original brightness is unknown.")

        sbc.set_brightness(
            self.original_brightness,
            display=self.display
        )

        return self.get_brightness()


if __name__ == "__main__":

    print("=" * 55)
    print("AMBIENTFOCUS AI - BRIGHTNESS CONTROLLER")
    print("=" * 55)

    try:
        controller = BrightnessController()

        print("\nCurrent brightness:",
              controller.get_brightness(), "%")

        print("\nReducing brightness smoothly to 60%...")

        result = controller.smooth_transition(
            target=60,
            duration=3,
            steps=10
        )

        print("New brightness:", result, "%")

        print("\nRestoring original brightness...")

        restored = controller.restore_original()

        print("Restored brightness:", restored, "%")

        print("\nController test completed successfully.")

    except Exception as error:
        print("\nController error:", repr(error))
