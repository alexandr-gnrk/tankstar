import time

import keyboard

from model import Model


model = Model((8, 8))
while True:
    if keyboard.is_pressed('up'):
        model.move(model.player)
    elif keyboard.is_pressed('down'):
        model.move(model.player, backward=True)
    elif keyboard.is_pressed('right'):
        model.turn(model.player)
    elif keyboard.is_pressed('left'):
        model.turn(model.player, ACW=True)
    elif keyboard.is_pressed('q'):
        break
    model.dump()
    time.sleep(1/10)
