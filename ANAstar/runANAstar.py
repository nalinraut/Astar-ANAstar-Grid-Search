import sys
from PIL import Image
import copy
import time
import matplotlib.pyplot as plt

'''
These variables are determined at runtime and should not be changed or mutated by you
'''
start = (0, 0)  # a single (x,y) tuple, representing the start position of the search algorithm
end = (0, 0)    # a single (x,y) tuple, representing the end position of the search algorithm
difficulty ="  " # a string reference to the original import file

'''
These variables determine display coler, and can be changed by you, I guess
'''
NEON_GREEN = (0, 255, 0)
PURPLE = (0, 0, 255)
LIGHT_GRAY = (50, 50, 50)
DARK_GRAY = (100, 100, 100)

'''
These variables are determined and filled algorithmically, and are expected (and required) be mutated by you
'''
path = []       # an ordered list of (x,y) tuples, representing the path to traverse from start-->goal
closed = {}   # a dictionary of (x,y) tuples, representing nodes that have been expanded
frontier = {}   # a dictionary of (x,y) tuples, representing nodes to expand to in the future

totalcost = []
ct = []

es = []
et = []

start_time=0

G = 9999999999999999
E = 9999999999999999

size = (0, 0)

class Cell:

    def __init__(self, XY, h, g, parent):

        global G

        self.XY = XY
        self.h=h
        self.g=g
        self.f=self.g+self.h
        self.parent= parent

        if self.h!=0:
            self.e= (float)(G - self.g)/self.h
        else:
            self.e = 9999999999999999


    def update(self):
        global G
        if self.h!=0:
            self.e= (float)(G - self.g)/self.h
        else:
            self.e = 9999999999999999

    def __cmp__(self, other):
        return cmp(self.e, other.e)

def  get_heuristic(current, goal):
    return 10*(abs(current[0]-goal[0]) + abs(current[0]-goal[1]))

def get_NextCellCost(parent):
    return(parent.g+10)

def get_PriorityCell():
    keys = frontier.keys()
    values = frontier.values()
    maxKeyCell = keys[values.index(max(values))]
    return maxKeyCell, frontier.pop(maxKeyCell)

def get_adjCells(currentCell, grid):
     
    global size

    current = currentCell.XY
    parentCurrent = currentCell.parent.XY

    reachable = []
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    for d in directions:
        adjX = current[0] + d[0]
        adjY = current[1] + d[1]

        if adjY>0 and adjX>0 and adjY<size[1] and adjX<size[0]:
            if grid[adjX, adjY]==0 and (adjX,adjY) != parentCurrent:
                h= get_heuristic((adjX, adjY), end)
                g= get_NextCellCost(currentCell)

                reachable.append(Cell((adjX, adjY), h, g, currentCell))

    return reachable

def pruneFrontier():

    for k in frontier.keys():
        if (frontier[k].g + frontier[k].h) >= G:
            del frontier[k]
        else:
            frontier[k].update()

def get_InitCell(start):
    h= get_heuristic(start, end)
    g=0
    f=g+h
    dParent= Cell(None,0,0,None)
    return Cell(start, h, g, dParent)

def get_path(endCell):

    global path

    path = []
    curr = endCell
    while curr.XY != start:
        path.append(curr.XY)
        curr = curr.parent
    path.reverse()

    totalcost.append(len(path))
    ct.append(time.time() - start_time)

    return len(path)


def ANAstar(grid):

    frontier.update({start:get_InitCell(start)})
    end = None

    start_time = time.time()

    while len(frontier)!=0:
        localOptimum = improveSolution(grid)

        if localOptimum is not None:
            end = localOptimum

            totalcost = get_path(end)

            print "Length of Path: ", totalcost
            print "e(s): ", format(E),"\n"

            visualize_search("out.png")


        pruneFrontier()

    totalcost = get_path(end)
    print "Length of Path: ", totalcost
    print "e(s): ", format(E),"\n"

    visualize_search("out.png")

def improveSolution(grid):

    global G, E

    while len(frontier)!=0:

        currPosition, currCell = get_PriorityCell()
        closed.update({currPosition:currCell})

        if currCell.e < E and currCell.e >1:
            E = currCell.e
            es.append(E)
            et.append(time.time() - start_time)

        if currCell.XY == end:
            G = currCell.g
            return currCell

        adjCells = get_adjCells(currCell, grid)

        for adjcell in adjCells:
            temp = adjcell.XY

            if frontier.has_key(temp):
                if adjcell.g < frontier[temp].g and (adjcell.g_adjcell.h)<G:
                    frontier.update({temp:adjcell})

            elif closed.has_key(temp):
                if adjcell.g < frontier[temp].g and (adjcell.g_adjcell.h)<G:
                    closed.update({temp:adjcell})
                    frontier.update({temp:closed.pop(temp)})

            else:
                frontier.update({temp:adjcell})


def visualize_search(save_file="do_not_save.png"):
    """
    :param save_file: (optional) filename to save image to (no filename given means no save file)
    """
    im = Image.open(difficulty).convert("RGB")
    pixel_access = im.load()

   

    # draw frontier pixels
    for pixel in frontier.keys():
        pixel_access[pixel[0], pixel[1]] = LIGHT_GRAY

    # draw expanded pixels
    for pixel in closed.keys():
        pixel_access[pixel[0], pixel[1]] = DARK_GRAY

    # draw path pixels
    for pixel in path:
        pixel_access[pixel[0], pixel[1]] = PURPLE

    # draw start and end pixels
    pixel_access[start[0], start[1]] = NEON_GREEN
    pixel_access[end[0], end[1]] = NEON_GREEN

    # display and (maybe) save results
    im.show()
    if(save_file != "do_not_save.png"):
        im.save(save_file)

    im.close()

def plotting(es,et,totalcost,ct):

    totalcost.reverse()
    ct.reverse()

    plt.figure(1)
    plt.title("Total Cost vs Time")
    plt.plot(ct, totalcost, 'g-')
    plt.xlabel('Time (s)')
    plt.ylabel('Total Cost (steps)')
    plt.show()

    es.reverse()
    et.reverse()

    plt.figure(2)
    plt.title("Suboptimality vs Time")
    plt.plot(et, es, 'r-')
    plt.xlabel('Time (s)')
    plt.ylabel('Suboptimality e(s)')
    plt.show()





if __name__ == "__main__":
    # Throw Errors && Such
    # global difficulty, start, end
    a=time.clock()
    assert sys.version_info[0] == 2                                 # require python 2 (instead of python 3)
    assert len(sys.argv) == 2, "Incorrect Number of arguments"      # require difficulty input

    # Parse input arguments
    function_name = str(sys.argv[0])
    difficulty = str(sys.argv[1])
    print "running " + function_name + " with " + difficulty + " difficulty."

    # Hard code start and end positions of search for each difficulty level
    if difficulty == "trivial.gif":
        start = (8, 1)
        end = (20, 1)
    elif difficulty == "medium.gif":
        start = (8, 201)
        end = (110, 1)
    elif difficulty == "hard.gif":
        start = (10, 1)
        end = (401, 220)
    elif difficulty == "very_hard.gif":
        start = (1, 324)
        end = (580, 1)
    elif difficulty =="self.gif":
        start = ()
        end =()
    else:
        assert False, "Incorrect difficulty level provided"

    # Perform search on given image
    im = Image.open(difficulty)
    size = im.size
    a=time.time()
    ANAstar(im.load())
    b=time.time()
    c=b-a
    plotting(es,et,totalcost,ct)

    print "===================================================================="
    print " Total time taken to find optimal path: ", c, "s"








   
    
