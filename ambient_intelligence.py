
import cv2
import numpy as np
import time


class AmbientIntelligence:

    def __init__(self, camera_index=0, smoothing=0.2):

        self.camera_index = camera_index
        self.smoothing = smoothing

        self.camera = None
        self.smoothed_brightness = None

        self.categories = {
            "dark": (0, 45),
            "dim": (45, 85),
            "normal": (85, 150),
            "bright": (150, 256)
        }

    def start_camera(self):

        self.camera = cv2.VideoCapture(
            self.camera_index,
            cv2.CAP_DSHOW
        )

        if not self.camera.isOpened():
            raise RuntimeError(
                "Unable to connect to webcam."
            )

        print("Ambient Intelligence started.")
        print("Webcam connected successfully.")

    def estimate_brightness(self, frame):

        # Resize frame for faster processing
        resized = cv2.resize(
            frame,
            (320, 240)
        )

        # Convert image into grayscale
        grayscale = cv2.cvtColor(
            resized,
            cv2.COLOR_BGR2GRAY
        )

        # Calculate average image brightness
        brightness = float(np.mean(grayscale))

        # Apply exponential smoothing
        if self.smoothed_brightness is None:

            self.smoothed_brightness = brightness

        else:

            self.smoothed_brightness = (
                self.smoothing * brightness
                + (1 - self.smoothing)
                * self.smoothed_brightness
            )

        return round(self.smoothed_brightness, 2)

    def classify_environment(self, brightness):

        for category, limits in self.categories.items():

            lower, upper = limits

            if lower <= brightness < upper:
                return category

        return "unknown"

    def get_ambient_data(self, frame):

        brightness = self.estimate_brightness(frame)

        category = self.classify_environment(
            brightness
        )

        return {
            "brightness_score": brightness,
            "environment": category,
            "measurement_type": "relative_camera_brightness",
            "timestamp": time.time()
        }

    def release(self):

        if self.camera is not None:

            self.camera.release()
            self.camera = None

        cv2.destroyAllWindows()


if __name__ == "__main__":

    ambient = AmbientIntelligence(
        camera_index=0,
        smoothing=0.2
    )

    try:

        ambient.start_camera()

        print("\nAmbient light monitoring started.")
        print("Press Q in the webcam window to exit.\n")

        while True:

            ret, frame = ambient.camera.read()

            if not ret:
                print("Unable to capture webcam frame.")
                break

            data = ambient.get_ambient_data(frame)

            brightness = data["brightness_score"]
            environment = data["environment"]

            # Display information on webcam frame
            cv2.putText(
                frame,
                f"Brightness: {brightness}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Environment: {environment.upper()}",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.imshow(
                "AmbientFocus AI - Ambient Intelligence",
                frame
            )

            print(
                f"Brightness: {brightness:6.2f} | "
                f"Environment: {environment}"
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\nMonitoring interrupted by user.")

    except Exception as error:
        print("\nError:", repr(error))

    finally:

        ambient.release()

        print("\nAmbient Intelligence stopped.")
