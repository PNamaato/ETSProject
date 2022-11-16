name  = "Cmpt103W21_X02L_MS3_NP.py  1.00  210309  PENINAH NAMAATO"
from pprint import PrettyPrinter, pprint
import pickle  # MS2-3
from graphics import *    # NOTE: 4.2

LON_L, LAT_N, LON_R, LAT_T =  -113.7136, 53.39576, -113.2714,53.71605
def pp(X, w=50):
    PrettyPrinter(indent=2, width=w).pprint(X)
from math import radians, sin, cos, sqrt, asin
import sys

#===============================================================================

def save_in_pickle(points, shapes,stops, fPath='etsdata.p'):
    '''
    Takes points(coordinates), shapes(shape_IDs). Asks the user for file name,
    if the user enters nothing, the filename defaults to fPath. Points and
    shapes are saved into a pickle file. Returns None
    '''
    fil = input(f'Enter a file name [{fPath}]: ')
    s_p = (points,shapes,stops)

    try:
        f = open( fPath, "wb")
    except:
        f = open( fil, "wb")
    pickle.dump( s_p, f)
    f.close()
    return None

#-------------------------------------------------------------------------------

def load_pickle(fPath='etsdata.p'):
    '''
    Asks the user for file name, if the user enters nothing or file does 
    not exist, then filename defaults to fPath. Loads shapes and shape_ids
    from pickle file. Returns a tuple of shape_ids and shapes.
    '''
    fil = input(f'Enter a file name [{fPath}]: ')
    try:
        f = open( fil, "rb" )
    except:
        f = open( fPath, "rb" )
    points_shapes_stops = pickle.load( f )
    f.close()

    return points_shapes_stops

#===============================================================================
# INTERACTIVE MAP GUI
def btn_create(x,y,w,h,label,win):
    '''
    This function creates button to be dislayed on the window for the user.
    This expects six arguments. x and y cordinates that determine the top left 
    corner of a button. w and h determine the bottom right corner of the button.
    label is displayed on thewindow to tell user what the button is used for.
    win is the window where the button will be displayed.
    '''
    r = Rectangle(Point(x,y), Point(x+w, y+h))
    r.draw(win)
    t = Text(r.getCenter(), label)
    t.draw(win)
    r.setFill('white')
    return r,t
 
#-------------------------------------------------------------------------------

def btn_clicked(pt,btn):
    '''
    This function Returns True if Point object pt is inside button: 
    btn = Tuple => (Rectangle,Text)... inside button. 
    '''
  # NOTE: Point coords available s: pt.x,pt.y
    p1, p2 = btn[0].getP1(), btn[0].getP2()  # btn[0] access coords of rectangle
    if p1.x < pt.x < p2.x and p1.y< pt.y < p2.y:
        return (p1.x < pt.x < p2.x) and (p1.y < pt.y < p2.y)

#-------------------------------------------------------------------------------

def plot_bus_route(win,coord_list):
    '''
    This function will plot bus routes for the user. Takes win = window,
    coord_list = list of one shape for that bus route with the most points.
    Uses colour "gray50" with width 3. Returns None.
    '''
    for k in range(len(coord_list)-1):
        y,x = coord_list[k]
        ty,tx = coord_list[k+1]
        line = Line( Point(x, y), Point(tx, ty) )
        line.setFill('grey50')
        line.setWidth(3)
        line.draw(win)
    return None

#-------------------------------------------------------------------------------

def get_coord_list(route, shapes, coords):
    '''
    This function takes route which is used to find shape id in the dictionary
    shapes. The shape id is in turn used to  find coordinates for the route.
    max_len is implemented to keep track of the shape_id with the most points.
    The values of the shape_id with the most points is returned in coord_list.
    Ex.Usage:
       route = '1'
       shapes[1]  = [1-30-1, 1-32-1, 1-31-1, 1-33-1, 1-35-1, 1-36-1,...,1-39-1']
       shape_id = 1-30-1
       coords[1-30-1] = [ (53.53864, -113.42325), (53.53863, -113.42329), 
                       (53.5386, -113.42332), ... (53.5206, -113.62288) ]
    '''
    max_len  = 0
    for shape_id in shapes[route]:
        if len(coords[shape_id])> max_len:
            max_len = len(coords[shape_id])
            shape_id_max = shape_id

    coord_list = coords[shape_id_max]
    return coord_list

