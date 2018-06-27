import pyglet
import Logic


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(600, 600)
        self.program = Logic.Program(self.get_size()[0], self.get_size()[1], 10, 0.4)
        pyglet.clock.schedule_interval(self.update, 1.0/24.0)

    def on_draw(self):
        self.clear()
        self.program.draw()

    def update(self, dt):
        self.program.run_rules()

window = Window()
pyglet.app.run()
