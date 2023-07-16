# pico-glove-rev1
This is the code that you run on the Raspberry Pi Pico. I have included the CircuitPython libraries you have to add to the Pico to read measurements from the MPU6050 and emulate a Keyboard HID. 

"boot.py" enables HID on boot. "code.py" contains the code that controls the glove. Every time the pico starts, "code.py" is run.
Accompanying blog post: https://sukkendi.com/glove-rev-1/