#-------------------------------------------------------------------------------

def interaction(win, shapes, points, btn_PLOT, usr_in, stops):
    '''
    This expects shapes and points(coords) used to call get_coord_list.
    usr_in contains the route number the user entered into the entry box.
    When the user clicks on the “Plot” rectangle, the program responds.
    If the provided route number does not exist, it ignores the button press. If
    it exists, it plots (using lines) that bus route.
    '''
    while True:
      # win.getMouse() returns Point(x,y) in new cordinates
        try:
            lon_lat = win.getMouse()
        except GraphicsError:
            return None

      # convert Point(long,lat) to (x,y) in pixels:
        xy = win.toScreen(lon_lat.x,lon_lat.y) #Tuple:(x,y) coords in pixl units
        pt = Point(xy[0], xy[1])

        #if btn_clicked(pt, btn_CLOSE):
            #btn_CLOSE[1].setText('BYE BYE')
            #btn_CLOSE[1].setTextColor('red')
            #break

        if btn_clicked(pt, btn_PLOT):
            route = usr_in.getText()
            if route in shapes:
                #btn_PLOT[1].setText(f'Bus: {usr_in.getText()}')
                #btn_PLOT[1].setText(f' {len(shapes[route])} shape_ids')
                coord_list = get_coord_list(route,shapes,points)
                plot_bus_route(win,coord_list)
            else:
                btn_PLOT[1].setText('PLOT')
        else:
            five_closest = calc_closest(lon_lat.y,lon_lat.x, stops)
            plot_stops(five_closest, win)
            print_closest_stops(five_closest)
    return None
    
