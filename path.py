import time
from pymavlink import mavutil

# Connect to the BlueROV2
mav = mavutil.mavlink_connection('udp:192.168.2.1:14550')
mav.wait_heartbeat()
print("ROV connected!")

def send_ned_velocity(vx, vy, vz, duration):
    """ Send velocity command in NED frame """
    msg = mav.mav.set_position_target_local_ned_encode(
        0, 0, 0, mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,  # Bitmask (only velocity)
        0, 0, 0, vx, vy, vz, 0, 0, 0, 0, 0)
    
    for _ in range(int(duration * 10)):  # Send command every 100ms
        mav.send(msg)
        time.sleep(0.1)

def zigzag_motion(length, width, speed, depth):
    """ Moves the ROV in a zigzag pattern """
    num_lanes = int(length / width)  # Number of zigzag turns
    direction = 1  # 1 = right, -1 = left

    # Set depth
    send_ned_velocity(0, 0, -0.5, 5)  # Move down
    time.sleep(2)

    for i in range(num_lanes):
        send_ned_velocity(speed, direction * speed, 0, width / speed)  # Move forward-right/left
        direction *= -1  # Change direction
        send_ned_velocity(speed, 0, 0, length / (2 * speed))  # Move forward

    # Stop ROV
    send_ned_velocity(0, 0, 0, 2)
    print("Zigzag path complete!")

# Parameters: pool size in meters
zigzag_motion(length=10, width=2, speed=0.5, depth=1)

