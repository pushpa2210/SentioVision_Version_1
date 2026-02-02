<h4>🧠 SentioVision – Human-Like Visual Perception System
📌 Overview
SentioVision is a real-time computer vision system designed to help machines perceive their surroundings in a human-like way.
Instead of only detecting objects, SentioVision:
•	understands what objects are
•	tracks who is the same object over time
•	extracts physical attributes
•	reasons about motion and behavior
•	handles unknown objects
•	produces explainable textual descriptions
•	stores a final perception snapshot
The goal is perception, not just detection.
🎯 Project Goals
•	Real-time object detection using a camera
•	Persistent object tracking with unique IDs
•	Attribute extraction:
o	size
o	color
o	distance (approximate)
•	Temporal behavior analysis:
o	moving / stationary
o	direction
•	Unknown object handling
•	Human-readable narration
•	Final snapshot logging (only last state)
🏗️ Project Architecture
Camera
  ↓
Detection (YOLO)
  ↓
Tracking (Object ID)
  ↓
Attributes (Color, Size, Distance)
  ↓
Behavior (Motion over time)
  ↓
Context & Narration
  ↓
Final Snapshot (Log)

Folder structure
SentioVision/
│
├── main.py                   # System controller
│
├── detector/                 # Object detection
│   └── yolo_detector.py
│
├── tracker/                  # Object ID tracking
│   └── object_tracker.py
│
├── attributes/               # Physical attributes
│   ├── color.py
│   └── size.py
│
├── behavior/                 # Temporal behavior
│   └── motion.py
│
├── context/                  # Scene-level understanding
│   └── scene_analysis.py
│
├── narration/                # Text description
│   └── describe.py
│
├── utils/                    # Math & visualization helpers
│   ├── geometry.py
│   └── visualization.py
│
├── models/
│   └── yolov8.pt             # Model weights (ignored in git)
│
├── logs/
│   └── session.log           # Final snapshot only
│
├── outputs/
│   ├── frames/
│   └── videos/
│
├── requirements.txt
├── README.md
└── .gitignore

🧩 Module Responsibilities (Simple Explanation)
main.py
•	Entry point of the system
•	Opens camera
•	Orchestrates all modules
•	Displays annotated output
•	Stores final snapshot when quitting
________________________________________
detector/
Purpose: What is this object?
•	Uses YOLO for detection
•	Outputs class, confidence, bounding box
________________________________________
tracker/
Purpose: Is this the same object as before?
•	Assigns unique IDs
•	Maintains identity across frames
________________________________________
attributes/
Purpose: What properties does this object have?
•	Color (dominant color)
•	Size (small / medium / large)
•	Distance (near / mid / far)
________________________________________
behavior/
Purpose: What is the object doing over time?
•	Motion detection
•	Direction inference
•	Stationary vs moving
________________________________________
context/
Purpose: What is happening in the scene overall?
•	Scene-level reasoning
•	(Extensible for crowd analysis, summaries)
________________________________________
narration/
Purpose: How can the system explain what it saw?
•	Converts perception into human-readable text
Example:
"Large blue person near and stationary"
________________________________________
utils/
Purpose: Supporting utilities
•	Geometry math
•	Visualization helpers
•	Keeps core logic clean
________________________________________
🖥️ Example Output (Terminal)
SENTIVISION – OBJECT PERCEPTION OUTPUT

ID          : 2
Object      : person
Motion      : moving up
Confidence  : 0.85
Color       : blue
Description : large blue person near and moving up
----------------------------------------
________________________________________
📸 Final Snapshot Logging
•	The system does NOT log every frame
•	Only the final perception state is stored
•	This avoids large logs and keeps output meaningful
Location:
logs/session.log
________________________________________
▶️ How to Run
1. Install dependencies
pip install -r requirements.txt
2. Run the system
python main.py
3. Quit
Press q to:
•	stop camera
•	store final snapshot
•	exit cleanly
