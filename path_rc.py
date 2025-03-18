from pymavlink import mavutil
import time

# Create the connection
master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
master.wait_heartbeat()

def set_rc_channel_pwm(channel_id, pwm=1500):
    """ Set RC channel PWM value
    Args:
        channel_id (int): Channel ID (1-11)
        pwm (int, optional): PWM value (1100-1900)
    """
    if channel_id < 1 or channel_id > 11:
        print("Channel does not exist.")
        return

    rc_channel_values = [65535 for _ in range(18)]
    rc_channel_values[channel_id - 1] = pwm
    master.mav.rc_channels_override_send(
        master.target_system,
        master.target_component,
        *rc_channel_values
    )

# Zig-zag movement loop
for i in range(5):  # Repeat 5 times
    # Move forward and strafe right
    set_rc_channel_pwm(5, 1600)  # Forward
    set_rc_channel_pwm(6, 1600)  # Strafe right
    time.sleep(2)

    # Small right turn
    set_rc_channel_pwm(4, 1600)  # Yaw right
    time.sleep(1)

    # Move forward and strafe left
    set_rc_channel_pwm(5, 1600)  # Forward
    set_rc_channel_pwm(6, 1400)  # Strafe left
    time.sleep(2)

    # Small left turn
    set_rc_channel_pwm(4, 1400)  # Yaw left
    time.sleep(1)

# Stop movement
set_rc_channel_pwm(5, 1500)  # Stop forward
set_rc_channel_pwm(6, 1500)  # Stop lateral
set_rc_channel_pwm(4, 1500)  # Stop yaw

print("Zig-zag maneuver complete.")
