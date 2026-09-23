# Software/Hardware - Digital Physical Therapist for Astronauts

## Software

### Name / central idea
Digital physical therapist for astronauts: the right exercise, even without gravity.

### System objective
Create health monitoring software for astronauts on space missions, focused on tracking physical exercise in microgravity and providing immediate feedback on posture and movement angles.

### General operation
The system uses video of the astronaut during exercise, estimates body pose, calculates joint angles, compares those angles with safe zones defined by a medical protocol, and provides immediate visual feedback.

Proposed workflow:

1. **Station cameras**
   - Capture video of the astronaut during exercise.

2. **Pose estimation**
   - Uses MediaPipe Pose.
   - Detects 33 skeletal key points in an image or video.

3. **Angle calculation**
   - Calculates angles between joints.
   - Examples mentioned:
     - shoulder-elbow-wrist;
     - hip-knee-ankle.

4. **Safe zones**
   - Compares the measured angles with limits defined by the medical protocol.
   - Each exercise has a safe range of motion.

5. **Immediate feedback**
   - Feedback may appear on a screen or in augmented reality glasses.
   - When a joint leaves the safe zone, the joint turns red.
   - The system indicates the required postural adjustment.

### Usage example
In the example presented, the system measures the knee angle during exercise.

- Before the exercise, the medical protocol defines the safe zone for the movement.
- During the exercise, the system measures the angle in each frame.
- When the movement leaves the safe zone, for example with a curved spine or overload on the patella, the joint is marked in red and the postural adjustment is indicated.

### Database
The project proposes using a PostgreSQL relational database to store session data.

Proposed data model for the prototype:

#### `astronaut` table
- `id`
- `name`

#### `exercise` table
- `id`
- `name`
- `joint`
- `min_angle`
- `max_angle`

#### `session` table
- `id`
- `astronaut_id`
- `exercise_id`
- `start`
- `end`

#### `measurement` table
- `id`
- `session_id`
- `timestamp`
- `angle`
- `inside_safe_zone`
- `confidence`

### Generated reports
Based on the measurements, the system should generate reports with:

- range of motion by joint and by session;
- time inside and outside the safe zone;
- deviations and asymmetry between the left and right sides;
- trend over the mission to estimate the effectiveness of atrophy mitigation;
- detection confidence for each measurement.

### Software validation plan
The document proposes validating the system by measuring:

| What to measure | Metric | How to measure |
|---|---|---|
| Angle accuracy | Angular error in degrees | Compare with a goniometer or manual frame annotation |
| Posture error detection | Sensitivity and false alerts | Intentionally record correct and incorrect movements |
| Feedback speed | Latency in milliseconds | Measure the time between the movement and the on-screen alert |
| Floating body | Angular error in multiple orientations | Repeat the test lying down, inverted, or with the image rotated |

### Technical risks and limitations
The document identifies the following risks and mitigation approaches:

| Risk | How to address it |
|---|---|
| MediaPipe Pose was trained under gravity; a floating or inverted body may fail | Test multiple orientations; adjust or retrain |
| Elastic bands and equipment may hide joints | Use the confidence score of each point; ignore weak measurements |
| A single camera limits angle depth | Evaluate more than one camera and validate against the reference |
| False alerts or missed alerts | Use zones defined by the medical protocol; the physician reviews the reports |
| Cameras record the astronaut, creating privacy and medical data concerns | Local processing, consent, and restricted access |

### Next technical steps for the prototype
The technical next steps mentioned are:

- create a prototype with MediaPipe Pose, a webcam, and angle calculation in one exercise, such as a squat or row;
- define example safe zones;
- implement visual feedback with the joint shown in red;
- store measurements in PostgreSQL;
- generate a simple report;
- measure the validation plan metrics;
- search for NASA open data that could be used in the prototype.

## Hardware

### Demo hardware
The document presents three hardware options to run the demonstration and record the project data.

### Option 1: TV box
Items:

- TV box: R$ 100.00
- P4 plug cable: R$ 26.00
- SanDisk Extreme 64 GB: R$ 214.99
- 2 mini desktop tripods: included in the total

Total with tripods: **R$ 385.97**

### Option 2: Raspberry Pi 5 (4 GB)
Items:

- Raspberry Pi 5 4 GB: R$ 1,294.00
- Official 27 W power supply: R$ 123.31
- Case with cooler: R$ 89.96
- Micro-HDMI cable: R$ 28.40
- SanDisk Extreme 64 GB: R$ 214.99
- 2 mini desktop tripods: included in the total

Total with tripods: **R$ 1,795.64**

### Option 3: Intel Celeron Mini PC
Items:

- Celeron Mini PC: R$ 600.00
- 2 mini desktop tripods: included in the total

Total with tripods: **R$ 644.98**

### Items common to the three options
- 2 mini desktop tripods: R$ 44.98, already included in the totals.
- Webcam: price still to be defined, outside the totals.

### Intended hardware use
The hardware will be used to:

- run the demonstration;
- capture or process the exercise video;
- execute the prototype;
- record the project data.
