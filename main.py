import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from geometry import render_portal, portal_width, ClosingGestureDetector
from filters import FILTERS
THUMB_TIP, THUMB_MCP= 4, 2
INDEX_TIP, INDEX_MCP = 8, 5
MIDDLE_TIP, MIDDLE_MCP = 12, 9
RING_TIP, RING_MCP = 16, 13
PINKY_TIP, PINKY_MCP = 20, 17

def main():
    base_options = python.BaseOptions(
    model_asset_path="hand_landmarker.task"
)

    options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)

    hands = vision.HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError(
            "Could not open webcam."
        )

    filter_index = 0
    closing_detector = ClosingGestureDetector()

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,data=rgb)

        results = hands.detect(mp_image)

        left_hand = None
        right_hand = None

        if results.hand_landmarks and results.handedness:
            for hand_landmarks, handedness in zip(
        results.hand_landmarks,
        results.handedness
    ):
                raw_label = handedness[0].category_name

                label = "Right" if raw_label == "Left" else "Left"

                if label == "Left":
                    left_hand = hand_landmarks
                else:
                    right_hand = hand_landmarks

        if left_hand is not None and right_hand is not None:
            lm_left = left_hand
            lm_right = right_hand

            p1 = (lm_left[INDEX_TIP].x * w, lm_left[INDEX_TIP].y * h)
            p2 = (lm_left[THUMB_TIP].x * w, lm_left[THUMB_TIP].y * h)
            p3 = (lm_right[INDEX_TIP].x * w, lm_right[INDEX_TIP].y * h)
            p4 = (lm_right[THUMB_TIP].x * w, lm_right[THUMB_TIP].y * h)

            width = portal_width(p1, p2, p3, p4)

            if closing_detector.update(width, w):
                filter_index = (filter_index + 1) 
                if filter_index > len(FILTERS)-1:
                    filter_index=0

            frame = render_portal(frame, p1, p2, p3, p4, FILTERS[filter_index])

        cv2.imshow("Filters", frame)
        if cv2.waitKey(1) & 0xFF == ord("s"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()