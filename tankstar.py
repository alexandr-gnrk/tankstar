import argparse

from model import Model


parser = argparse.ArgumentParser(
    description="Simplified Battle City clone")
parser.add_argument(
    '-m', '--mode', 
    choices=('gui', 'console'),
    default='gui',
    dest='mode',
    help='game mode')

args = parser.parse_args()


model = Model()

if args.mode == 'console':
    import time
    import keyboard

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
        time.sleep(1/5)
else:
    from view import View
    
    View(model).start()



