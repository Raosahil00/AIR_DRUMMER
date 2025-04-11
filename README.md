
# 🥁 Air Drummer

**Air Drummer** is a virtual drumming experience powered by computer vision and audio. With just your hands and a webcam, you can play a full drum kit by striking invisible zones in the air — no drumsticks or pads needed!

## 📸 What It Does

- Tracks your hand movements using **MediaPipe** + **cvzone**  
- Detects **drum hits** based on hand **speed** and **position**
- Plays **different drum sounds** (A–H) mapped to on-screen zones
- Provides visual feedback in real-time with OpenCV

## 🧠 How It Works

- Your webcam captures hand motion  
- Each drum zone is a circular area on screen (like pads)
- If your hand enters a zone *with enough velocity*, a sound is triggered  
- Drum sounds (e.g., `A.wav`, `B.wav`) are loaded from a local `sounds/` folder  

## 🕹️ Controls

- Use **any part of your hand** (tip of the middle finger is tracked)  
- Drum zones are spread across 3 rows (top, middle, bottom)
- The **faster** you move into a zone, the **louder** the sound

## 🎵 Sound Files

Place your custom drum `.wav` files (named `A.wav` to `H.wav`) inside a `sounds/` folder in the same directory as the script:

```
your_project/
├── DRUMMER.py
└── sounds/
    ├── A.wav
    ├── B.wav
    └── ...
```

## 🚀 Installation

```bash
pip install opencv-python mediapipe pygame cvzone numpy
```

## ▶️ How to Run

```bash
python DRUMMER.py
```

> Press `q` to quit the app.

## 🧹 Cleanup

The app automatically releases all resources when you exit:
- Closes webcam
- Shuts down Pygame audio engine
- Destroys OpenCV window

## 💡 Features You Could Add

- Multi-hand coordination (left for snares, right for cymbals?)  
- Different sound sets (rock, jazz, trap, etc.)  
- Customizable drum layout and sensitivity  

---
