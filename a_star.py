import pygame
from pygame.locals import *

class A_star:
    def __init__(self, size, win, win_size):
        self.grid_size = size
        self.grid = [[Node(r,c) for c in range(size)] for r in range(size)]
        self.win = win
        self.win_size = win_size

    def draw_grid(self):
        """ Draw the entire grid. """
        dif = self.win_size / self.grid_size
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                node = self.grid[i][j]
                x = node.row * dif
                y = node.col * dif
                pygame.draw.rect(self.win, (0, 0, 0), (x, y, dif, dif), 1)
                if node.wall:
                    pygame.draw.rect(self.win, (0, 0, 0), (x, y, dif, dif), 0)
                elif node.visited:
                    pygame.draw.rect(self.win, (255, 0, 0), (x, y, dif, dif), 0)
                if node.solution:
                    pygame.draw.rect(self.win, (0, 255, 0), (x, y, dif, dif), 0)

    def draw_node(self, node):
        """ Draw the specified node on the board. """
        dif = self.win_size / self.grid_size
        fnt = pygame.font.SysFont("comicsans", int(dif/3))
        x = node.row * dif
        y = node.col * dif
        if node.wall:
            pygame.draw.rect(self.win, (0, 0, 0), (x, y, dif, dif), 0)
        elif node.visited:
            pygame.draw.rect(self.win, (255, 0, 0), (x, y, dif, dif), 0)
        if node.solution:
            pygame.draw.rect(self.win, (0, 255, 0), (x, y, dif, dif), 0)
        if node.g != 0:
            # pygame.draw.rect(self.win, (255, 255, 255), (x, y, dif/2, dif/2), 0)
            im = fnt.render(str(node.f), 1, (0, 0, 0))
            self.win.blit(im, (x, y))
            im = fnt.render(str(node.g), 1, (0, 0, 0))
            self.win.blit(im, (x + dif/3, y))
            im = fnt.render(str(node.h), 1, (0, 0, 0))
            self.win.blit(im, (x + 2*(dif/3), y))
        pygame.draw.rect(self.win, (0, 0, 0), (x, y, dif, dif), 1)


    def get_square(self, pos):
        """ Returns the square indexes for the current cursor position. """
        if 0 <= pos[0] <= self.win_size and 0 <= pos[1] <= self.win_size:
            dif = self.win_size / self.grid_size
            row = pos[0] // dif
            col = pos[1] // dif
            return (int(row), int(col))
        return None

    def get_neighbours(self, node):
        """ Returns a list of neighbouring nodes. """
        result = []
        coords = [(0,1),(1,0),(1,1),(0,-1),(-1,0),(-1,-1),(1,-1),(-1,1)]
        for (x,y) in coords:
            row = node.row - x
            col = node.col - y
            if row in range(self.grid_size) and col in range(self.grid_size):
                if not self.grid[row][col].wall:
                    result.append(self.grid[row][col])
        return result

    def heuristic(self, start, finish):
        # return math.sqrt((start.row - finish.row)**2 + (start.col - finish.col)**2) # euclidean
        return abs(start.row - finish.row) + abs(start.col - finish.col) # manhattan

    def toggle_wall(self, row, col):
        self.grid[row][col].wall = True

    def search(self, start, finish):
        """ Search for a path between the start and finish node """
        # Initialize variables
        to_visit = []
        to_visit.append(start)
        visited = []
        max_iterations = (self.grid_size // 2) ** 10
        iteration = 0

        # Loop until all nodes have been visited
        while to_visit != []:
            iteration += 1
            # Select node from to visit list with lowest f value
            current_node = to_visit[0]
            current_index = 0
            for index, node in enumerate(to_visit):
                if node.f < current_node.f:
                    current_node = node
                    current_index = index
            print("current: ", current_node.row, current_node.col)
            # Draw the node as visited
            current_node.visited = True
            self.draw_node(current_node)
            pygame.display.update()
            pygame.time.delay(100)
            # Remove node from to visit list and add to visited list
            to_visit.pop(current_index)
            visited.append(current_node)

            # print("visited: ", [(c.row, c.col) for c in visited])
            print("to_visit: ", [(c.row, c.col) for c in to_visit])
            # Goal condition
            if current_node == finish:
                path = []
                current = current_node
                while current:
                    r = current.row
                    c = current.col
                    self.grid[r][c].solution = True
                    path.append(current)
                    current = current.parent
                print([(n.row, n.col) for n in path])
                break
            # iteration cap
            if iteration == max_iterations:
                print('taking too long')
                break
            # Get all node neighbours
            child_nodes = []
            for neighbour in self.get_neighbours(current_node):
                new_node = Node(neighbour.row, neighbour.col, current_node)
                child_nodes.append(new_node)
            print("Children: ", [(c.row, c.col) for c in child_nodes])
            # Evaluate child nodes
            for next_node in child_nodes:
                print("Checking: ", next_node.row, next_node.col)
                # Ignore if next node is in visited list
                if next_node in visited:
                    # print('already visited')
                    continue
                # Ignore walls
                # if self.grid[next_node.row][next_node.col].wall:
                #     print("wall ignored")
                #     continue
                # calculate values
                # print("not visited already")
                temp_g = current_node.g + 1
                if next_node not in visited:
                    if next_node in to_visit:
                        if next_node.g > temp_g:
                            next_node.g = temp_g
                            next_node.parent = current_node
                    else:
                        next_node.g = temp_g
                        visited.append(next_node)
                next_node.h = self.heuristic(next_node, finish)
                next_node.f = next_node.g + next_node.h
                # Ignore if g is not lower
                # if len([v for v in to_visit if next_node == v and next_node.g > v.g]) > 0:
                #     print("lower g score ignored")
                #     continue
                # Otherwise add next node to to_visit list
                if next_node not in to_visit:
                    to_visit.append(next_node)
                # if not next_node.parent:
                #     next_node.parent = current

            # input("Press Enter to continue...")

class Node:
    def __init__(self, row, col, parent=None):
        self.row = row
        self.col = col
        self.parent = parent
        self.wall = False
        self.visited = False
        self.solution = False
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

class App:
    """ The App class contains the PyGame instance. """
    def __init__(self, grid_size):
        self._running = True
        self._display_surf = None
        self.size = self.height, self.width = 500, 500
        self.a_star = None
        self.grid_size = grid_size
        self.toggle_walls = False

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        self.a_star = A_star(self.grid_size,self._display_surf,self.height)
        self._running = True

    def on_event(self, event):
        """ When closing window. """
        if event.type == pygame.QUIT:
            self._running = False

        """ When clicking. """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.toggle_walls = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.toggle_walls = False

        """ When keyboard button is pressed. """
        if event.type == pygame.KEYDOWN:
            # Spacebar
            if event.key == 32:
                s = self.grid_size - 1
                self.a_star.search(self.a_star.grid[0][0], self.a_star.grid[s][s])
            # Enter
            if event.key == 13:
                self.a_star = A_star(self.grid_size,self._display_surf,self.height)

    def on_loop(self):
        if self.toggle_walls:
            pos = pygame.mouse.get_pos()
            square = self.a_star.get_square(pos)
            if square:
                self.a_star.toggle_wall(square[0], square[1])

    def on_render(self):
        """ Drawing routine. """
        self._display_surf.fill((255, 255, 255))
        self.a_star.draw_grid()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        """ The main loop. """
        if self.on_init() == False:
            self._running = False
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App(10)
    theApp.on_execute()
