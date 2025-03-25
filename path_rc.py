"""
Example of how to use RC_CHANNEL_OVERRIDE messages to force input channels
in Ardupilot. These effectively replace the input channels (from joystick
or radio), NOT the output channels going to thrusters and servos.
"""

# Import mavutil
from pymavlink import mavutil
import time

# Create the connection
master = mavutil.mavlink_connection('udpin:192.168.2.1:14550')
# Wait a heartbeat before sending commands
master.wait_heartbeat()

# Armement du BlueROV2
master.arducopter_arm()
#master.motors_armed_wait()

# Create a function to send RC values
# More information about Joystick channels
# here: https://www.ardusub.com/operators-manual/rc-input-and-output.html#rc-inputs

GUIDED_MODE = 'STABILIZE'
while not master.wait_heartbeat().custom_mode == master.mode_mapping()[GUIDED_MODE]:
    master.set_mode(GUIDED_MODE)


def set_rc_channel_pwm(channel_id, pwm=1500):
    """ Set RC channel pwm value
    Args:
        channel_id (TYPE): Channel ID
        pwm (int, optional): Channel pwm value 1100-1900
    """
    if channel_id < 1 or channel_id > 18:
        print("Channel does not exist.")
        return

    # Mavlink 2 supports up to 18 channels:
    # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
    rc_channel_values = [65535 for _ in range(18)]
    rc_channel_values[channel_id - 1] = pwm
    master.mav.rc_channels_override_send(
        master.target_system,                # target_system
        master.target_component,             # target_component
        *rc_channel_values)                  # RC channel list, in microseconds.

def brake():
    """ Active braking to reduce drift """
    set_rc_channel_pwm(5, 1400)  # Reverse briefly
    time.sleep(0.5)
    set_rc_channel_pwm(5, 1500)  # Stop


def turn_right():
    """ Turn 90° to the right using roll or directional thrusters """
    set_rc_channel_pwm(4, 1630)  # Rotation droite
    time.sleep(2)  # Ajuster pour un vrai 90°
    set_rc_channel_pwm(4, 1500)  # Stop rotation


def turn_left():
    """ Turn 90° to the left using roll or directional thrusters """
    set_rc_channel_pwm(4, 1370)  # Rotation gauche
    time.sleep(2)  # Ajuster pour un vrai 90°
    set_rc_channel_pwm(4, 1500)  # Stop rotation


set_rc_channel_pwm(5, 1580)  
time.sleep(2)  
brake()

# Boustrophédon movement loop
for _ in range(3):  # Nombre de lignes
    # Avancer tout droit
    set_rc_channel_pwm(5, 1580)  
    time.sleep(2)  
    brake()

    # Tourner 90° à droite
    turn_right()

    # Avancer un peu
    set_rc_channel_pwm(5, 1580)
    time.sleep(1.5)
    brake()

    # Tourner encore 90° à droite
    turn_right()

    # Avancer tout droit
    set_rc_channel_pwm(5, 1580)
    time.sleep(2)
    brake()

    # Tourner 90° à gauche
    turn_left()

    # Avancer un peu
    set_rc_channel_pwm(5, 1580)
    time.sleep(1.5)
    brake()

    # Tourner encore 90° à gauche
    turn_left()

# Arrêt final
set_rc_channel_pwm(5, 1500)

master.arducopter_disarm()
master.motors_disarmed_wait()
