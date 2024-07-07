from machine import UART, Pin
import time

uart2 = UART(2, baudrate=115200, tx=Pin(17), rx=Pin(16))
led = Pin(4, Pin.OUT)

def align_to_packet(uart):
    while True:
        if uart.any():
            byte = uart.read(1)
            if byte == b'\x59': 
                second_byte = uart.read(1)
                if second_byte == b'\x59':
                    return bytearray(b'\x59\x59')
        time.sleep(0.01)

def getLidarData(uart):
    temp = align_to_packet(uart)
    if temp:
        rest_of_data = uart.read(7)
        if rest_of_data and len(rest_of_data) == 7:
            temp += rest_of_data
            distance = temp[2] + temp[3] * 256
            strength = temp[4] + temp[5] * 256
            temperature = (temp[6] + temp[7] * 256) / 8 - 256
            #print(f"distance = {distance}cm, strength = {strength}, temperature = {temperature}℃")
            return distance

def debounce_sensor(trigger_distance=500, debounce_time=0.05):
    last_triggered = 0
    while True:
        distance = getLidarData(uart2)
        if distance is not None and distance < trigger_distance:
            current_time = time.time()
            if (current_time - last_triggered) > debounce_time:
                led.on()
                time.sleep(0.1)
                led.off()
                last_triggered = current_time
        time.sleep(0.01)

debounce_sensor()
