import heapq

#The basic object here is a cell so we write a class for it.
#We store the coordinates x and y, the values of G and H plus the sum F.
#reachable is cell reachable? not a wall?
class Cell(object):
      def __init__(self, x, y, reachable):
         #initialize new cell
          self.reachable = reachable
          self.x = x
          self.y = y
          self.parent = None
          self.g = 0
          self.h = 0
          self.f = 0

#Next is our main class named AStar. Attributes are the open list heapified (keep cell with lowest F at the top)
#the closed list which is a set for fast lookup,
#the cells list (grid definition) and the size of the grid
#dh l class 2li feh kol l functions 2li ht3mli l A star alogrithm
class AStar(object):
      def __init__(self):
          # open list
          self.opened = []
	  #hena ana ha7ot l child nodes bto3i fe l priority queue
	  #least F value has the highest priority
          heapq.heapify(self.opened) 
          # visited cells list
          self.closed=set()
          # MAP cells
          self.cells =[]
          # MAP height
          self.grid_height = None
	  # MAP width
          self.grid_width  = None

      #Prepare grid cells, walls. 

      def init_grid(self, width, height, walls, start, end):
          # walls are list of wall x,y tuples.
          # start is starting point x,y tuple.
          #end is ending point x,y tuple. 
          #walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),(3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
          self.grid_height = height
          self.grid_width = width
          for x in range(self.grid_width):
              for y in range(self.grid_height):
                  if (x, y) in walls:
                      reachable = False
                  else:
                      reachable = True
          #the next line decide any cell int our grid is reachable or not(obstacle)
                  self.cells.append(Cell(x, y, reachable))
          #self.start = self.get_cell(0,0)
          self.start = self.get_cell(*start)
          self.end = self.get_cell(*end)
          #self.end = self.get_cell(5,5)
      
          # Compute the heuristic value H for a cell: distance between
          #this cell and the ending cell multiply by 10.
      def get_heuristic(self, cell):
          #cell the point I want to check
          #cell.end is tuple of end point(x,Y)   
          return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))


       #Returns a cell from the cells list
       #bab3tlaha l x&y of cell w bitl3ahli from the list of cells
      def get_cell(self, x, y):
           return self.cells[x * self.grid_height + y]

       #Returns adjacent cells to a cell.
      def get_adjacent_cells(self, cell):
           cells = []
           if cell.x < self.grid_width-1:
              cells.append(self.get_cell(cell.x+1, cell.y))
           if cell.y > 0:
              cells.append(self.get_cell(cell.x, cell.y-1))
           if cell.x > 0:
              cells.append(self.get_cell(cell.x-1, cell.y))
           if cell.y < self.grid_height-1:
              cells.append(self.get_cell(cell.x, cell.y+1))
           return cells

       #Simple method to print the path found.
       #It follows the parent pointers to go from the ending cell to the starting cell.
      def display_path(self):
           cell = self.end
           path = [(cell.x, cell.y)]
           while cell.parent is not self.start:
                 cell = cell.parent
                 path.append((cell.x, cell.y))
                 #print('path: cell: %d,%d' % (cell.x, cell.y))
           path.append((self.start.x, self.start.y))
           path.reverse()
           print ' path is : \n', path
       
       #Update adjacent cell with G and H
      def update_cell(self, adj, cell):
           #adj is adjacent cell to current cell
           #cell is current cell being processed
          adj.g = cell.g + 10
          adj.h = self.get_heuristic(adj)
          adj.parent = cell #dh msh fahm bi3ml a
          adj.f = adj.h + adj.g
       #The main method implements the algorithm itself(Astar alogrithm)
       #find path to ending cell.
       #returns path or None if not found.    
      def process(self):
           # add starting cell to open heap queue
           heapq.heappush(self.opened, (self.start.f, self.start))
           while len(self.opened):
                 # pop cell from heap queue
                 f, cell = heapq.heappop(self.opened)
                 # add cell to closed list so we don't process it twice
                 self.closed.add(cell)
                 # if ending cell, display found path
                 if cell is self.end:
                    self.display_path()
                    break
                 # get adjacent cells for cell
                 adj_cells = self.get_adjacent_cells(cell)
                 for adj_cell in adj_cells:
                     if adj_cell.reachable and adj_cell not in self.closed:
                        if (adj_cell.f, adj_cell) in self.opened:
                           # if adj cell in open list, check if current path is
                           # better than the one previously found for this adj cell.
                           if adj_cell.g > cell.g + 10:
                              self.update_cell(adj_cell, cell)
                        else:
                             self.update_cell(adj_cell, cell)
	                     # add adj cell to open list
                             heapq.heappush(self.opened, (adj_cell.f, adj_cell))

#astar1
#width=7
#height=6
#walls= ((1, 1),(3,3),(3,1),(3,2),(3,4))
#start=(1,2)
#end=(5,1)
                             
#astar 2
width=6
height=6
walls= ((0, 5),(1,0),(1,1),(1,5),(2,3),(3,1),(3,2),(3,5),(4,1),(4,4),(5,1))
start=(0,0)
end=(5,5)
a = AStar()
a.init_grid(width, height, walls, start, end)
a.process()
