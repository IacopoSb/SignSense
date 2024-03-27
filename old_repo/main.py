# This file load first model and runs it in background. When the button is pressed, it kills the recognition script and starts the second model
import RPi.GPIO as GPIO
import subprocess
import time
import os
import signal

# Define GPIO pin connected to the button
BUTTON_PIN = 17

# Define the commands to be executed when the button is pressed
COMMAND_SCRIPT1 = "python3 PATH/TO/SCRIPT1"
COMMAND_SCRIPT2 = "python3 PATH/TO/SCRIPT2"

# Variable to keep track of the background process
background_process = None

# Variable to keep track of the current script command
current_command = COMMAND_SCRIPT1

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to start the background process
def start_process(command):
    global background_process
    background_process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)

# Function to stop the background process
def stop_process():
    global background_process
    if background_process:
        # Send a SIGINT signal to terminate immediately the process group
        os.killpg(os.getpgid(background_process.pid), signal.SIGINT)
        background_process = None

# Variable to keep track of button state (pressed or not)
button_state = GPIO.LOW

# Start first script
start_process(current_command)

try:
    while True:
        # Check if the button state has changed
        if GPIO.input(BUTTON_PIN) != button_state:
            # Update the button state
            button_state = GPIO.input(BUTTON_PIN)

            # Button is pressed (GPIO.HIGH)
            if button_state == GPIO.HIGH:
                # Toggle between the two scripts on each button press
                if current_command == COMMAND_SCRIPT1:
                    current_command = COMMAND_SCRIPT2
                else:
                    current_command = COMMAND_SCRIPT1

                # If the process is running, stop it
                stop_process()

                # Start the new process based on the current command
                start_process(current_command)

        # Add a small delay to debounce the button
        time.sleep(0.1)

except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    GPIO.cleanup()
