from graphics import *
from Logic import CellAutomata as Ca


class GraphicsUnit:

    @staticmethod
    def draw_grid(window, cells, cell_size):
        draw_on_screen = []
        for row in range(0, len(cells)):
            for col in range(0, len(cells[0])):
                draw_on_screen.append(GraphicsUnit.draw_cell(window, col * cell_size, row * cell_size, cell_size,
                                                             cells[row][col]))
        return draw_on_screen

    @staticmethod
    def undraw_elements(drawn_elements):
        for cell in drawn_elements:
            for element in cell:
                element.undraw()

    @staticmethod
    def draw_cell(window, x_up_left, y_up_left, cell_size, cell):
        p1 = Point(x_up_left, y_up_left)
        p2 = Point(x_up_left + cell_size, y_up_left + cell_size)

        cell_graphic = []
        if cell.state_person == 1:
            square = Rectangle(p1, p2)
            square.setFill(color_rgb(20, 20, 20))
            square.setOutline(color_rgb(255, 0, 144))
            square.setWidth(1)

            # Human specific Data
            txt1 = Text(Point((p1.getX() + cell_size / 5), (p1.getY() + cell_size / 5)), cell.state_wealth)
            txt2 = Text(Point((p1.getX() + 4 * cell_size / 5), (p1.getY() + cell_size / 5)), cell.state_culture)
            txt3 = Text(Point((p1.getX() + cell_size / 2), (p1.getY() + 3.5 * cell_size / 5)), cell.state_skin)

            # Wealth on uninhabited cells is cost
            txt_list = [txt1, txt2, txt3]
            for i in txt_list:
                i.setSize(int(round(cell_size / 3.25)))

            txt1.setTextColor("red")
            txt2.setTextColor("orange")
            txt3.setTextColor("white")

        else:
            square_empty = Rectangle(p1, p2)

            # Space cost instead of persons wealth
            txt1 = Text(Point((p1.getX() + cell_size / 2), (p1.getY() + cell_size / 2)), cell.state_wealth)
            txt1.setSize(int(round(cell_size / 2.5)))
            txt1.draw(window)

            cell_graphic.append(square_empty)
            cell_graphic.append(txt1)
            return cell_graphic

        square.draw(window)
        cell_graphic.append(square)
        for i in txt_list:
            i.draw(window)
            cell_graphic.append(i)

        return cell_graphic

    @staticmethod
    def highlight_clusters(ca, drawn_elements, cells, window, cell_size):

        two_dimension_drawn_elements = [drawn_elements[i:i+ca.grid_width] for i in range(0, len(drawn_elements), ca.grid_width)]

        for row in range(0, len(cells)):
            for col in range(0, len(cells[row])):
                surrounding_coords = Ca.select_cells(ca, row, col)

                wealth_indication = 0.0
                culture_indication = 0.0
                skin_indication = 0.0
                persons = 0

                for coord in surrounding_coords:
                    if cells[coord[0]][coord[1]].state_person == 1:
                        persons += 1

                for coord in surrounding_coords:
                    if cells[coord[0]][coord[1]].state_person == 1 and \
                            cells[coord[0]][coord[1]].state_wealth == cells[row][col].state_wealth:
                        wealth_indication += 1/persons
                    if cells[coord[0]][coord[1]].state_person == 1 and \
                            cells[coord[0]][coord[1]].state_culture == cells[row][col].state_culture:
                        culture_indication += 1/persons
                    if cells[coord[0]][coord[1]].state_person == 1 and \
                            cells[coord[0]][coord[1]].state_skin == cells[row][col].state_skin:
                        skin_indication += 1/persons

                    fill_percent = int(round((abs(1-((wealth_indication+culture_indication+skin_indication)/3)))*255))

                    if persons <= 2:
                        two_dimension_drawn_elements[row][col][0].setFill(color_rgb(220, 220, 220))
                    else:
                        two_dimension_drawn_elements[row][col][0].setFill(
                            color_rgb(fill_percent, fill_percent, fill_percent))

        GraphicsUnit.draw_cell(window, coord[1] * cell_size, coord[0] * cell_size, cell_size, cells[coord[0]][coord[1]])
