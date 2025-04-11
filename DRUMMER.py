import cv2
import mediapipe as mp
import pygame
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
import os

class AirDrummer:
    def __init__(self):
        # Initialize video capture
        self.cap = cv2.VideoCapture(0)
        
        # Initialize hand detector
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)
        
        # Initialize Pygame for audio
        pygame.init()
        pygame.mixer.init()
        
        # Get the current directory and sounds folder path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sounds_dir = os.path.join(current_dir, 'sounds')
        
        # Add this debug code at the start of your __init__ function
        print("=== Debug Information ===")
        print(f"Current directory: {os.getcwd()}")
        print(f"Sounds directory: {sounds_dir}")
        try:
            files = os.listdir(sounds_dir)
            print(f"Files found in sounds directory: {files}")
            for file in files:
                print(f"Found file: {file}")
        except Exception as e:
            print(f"Error listing files: {e}")
        print("=====================")
        
        # Load drum sounds with simpler names
        try:
            self.drums = {
                'A': pygame.mixer.Sound(os.path.join(sounds_dir, 'A.wav')),
                'B': pygame.mixer.Sound(os.path.join(sounds_dir, 'B.wav')),
                'C': pygame.mixer.Sound(os.path.join(sounds_dir, 'C.wav')),
                'D': pygame.mixer.Sound(os.path.join(sounds_dir, 'D.wav')),
                'E': pygame.mixer.Sound(os.path.join(sounds_dir, 'E.wav')),
                'F': pygame.mixer.Sound(os.path.join(sounds_dir, 'F.wav')),
                'G': pygame.mixer.Sound(os.path.join(sounds_dir, 'G.wav')),
                'H': pygame.mixer.Sound(os.path.join(sounds_dir, 'H.wav'))
            }
            print("Successfully loaded all sound files!")
        except Exception as e:
            print(f"Error loading sound files: {e}")
            print(f"Looking in directory: {sounds_dir}")
            print("Please ensure all .wav files are in the sounds folder")
            raise
        
        # Define drum zones with better spacing
        self.drum_zones = {
            # Top row (more spread out)
            'A': {'pos': (100, 150), 'radius': 60, 'color': (255, 0, 0)},      # Red - Top Left
            'B': {'pos': (300, 150), 'radius': 60, 'color': (0, 255, 0)},      # Green - Top Middle
            'C': {'pos': (500, 150), 'radius': 60, 'color': (0, 0, 255)},      # Blue - Top Right
            
            # Middle row
            'D': {'pos': (200, 300), 'radius': 60, 'color': (255, 255, 0)},    # Yellow - Middle Left
            'E': {'pos': (400, 300), 'radius': 60, 'color': (255, 0, 255)},    # Magenta - Middle Right
            
            # Bottom row
            'F': {'pos': (100, 350), 'radius': 60, 'color': (0, 255, 255)},    # Cyan - Bottom Left
            'G': {'pos': (300, 350), 'radius': 60, 'color': (128, 128, 255)},  # Light Blue - Bottom Middle
            'H': {'pos': (500, 350), 'radius': 60, 'color': (255, 128, 0)}     # Orange - Bottom Right
        }
        
        # Cooldown timers for each drum
        self.last_hit_time = {drum: 0 for drum in self.drums.keys()}
        self.cooldown = 0.1  # 100ms cooldown
        
        # Velocity tracking
        self.prev_hand_positions = {}
        self.velocity_threshold = 50

    def calculate_velocity(self, hand_id, current_pos):
        """Calculate hand velocity"""
        if hand_id not in self.prev_hand_positions:
            self.prev_hand_positions[hand_id] = current_pos
            return 0
        
        prev_pos = self.prev_hand_positions[hand_id]
        velocity = np.sqrt((current_pos[0] - prev_pos[0])**2 + 
                         (current_pos[1] - prev_pos[1])**2)
        
        self.prev_hand_positions[hand_id] = current_pos
        return velocity

    def check_drum_hit(self, hand_pos, velocity):
        """Check if a drum is hit and play sound"""
        current_time = time.time()
        
        for drum_name, zone in self.drum_zones.items():
            distance = np.sqrt((hand_pos[0] - zone['pos'][0])**2 + 
                             (hand_pos[1] - zone['pos'][1])**2)
            
            if (distance < zone['radius'] and 
                velocity > self.velocity_threshold and 
                current_time - self.last_hit_time[drum_name] > self.cooldown):
                
                # Play sound with velocity-based volume
                volume = min(1.0, velocity / 200.0)
                self.drums[drum_name].set_volume(volume)
                self.drums[drum_name].play()
                self.last_hit_time[drum_name] = current_time
                return drum_name
        
        return None

    def draw_drums(self, img):
        """Draw drum zones on the image"""
        for drum_name, zone in self.drum_zones.items():
            cv2.circle(img, zone['pos'], zone['radius'], zone['color'], 2)
            # Draw the letter in a larger, more visible font
            cv2.putText(img, drum_name, 
                       (zone['pos'][0] - 15, zone['pos'][1] + 15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, zone['color'], 3)

    def run(self):
        try:
            while True:
                success, img = self.cap.read()
                if not success:
                    break
                
                # Flip image horizontally for more intuitive interaction
                img = cv2.flip(img, 1)
                
                # Find hands
                hands, img = self.detector.findHands(img)
                
                # Draw drum zones
                self.draw_drums(img)
                
                if hands:
                    for i, hand in enumerate(hands):
                        # Get hand position (using middle finger tip)
                        hand_landmarks = hand['lmList']
                        hand_pos = (hand_landmarks[12][0], hand_landmarks[12][1])
                        
                        # Calculate velocity
                        velocity = self.calculate_velocity(i, hand_pos)
                        
                        # Check for drum hits
                        hit_drum = self.check_drum_hit(hand_pos, velocity)
                        
                        if hit_drum:
                            # Visual feedback for hit
                            cv2.circle(img, self.drum_zones[hit_drum]['pos'], 
                                     self.drum_zones[hit_drum]['radius'], 
                                     (255, 255, 255), -1)
                        
                        # Draw hand position and velocity
                        cv2.circle(img, hand_pos, 10, (0, 255, 0), -1)
                        cv2.putText(img, f"Vel: {int(velocity)}", 
                                  (hand_pos[0] - 20, hand_pos[1] - 20),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # Display
                cv2.imshow("Air Drummer", img)
                
                # Exit on 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup resources"""
        pygame.mixer.quit()
        pygame.quit()
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    drummer = AirDrummer()
    drummer.run()