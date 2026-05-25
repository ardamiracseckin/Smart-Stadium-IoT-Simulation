"""
Smart Stadium IoT Project - Goal Line Sensor (Tripwire)
Note: This script is designed to run within the Cisco Packet Tracer SBC/MCU environment.
It detects objects crossing the goal line and sends a high-voltage signal to the scoreboard.
"""

from gpio import *
from time import *

def main():
    # Pin Configurations
    pinMode(1, IN)   # Tripwire sensor input
    pinMode(2, OUT)  # RGB LED output for visual feedback
    pinMode(3, OUT)  # Signal output to the Scoreboard SBC

    while True:
        sensor_value = analogRead(1)
        
        # If the tripwire detects an object (e.g., the ball)
        if sensor_value >= 1000:
            # Send high voltage signal to scoreboard and turn on Red LED
            analogWrite(3, 1023) 
            analogWrite(2, 1023) 
            print("GOAL! Signal sent to the scoreboard.")
            
            # Keep the signal active for 3 seconds
            delay(3000)
            analogWrite(3, 0) # Cut the signal
        else:
            # Reset states if no detection
            analogWrite(2, 0)
            analogWrite(3, 0)
            
        delay(100)

if __name__ == "__main__":
    main()