import a_star_path_finding as pf
import sys
from PIL import Image
import copy
import time

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
BLUE = (0, 0, 255)
LIGHT_GRAY = (50, 50, 50)
DARK_GRAY = (100, 100, 100)

'''
These variables are determined and filled algorithmically, and are expected (and required) be mutated by you
'''
path = []       # an ordered list of (x,y) tuples, representing the path to traverse from start-->goal
expanded = ()   # a dictionary of (x,y) tuples, representing nodes that have been expanded
frontier = ()   # a dictionary of (x,y) tuples, representing nodes to expand to in the future


def search(maze):
	"""
	This function is meant to use the global variables [start, end, path, expanded, frontier] to search through the
	provided maze.
	:param maze: A '1-concept' PIL PixelAccess object to be searched. (basically a 2d boolean array)
	"""

	# O is unoccupied (white); 1 is occupied (black)
	print "pixel value at start point ", maze[start[0], start[1]]
	print "pixel value at end point ", maze[end[0], end[1]]

	# put your final path into this array (so visualize_search can draw it in purple)
	#path.extend([(8,2), (8,3), (8,4), (8,5), (8,6), (8,7)])

	# put your expanded nodes into this dictionary (so visualize_search can draw them in dark gray)
	#expanded.update({(7,2):True, (7,3):True, (7,4):True, (7,5):True, (7,6):True, (7,7):True})

	# put your frontier nodes into this dictionary (so visualize_search can draw them in light gray)
	#frontier.update({(6,2):True, (6,3):True, (6,4):True, (6,5):True, (6,6):True, (6,7):True})
	walls=[]

	for x in xrange(im.size[0]):
		for y in xrange(im.size[1]):
			if maze[x,y] == 1:
				walls.append((x,y))

	#visualize_search("out.png") # see what your search has wrought (and maybe save your results)
	return walls

def problem(height, width, walls, start, end):
    a= pf.AStar()
    a.init_grid(height, width, walls, start, end)
    path = a.solve()

    #visualize_search("out.png")
    return path



def visualize_search(save_file, path):
    """
    :param save_file: (optional) filename to save image to (no filename given means no save file)
    """
    im = Image.open(difficulty).convert("RGB")
    pixel_access = im.load()

    

    # draw path pixels
    for pixel in path:
        pixel_access[pixel[0], pixel[1]] = BLUE

    # draw start and end pixels
    pixel_access[start[0], start[1]] = NEON_GREEN
    pixel_access[end[0], end[1]] = NEON_GREEN
    '''
    # draw frontier pixels
    for pixel in frontier.keys():
        pixel_access[pixel[0], pixel[1]] = LIGHT_GRAY

    # draw expanded pixels
    for pixel in expanded.keys():
        pixel_access[pixel[0], pixel[1]] = DARK_GRAY
    '''
    # display and (maybe) save results
    im.show()
    if(save_file != "do_not_save.png"):
        im.save(save_file)

    im.close()




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
    else:
        assert False, "Incorrect difficulty level provided"

    # Perform search on given image
    im = Image.open(difficulty)
    height = im.size[0]
    width = im.size[0]
    walls=tuple(search(im.load()))

    path = problem(height, width, walls, start, end)
    b=time.clock()
    c=b-a
    print path
    visualize_search("out.png", path)

    
    
    print "===================================================================="
    print " Total time taken to find optimal path: ", c, "s"



   
    
