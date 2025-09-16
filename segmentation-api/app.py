import cv2

def run_segmentation():
    cap = cv2.VideoCapture(0)  # 0 = default webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Simple binary threshold segmentation
        _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

        # Show both original and mask
        cv2.imshow("Original", frame)
        cv2.imshow("Mask", mask)

        # Quit when user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_segmentation()
