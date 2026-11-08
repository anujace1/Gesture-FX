GestureFX is a Python computer-vision project that uses a webcam and hand-landmark detection to create an interactive visual-effects window. By positioning both hands in front of the camera, you can define a four-point “portal” area where a visual filter is applied. A closing hand movement switches to the next filter.

The project explores real-time hand tracking, gesture interaction, image processing, and modular visual-effect design.
Features
- Real-time hand detection: Detects up to two hands from the webcam feed using MediaPipe.
- Hand-controlled effect area: Uses the index-finger tips and thumbs to define a four-corner polygon.
- Gesture-based filter switching: Moving the hands closer together triggers a switch to the next visual effect.
- Multiple visual effects: Includes halftone/dot patterns, colour-threshold effects, channel shifting, colour maps, sepia with vignette, soft blur, and grid overlays.
- Modular implementation: Separates the main webcam loop, geometry/gesture logic, and filter functions into different Python files.

Tech Stack
- Python — application logic
- OpenCV — webcam capture, image processing, drawing, and display
- MediaPipe — hand landmark detection
- NumPy — image and geometry calculations

Project Structure
filter-project/
├── main.py                 # Webcam loop, hand detection, and interaction
├── filters.py              # Collection of visual filter functions
├── geometry.py             # Portal geometry, polygon masking, and gesture logic
└── hand_landmarker.task    # MediaPipe hand landmark model

How It Works
1. The application opens the computer's default webcam and mirrors the camera frame.
2. MediaPipe detects up to two hands and returns their landmark positions.
3. The program uses the index-finger tips and thumb tips from both hands to calculate four points.
4. Those points form a quadrilateral that acts as the effect area.
5. The selected filter is applied only inside that polygon; the rest of the camera frame remains unchanged.
6. When the distance between the hands crosses the configured closing threshold, the application advances to the next filter.

What I Learned
This project provided practical experience with:
- Real-time computer vision and webcam processing
- Hand landmark detection with MediaPipe
- Mapping normalized landmark coordinates to image coordinates
- Polygon masks and region-of-interest image processing
- Gesture-triggered interaction
- Building modular Python applications

Author
Anuj Gupta

GitHub: @anujace1
