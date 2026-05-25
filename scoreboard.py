"""
Smart Stadium IoT Project - Scoreboard Controller
Note: This script is designed to run within the Cisco Packet Tracer SBC/MCU environment.
It reads goal signals, updates the LCD display, and syncs with the IoT Smartphone App.
"""

from gpio import *
from time import *
from ioeclient import * skor_home = 0
skor_away = 0

def update_lcd():
    """Updates the physical LCD screen with the current score."""
    yeni_skor = "Home: " + str(skor_home) + " - Away: " + str(skor_away)
    customWrite(2, yeni_skor)

def onInputReceive(stateName, value):
    """Handles incoming commands from the IoT Smartphone Application."""
    global skor_home, skor_away
    
    if str(value).lower() in ["true", "1"]:
        if stateName == "Reset Score":
            skor_home = 0
            skor_away = 0
            print("SMARTPHONE CMD: Score Reset!")
            update_lcd()
            
        elif stateName == "Home +1":
            skor_home += 1
            print("SMARTPHONE CMD: Home +1")
            update_lcd()
            
        elif stateName == "Away +1":
            skor_away += 1
            print("SMARTPHONE CMD: Away +1")
            update_lcd()

def main():
    global skor_home, skor_away
    
    # Pin Configurations
    pinMode(0, IN)  # Goal signal from Goal 1
    pinMode(1, IN)  # Goal signal from Goal 2
    pinMode(2, OUT) # LCD Display output
    
    update_lcd()
    print("Scoreboard initialized...")
    
    # IoT Interface Setup for the Smartphone App
    IoEClient.setup({
        "type": "Scoreboard",
        "states": [
            {"name": "Reset Score", "type": "bool", "controllable": True},
            {"name": "Home +1", "type": "bool", "controllable": True},
            {"name": "Away +1", "type": "bool", "controllable": True}
        ]
    })
    
    IoEClient.onStateSet(onInputReceive)
    
    while True:
        kale1 = analogRead(0)
        kale2 = analogRead(1)
        
        # If Goal 1 sensor is triggered
        if kale1 > 500:
            skor_away += 1
            update_lcd()
            print("AWAY TEAM SCORED! Score: Home: " + str(skor_home) + " - Away: " + str(skor_away))
            delay(3000)
            
        # If Goal 2 sensor is triggered
        if kale2 > 500:
            skor_home += 1
            update_lcd()
            print("HOME TEAM SCORED! Score: Home: " + str(skor_home) + " - Away: " + str(skor_away))
            delay(3000)
            
        # Reset phone buttons to 'False' to prevent them from getting stuck
        IoEClient.reportStates([False, False, False])
        delay(100)

if __name__ == "__main__":
    main()