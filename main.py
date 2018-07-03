from graphics import *
from Logic import *
from GraphicsUnit import GraphicsUnit as Gu
import ctypes
import config


def main():
    window_width = config.window_width
    window_height = window_width
    cell_size = config.cell_size
    weights = config.weights

    # Initialize Windows
    window = GraphWin("PY-CA", window_width, window_height, autoflush=False)

    # Initialize automat with propability vector
    automat = CellAutomata(window_width, window_height, cell_size)

    ctypes.windll.user32.MessageBoxW(0,
            "Simulation startet mit " + str(config.max_period) + " Iterationan.\n"
            "Durch Klick auf die Simulationsfläche nach Ende des durchlaufs \n"
            "werden weitere " + str(config.max_period) +
            " Simulationen an den Simulationslauf angehängt \n"
            "Wenn ein Simulationslauf endet werden die \n"
            "erkannten Cluster farbig dargestellt.\n\n"
            "Die Parameter der Simulation können in config.py angepasst werden." , "PA-CA", 0)

    while True:
        period = 0
        max_period = config.max_period
        while period < max_period:
            drawn_elements = (Gu.draw_grid(window, automat.cells, cell_size))
            window.update()
            Gu.undraw_elements(drawn_elements)
            automat.run_rules(period, weights)
            period += 1
        drawn_elements = Gu.draw_grid(window, automat.cells, cell_size)  # Draw final state
        Gu.highlight_clusters(automat, drawn_elements, automat.cells, window, cell_size)
        window.getMouse()
        Gu.undraw_elements(drawn_elements)
main()
