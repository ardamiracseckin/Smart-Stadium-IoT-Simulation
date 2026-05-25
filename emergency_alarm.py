"""
Smart Stadium IoT Project - Emergency Alarm System
Note: This script is designed to run within the Cisco Packet Tracer SBC/MCU environment.
It synchronizes a physical emergency button with a digital IoT toggle switch.
"""

from gpio import *
from time import *
from ioeclient import *

alarm_active = False

def trigger_alarm(new_state):
    """Toggles the physical alarm siren and updates the IoT app."""
    global alarm_active
    alarm_active = new_state
    
    if alarm_active:
        print(">>> ALARM ACTIVATED! <<<")
        digitalWrite(1, 1)
        customWrite(1, 1)
        analogWrite(1, 1023)
    else:
        print(">>> ALARM DEACTIVATED! <<<")
        digitalWrite(1, 0)
        customWrite(1, 0)
        analogWrite(1, 0)
        
    # Sync the smartphone UI with the current physical state
    IoEClient.reportStates([alarm_active])

def onInputReceive(stateName, value):
    """Handles alarm toggle commands from the smartphone."""
    if stateName == "Alarm Control":
        if str(value).lower() in ["true", "1"]:
            trigger_alarm(True)
        else:
            trigger_alarm(False)

def main():
    global alarm_active
    
    # Pin Configurations
    pinMode(0, IN)   # Physical Button
    pinMode(1, OUT)  # Siren / Alarm Device

    print("System Ready. Listening for button and smartphone inputs...")

    # IoT Interface Setup
    IoEClient.setup({
        "type": "Emergency_System",
        "states": [
            {"name": "Alarm Control", "type": "bool", "controllable": True}
        ]
    })
    
    IoEClient.onStateSet(onInputReceive)
    IoEClient.reportStates([False])

    while True:
        button_value = analogRead(0) 
        
        # If the physical button is pressed
        if button_value > 500:
            # Toggle the current state
            trigger_alarm(not alarm_active)
            
            # Debounce delay to prevent multiple triggers from a single press
            delay(1000) 
            
        delay(10) 

if __name__ == "__main__":
    main()