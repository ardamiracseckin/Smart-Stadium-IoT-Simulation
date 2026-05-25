"""
Smart Stadium IoT Project - Smart Lighting Controller
Note: This script is designed to run within the Cisco Packet Tracer SBC/MCU environment.
It uses environmental sensors (Light/Motion) for automation and allows manual IoT override.
"""

from gpio import *
from time import *
from ioeclient import *

manual_override = False
is_light_on = False

def turn_on_lights():
    """Activates all stadium LEDs and updates the IoT app state."""
    global is_light_on
    # Triggering multiple LED pins
    for pin in [1, 3, 4, 5]:
        digitalWrite(pin, 1)
        analogWrite(pin, 1023)
    
    if not is_light_on:
        is_light_on = True
        IoEClient.reportStates([manual_override, is_light_on])

def turn_off_lights():
    """Deactivates all stadium LEDs and updates the IoT app state."""
    global is_light_on
    for pin in [1, 3, 4, 5]:
        digitalWrite(pin, 0)
        analogWrite(pin, 0)
    
    if is_light_on:
        is_light_on = False
        IoEClient.reportStates([manual_override, is_light_on])

def onInputReceive(stateName, value):
    """Handles manual override commands from the smartphone."""
    global manual_override
    
    if stateName == "Manual Override":
        if str(value).lower() in ["true", "1"]:
            manual_override = True
            print("SMARTPHONE CMD: Lights turned ON manually!")
        else:
            manual_override = False
            print("SMARTPHONE CMD: Switched to Automatic Sensor Mode.")

def main():
    global manual_override
    
    # Pin Configurations
    pinMode(0, IN)  # Light Sensor 
    pinMode(2, IN)  # Motion Sensor 
    for pin in [1, 3, 4, 5]:
        pinMode(pin, OUT) # Stadium LEDs
        
    print("Smart Lighting System initialized...")

    # IoT Interface Setup
    IoEClient.setup({
        "type": "Lighting_System",
        "states": [
            {"name": "Manual Override", "type": "bool", "controllable": True},
            {"name": "Light Status", "type": "bool", "controllable": False} # Read-only status
        ]
    })

    IoEClient.onStateSet(onInputReceive)
    IoEClient.reportStates([False, False])

    while True:
        light_level = analogRead(0)
        motion_detected = analogRead(2)

        # STATE 1: Manual Override is active
        if manual_override:
            turn_on_lights()
            
        # STATE 2: Automatic Sensor Mode
        else:
            # If it's night (0) AND there is movement in the stadium
            if light_level == 0 and motion_detected >= 1000:
                print("Nighttime and motion detected. Lights ON!")
                turn_on_lights()
                
                # Non-blocking delay: Keeps lights on for 6 seconds (60 * 100ms)
                # Allows the system to immediately respond if manual override is triggered
                for _ in range(60):
                    if manual_override: 
                        break
                    delay(100)
            else:
                turn_off_lights()

        delay(100)

if __name__ == "__main__":
    main()