from inputs import get_gamepad
import time

events = get_gamepad()
for event in events:
	print(event.code)
