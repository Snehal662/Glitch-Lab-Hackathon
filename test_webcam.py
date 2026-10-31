
import cv2

print("=" * 50)
print("AMBIENTFOCUS AI - WEBCAM TEST")
print("=" * 50)

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("ERROR: Webcam could not be opened.")
    print("Check camera connection and Windows permissions.")

else:
    print("Webcam connected successfully!")

    ret, frame = camera.read()

    if ret:
        print("Frame captured successfully!")
        print("Frame dimensions:", frame.shape)

        cv2.imshow("AmbientFocus AI - Webcam Test", frame)

        print("\nPress Q to close the webcam window.")

        while True:
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    else:
        print("ERROR: Could not capture webcam frame.")

camera.release()
cv2.destroyAllWindows()

print("\nWebcam test completed.")
