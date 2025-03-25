import time
from pymavlink import mavutil

# Connect to the BlueROV2 (adjust the connection string as needed)
mav = mavutil.mavlink_connection('udp:192.168.2.1:14550')

# Wait for the heartbeat signal to confirm connection
mav.wait_heartbeat()
print("Heartbeat received. Connection established.")

def set_light_signal(signal_value):
    """
    Set the PWM signal for the Lumen light.
    :param signal_value: Integer from 1100 (off) to 1900 (full brightness)
    """ 
    # Send command to control the light (Servo output on channel 9)
    mav.mav.command_long_send(
        mav.target_system, mav.target_component,  # Target system and component
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,    # Command to set servo output
        0,  # Confirmation
        9,  # Servo channel (adjust if necessary)
        signal_value,  # PWM signal value
        0, 0, 0, 0, 0  # Unused parameters
    )
    print(f"Lumen light signal set to {signal_value}")

# Turn the light off initially
set_light_signal(1100) #1100

time.sleep(2)

# Set light brightness to a specific signal value
set_light_signal(1700) #1100

# Keep the connection alive for a few seconds
time.sleep(5)


# Turn the light off initially
set_light_signal(1100) #1100

time.sleep(2)
