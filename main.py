from graphics import *
from Logic import *
import GraphicsUnit

#         pyglet.clock.schedule_interval(self.update, 1.0/24.0)
#
#     def on_draw(self):
#         self.clear()
#         self.program.draw()
#
#     def update(self, dt):
#         self.program.run_rules()
def main():
    window_width = 500
    window_height = 500
    cell_size = 10
    percent_fill = 0.4
    initial_append_vector = [0.4, [1, 0.4, 0.1]]

    # Initialize Window
    window = GraphWin("PY-CA", window_width, window_height)
    # Initialize automat with propability vector
    automat = CellAutomata(window_width, window_height, cell_size, initial_append_vector)

    window.getMouse()
    while True:
        automat.run_rules()

main()