#-------------------------------------------------------------------------------
def Edmonton_map_GUI(shapes, points, stops):
    '''
  This expects bus route dictionary and shapes. Creates a GraphWin in which it 
  displays the map of Edmonton and Plot buttons. It also displays the user entry
  box and graphs the bus route the user specified if it exists.
  '''

    img = Image(Point(0, 0), 'Background.gif')
    w, h = img.getWidth(), img.getHeight()
    win = GraphWin('Edmonton Transit System', w, h)
    img.move(w // 2, h // 2)
    img.draw(win)

    #btn_CLOSE = btn_create(w-100,20,70,20, 'CLOSE', win)
    btn_PLOT = btn_create(100,20,70,20,'PLOT', win)

    # user entry box:
    usr_in = Entry(Point(50,30), 5)
    usr_in.draw(win)
    usr_in.setFill('grey50')
    usr_in.setTextColor('white')

    ##Non interactive
    #info_msg = btn_create(w//2-50,20,100,40,'MOUSE\nCLICK', win)
    #info_msg[1].setTextColor('red')

    win.setCoords(LON_L, LAT_N, LON_R, LAT_T)
    interaction(win, shapes, points, btn_PLOT, usr_in, stops)
    #info_msg[1].setText(f'{lon_lat.x:.4f}\n{lon_lat.y:.4f}')
    win.close()

#===============================================================================
# MS III
def load_stops(fPath = 'data/stops.txt'):
    '''
    This reads bus stop information from file fName, where each line is like:
       "1001,1001,"Abbottsfield Transit Centre",,  53.571965,-113.390362,,,0,"
        0   1    2                             34           5           678 9
         ID        name                           longitude   latitude
    and returns a dictionary with bus stop (long, lat) as keys, and a list of
    (bus stop ID, bus stop name) tuples for each; ex.:
    {  (53.571965, -113.390362) :  [ ('1001', 'Abbottsfield Transit Centre') ]
            :           :               :                  :                   }
    NOTE: examination of the resulting dictionary and source text file seems to
    indicate that there is a one to one relationship between the dictionary keys
    and bus stops in the text file, suggesting that there is no need for a list
    of bus stop info for each key.
    '''
    stops = {}  # To be returned
    EOF = ''

    # open file. Try and except
    fil = input(f'Enter a file name [{fPath}]: ')
    try:
        f = open(fil)
    except:
        f = open(fPath)

    line = f.readline()  # skip first line
    line = f.readline()
    while line != EOF:
        line = line.strip().split(',')
        stop_id, stop_name, = int(line[0]), line[2].replace('"', '')
        lat_long = float(line[4]), float(line[5])
        if lat_long not in stops:
            stops[lat_long] = [stop_id,stop_name]
        line = f.readline()
    f.close()
    return stops
#-------------------------------------------------------------------------------

def print_stops(stops_dict):
    '''This expects  dictionary, like:
      { (53.595436, -113.421703): [9944, 'DL MacDonald Platform'], 
        (53.595527, -113.421853): [9945, 'DL MacDonald Platform'], 
        ...
        (53.512908, -113.526199): [9981, 'McKernan Belgravia Station'], 
        (53.513008, -113.526113): [9982, 'McKernan Belgravia Station'] }
        
    prompts user for a location as lat, lon and displays something like:
    Stops for (53.575137, -113.403388):
            1065 40 Street & 121 Avenue
    '''
    usr = input("Location as 'lat, lon'? ")

    try:
        sp = usr.split(',')
        location = ( float(sp[0]), float(sp[1]) )
    except:
        print(f'Stops for ({usr}):\n' '** NOT FOUND **')
        return None

    if location not in stops_dict:
        print(f'Stops for ({usr}):\n' '** NOT FOUND **')
    else:
        print(f'Stops for {location}:')
        for val in stops_dict[location]:
            print(f'\t{val[0]}\t{val[1]}')
    return None
#-----------------------------------------------------------------------------

def haversine(lat1, lon1,lat2, lon2):
    ''' 
    Returns great-circle distances between two points on earth from their 
    longitudes and latitudes ( (lat1, lon1(, and (lat2, lon2) )
    From: https://rosettacode.org/wiki/Haversine_formula#Python  
    Ex. haversine(36.12, -86.67, 33.94, -118.40) = 2887.25995 (km)
    '''

    R = 6372.8  # Earth radius in kilometers
 
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
 
    a = sin(dLat / 2)**2 + cos(lat1) * cos(lat2) * sin(dLon / 2)**2
    c = 2 * asin(sqrt(a))
 
    return R * c
#-----------------------------------------------------------------------------

def calc_closest(lat,long,stops):
    '''
    This expects GraphWin, and a list of bus stops, ex.:
      distance, stop_ID,  name                        , latitude , longitude 
           [0]      [1]   [2]                           [3]        [4]
    [[     4.1,  '1001', 'Abbottsfield Transit Centre', 53.571965, -113.390362], 
     [    21.3,  '1002', 'Abbottsfield Transit Centre', 53.572087, -113.390058], 
        ...
     [   192.3,  '1612', '34 Street & 119 Avenue', 53.57185, -113.393205]  ]
    and plots a Point at each one.
    '''

    # lat and long from user.
    d = []
    for coords, info in stops.items():
    ## coords[0] coords[1] info[0] info[1]
    ## lat       long         stop_id  name
        dist = haversine(lat,long ,coords[0], coords[1])
        d.append([round(dist*1000,1), info[0], info[1], coords[0],coords[1] ])
    return sorted(d)[1:6]
#--------------------------------------------------------------------------------

def print_closest_stops(five_closest):
    '''
    This expects GraphWin, and a list of bus stops, ex.:
      distance, stop_ID,  name                        , latitude , longitude 
           [0]      [1]   [2]                           [3]        [4]
    [[     4.1,  '1001', 'Abbottsfield Transit Centre', 53.571965, -113.390362], 
     [    21.3,  '1002', 'Abbottsfield Transit Centre', 53.572087, -113.390058], 
        ...
     [   192.3,  '1612', '34 Street & 119 Avenue', 53.57185, -113.393205]  ]
    and for each prints out the distance, bus stop id, and name.
    '''

    print('Nearest stops:\n'\
                     '\t\tDistance\tStop\tDescription')
    for i in five_closest:
        print(f'\t\t{i[0]}\t\t{i[1]}\t{i[2]}')
    sys.stdout.flush()
    return None
#--------------------------------------------------------------------------------

def plot_stops(closest_stops,win):
    '''
    This expects GraphWin, and a list of bus stops, ex.:
      distance, stop_ID,  name                        , latitude , longitude 
           [0]      [1]   [2]                           [3]        [4]
    [[     4.1,  '1001', 'Abbottsfield Transit Centre', 53.571965, -113.390362], 
     [    21.3,  '1002', 'Abbottsfield Transit Centre', 53.572087, -113.390058], 
        ...
     [   192.3,  '1612', '34 Street & 119 Avenue', 53.57185, -113.393205]  ]
    and plots a Point at each one.
    '''

    for l in closest_stops:
        y,x = l[4], l[3]
        pt = Point(y,x)
        pt.setFill('black')
        pt.draw(win)
    return None
#===============================================================================
def print_shape_ids(route_shape_ids):
    '''
    This expects a dictionary structured as follows:
      { '1'  : [1-30-1, 1-32-1, 1-31-1, 1-33-1, 1-35-1, 1-36-1, ... 1-39-1']
        '113': ['113-22-1 113-24-1 113-23-1'] ... }
    prompts user for for a route no., ex. 1, and then displays something like:
       ShapeIDs for 1:
       1-30-1
           1-32-1
           ...
           1-39-1
    '''

    route = input('Route? ')
    if route not in route_shape_ids:
        print(f'Shape IDs for {route}:\n' '** NOT FOUND **')
    else:
        print(f'Shape IDs for {route}:')
        for val in route_shape_ids[route]:
            print(f'\t{val}')
    return None
#--------------------------------------------------------------------------------

def print_points(route_shapes):
    '''
    This expects  dictionary, like:
      { '1-30-1'   : [ (53.53864, -113.42325), (53.53863, -113.42329), 
                       (53.5386, -113.42332), ... (53.5206, -113.62288) ]
        ...
        '977-14-1' : [ (53.45622, -113.42523), (53.45623, -113.42524), 
                       (53.45693, -113.42644), ... (53.45786, -113.42803) ] }
    prompts user for a shape ID and displays something like:
    Shape for 3-15-1:
        (53.54026, -113.59275)
        (53.54026, -113.59383)
        (53.54078, -113.59382)
         ...
        (53.54094, -113.49373)
        (53.54035, -113.49373)
        (53.53976, -113.49373)
    '''
    shape = input('Shape ID? ')
    if shape not in route_shapes:
        print('Shape for no_shape-id:\n' '** NOT FOUND **')
    else:
        print(f'Shape for {shape}:')
        for val in route_shapes[shape]:
            print(f'\t{val}')
    return None


#-------------------------------------------------------------------------------
def get_shape_ids(fPath='data/trips.txt'):
    '''
    Reads in the contents from a Trips.txt file from ETS of shape_id strings 
    for every bus route and returns a dictionary, structured like:
      { '1'  : '1-30-1 1-32-1 1-31-1 1-33-1 1-35-1 1-36-1 ... 1-39-1'
    '113': '113-22-1 113-24-1 113-23-1' ... }
    where the keys are bus route numbers, and values are list if unique shape 
    ids for every bus route.
    '''
    shapes = {}  # To be returned
    EOF = ''

    # open file. Try and except
    fil = input(f'Enter a file name [{fPath}]: ')
    try:
        f = open(fil)
    except:
        f = open(fPath)

    line = f.readline()  # skip first line
    line = f.readline()
    while line != EOF:
        line = line.strip().split(',')
        route_id, shape_id = line[0], line[-1]
        if route_id not in shapes:
            shapes[route_id] = [shape_id]
        else:
            if shape_id not in shapes[route_id]:
                shapes[route_id].append(shape_id)
                # shapes[route_id] = shapes[route_id] + ' '.join(shape_id)
        line = f.readline()
    f.close()
    return shapes


# ------------------------------------------------------------------------------


def get_shapeCordinates(fPath='data/shapes.txt'):
    '''
    This expects a file name, ex. Shapes.txt:
       shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence
       1-30-1,53.53864,-113.42325,1
       ...
       113-22-1,53.51991,-113.62076
       ...
    loads the file contents, skips the first line, and returns a dictionary of
    <key, value> pairs, with key = value before the first comma, and value = 
    a list of 2-tuples consisting of two float values after the first comma; ex:
       { '1-30-1' : [ (53.53864, -113.42325), 
              (53.53863, -113.42329) ... (53.5206, -113.62288) ]
     ...
     '113-22-1' : [ (53.52029, -113.62225),
            (53.52024, -113.62194), ... (53.52029, -113.62225) ]
     ... }
    '''

    coords = {}  # To be returned
    EOF = ''

    # open file. Try and except
    fil = input(f'Enter a file name [{fPath}]: ')
    try:
        f = open(fil)
    except:
        f = open(fPath)

    line = f.readline()  # skip first line
    line = f.readline()
    while line != EOF:
        shape_id, lat, long, x = line.strip().split(',')
        if shape_id not in coords:
            coords[shape_id] = [(float(lat), float(long))]
        else:
            coords[shape_id].append((float(lat), float(long)))
        line = f.readline()
    f.close()
    return coords


#-------------------------------------------------------------------------------


def menu():
    # Presents menu, and returns int value of user selection.
    print('\n\tEdmonton Transit System\n'
          '---------------------------------\n'
          '(1) Load shape IDs from GTFS file\n'
          '(2) Load shapes from GTFS file\n'
          '(3) Load stops from GTS file\n\n'
          '(4) Print shape IDs for a route\n'
          '(5) Print points for a shape ID\n'
          '(6) Print stops for a location\n\n'
          '(7) Save shapes, shape IDs, and stops in a pickle\n'
          '(8) Load shapes, shape IDs, and stops from a pickle\n\n'
          '(9) Display interactive map\n\n'
          '(0) Quit\n'
          '* Note: some functionalities will not work unless all files are loaded')

    ask = 'Enter command: '
    while True:
        num = input(ask)  # int
        if not num.isdigit():
            ask = 'Enter command: '
        elif int(num) < 0 or int(num) > 9:
            ask
        else:
            return int(num)


#-------------------------------------------------------------------------------


def main():
    while True:
        opt = menu()
        if opt == 1:
            route_shape_ids = get_shape_ids()
        elif opt == 2:
            route_shapes = get_shapeCordinates()
        elif opt == 3:
            stops = load_stops()
        elif opt == 4:
            try:
                print_shape_ids(route_shape_ids)
            except:
                continue
        elif opt == 5:
            try:
                print_points(route_shapes)
            except:
                continue
        elif opt == 6:
            try:
                print_stops(stops)
            except:
                continue
        elif opt == 7:
            try:
                save_in_pickle(route_shape_ids, route_shapes,stops)
            except:
                continue
        elif opt == 8:
            try:
                route_shape_ids, route_shapes, stops = load_pickle()
            except:
                continue
        elif opt == 9:
            #try:
            Edmonton_map_GUI(route_shape_ids,route_shapes, stops)
            #except:
                #continue
        elif opt == 0:
            print('Goodbye')
            break
    return None


#===============================================================================
if __name__ == '__main__':
    if input('Excecute tests (y/n): ') in 'Yy':
        shapes = get_shape_ids('data/trips.txt')
        pp(shapes)
        #coordinates
        points = get_shapeCordinates('data/shapes.txt')
        pprint(points['309-10-1'][:5])
        pprint(points['309-10-1'][-5:])
        stops = load_stops()
        Edmonton_map_GUI(shapes, points,stops)
    else:
        main()

#===============================================================================
