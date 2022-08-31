import time
from rover import *


def follow_line_until(speed, condition, timeout=10000):
    count = 0
    last_time = time.ticks_ms()
  
    standard_speed = 25
  
    while time.ticks_ms() - last_time < timeout:
        if condition():
            count = count + 1
            if count == 3:
                break

        if speed >= 0:
            if rover.read_line_sensors() == (1, 0, 0, 0):
                rover.turn_left(70 if speed > 50 else 50)
            elif rover.read_line_sensors() == (1, 1, 0, 0):
                rover.turn_left(speed)
            elif rover.read_line_sensors() == (0, 0, 0, 1):
                rover.turn_right(50)
            elif rover.read_line_sensors() == (0, 0, 1, 1):
                rover.turn_right(70 if speed > 50 else 50)
            elif rover.read_line_sensors() == (0, 0, 0, 0):
                if count == 0:
                    rover.backward(speed)
            else:
                rover.forward(speed)
        else:
            if rover.read_line_sensors() == (0, 0, 1, 0):
                rover.set_wheel_speed(0, speed)
            elif rover.read_line_sensors() == (0, 1, 0, 0):
                rover.set_wheel_speed(speed, 0)
            else:
                rover.backward(abs(speed))
    
        time.sleep_ms(10)

    rover.stop()

def turn_until_line_detected(m1_speed, m2_speed, timeout=5000):
    turn_left = 1
    count = 0
    sensor_index = 2
    if m1_speed > m2_speed:
        turn_left = 0
        sensor_index = 3    
  
    last_line_status = rover.read_line_sensors(sensor_index)
  
    rover.set_wheel_speed(m1_speed, m2_speed)
  
    last_time = time.ticks_ms()
  
    while time.ticks_ms() - last_time < timeout:
    
        current_line_status = rover.read_line_sensors(sensor_index)

        if current_line_status == 1: # black line detected
	  # ignore case when robot is still on black line since started turning
            if last_line_status == 1 or time.ticks_ms() - last_time < 500:
                continue
            else:
        # only considered as black line detected after 3 times reading
                if count > 3:
                    rover.stop()
                    break
                else:
                    count = count + 1
        else: # meet white background
            last_line_status = 0
  
        time.sleep_ms(10)

    rover.stop()

def follow_line_delay(speed, timeout=10000):
  count = 0
  last_time = time.ticks_ms()
  
  standard_speed = 25
  
  while time.ticks_ms() - last_time < timeout:
    if speed >= 0:
      if rover.read_line_sensors() == (1, 0, 0, 0):
        rover.turn_left(70 if speed > 50 else 50)
      elif rover.read_line_sensors() == (1, 1, 0, 0):
        rover.turn_left(speed)
      elif rover.read_line_sensors() == (0, 0, 0, 1):
        rover.turn_right(50)
      elif rover.read_line_sensors() == (0, 0, 1, 1):
        rover.turn_right(70 if speed > 50 else 50)
      elif rover.read_line_sensors() == (0, 0, 0, 0):
        if count == 0:
          rover.backward(speed)
      else:
        rover.forward(speed)
    else:
      if rover.read_line_sensors() == (0, 0, 1, 0):
        rover.set_wheel_speed(0, speed)
      elif rover.read_line_sensors() == (0, 1, 0, 0):
        rover.set_wheel_speed(speed, 0)
      else:
        rover.backward(abs(speed))
    
    time.sleep_ms(10)

  rover.stop()
