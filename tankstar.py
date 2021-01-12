import time

import keyboard

from model import Model


model = Model()
while True:
    if keyboard.is_pressed('up'):
        model.add_move_action(model.player, backward=False)
    elif keyboard.is_pressed('down'):
        model.add_move_action(model.player, backward=True)
    elif keyboard.is_pressed('right'):
        model.add_turn_action(model.player, ACW=False)
    elif keyboard.is_pressed('left'):
        model.add_turn_action(model.player, ACW=True)
    elif keyboard.is_pressed('space'):
        model.add_shoot_action(model.player)
    elif keyboard.is_pressed('q'):
        break

    model.update()
    model.dump()
    time.sleep(1/10)
