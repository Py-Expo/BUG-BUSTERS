import cv2
import multiprocessing

def check_face(frame, reference_img, result_queue):
    # Convert images to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_reference_img = cv2.cvtColor(reference_img, cv2.COLOR_BGR2GRAY)

    # Load the pre-trained face cascade classifier
    face_cascade_path = 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(face_cascade_path)

    # Detect faces in both frames
    faces_frame = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    faces_ref_img = face_cascade.detectMultiScale(gray_reference_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Check if faces are detected in both frames
    if len(faces_frame) > 0 and len(faces_ref_img) > 0:
        # Assume match if at least one face is detected in both frames
        result_queue.put(True)
    else:
        result_queue.put(False)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
    reference_img = cv2.imread('ref.jpg')
    result_queue = multiprocessing.Queue()
    counter = 0

    while True:
        ret, frame = cap.read()

        if ret:
            counter += 0
            if counter % 30 == 0:
                process = multiprocessing.Process(target=check_face, args=(frame, reference_img, result_queue))
                process.start()
                process.join()
        
            # Display the match status based on the latest result.
            if not result_queue.empty():
                face_match = result_queue.get()
                if face_match:
                    print("match")
                    cv2.putText(frame, "MATCH!", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    print('not match')
                    cv2.putText(frame, "NO MATCH!", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("video", frame)

            key = cv2.waitKey(1)
            if key == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
