*****************************************************************************
This program has been developed in 3 stages and presents a text-based menu, through which
the user can select:
 a) to load each of three bus transportation data files
 b) selectively display contents of those data files
 c) save or retrieve that data to or from a Python pickle file
 d) display a map of the city of Edmonton, and interact with it by mouse clicks:
    e) plot selected bus routes
    f) plot locations of 5 bus stops closest to where the user mouse is clicked
--------------------------------------------------------------------------------
CONTENTS
A) The Big Picture
B) Project Specs: excerpt
C) Data File Details
D) Development Plan
E) Program Organization
--------------------------------------------------------------------------------
A) THE BIG PICTURE
1. using graphics.py, an image (provided) of the map of the city of Edmonton is
   displayed, which the user can "interact" with via simple clicks; see below
2. Edmonton Transit System (ETS) information, consisting of several text data 
   files in a zip file, is available from:
   https://data.edmonton.ca/Transit
          /ETS-Bus-Schedule-GTFS-Data-Schedules-zipped-files/urjq-fvmq
   Files of interest to this program are: Trips.txt, Shapes.txt, and Stops.txt
   For ref, a map can be viewed at: City of Edmonton Corporate Boundary Map
       https://data.edmonton.ca/Administrative
              /City-of-Edmonton-Corporate-Boundary-Map/4y6q-mtg6
   A map of Edmonton can (maybe) be obtained from:
     https://www.openstreetmap.org
            /search?query=Edmonton%20city#map=10/53.5321/-113.3878
     https://wiki.openstreetmap.org/wiki/Main_Page
     https://wiki.openstreetmap.org/wiki/Downloading_data
   
3. the end objective is that:
   a) the user can enter a route identifier (ex. 1, 401, or other from among 
      ??? of them), click on a button, and the route is then plotted on the map,
      based on the above-mentioned data text files
   b) if the user clicks on the map, the closest 5 bus stop(s) are shown
4. for that purpose, three data files are loaded into suitable dictionary
   structures, from which the necessary information is retrieved, as needed,
   based on user input to produce desired plots on the map
5. the program starts by presenting a plain text-based menu, from which the user
   can select to (1) read the data files into suitable dictionary structures
   (2) display selected entries from those dictionaries, (3) display the map to
   interact with the user, (4) save data structures to, or retrieve from,
   a pickle file, or (5) plot the map and "interact" with it
6. Overall program development is in 3 stages: MS1, MS2, and MS3, such that:
   MS1 and MS2 can be imported into MS2 and MS3, respectively.
--------------------------------------------------------------------------------
B) FROM SPECS
This program:
a) parses Edmonton Transit System (ETS) data available from the City of Edmonton
   Open Data Catalogue
b) provides a user interface to explore and plot some of these data.

The "ETS Bus Schedule GTFS Data Schedules" files can be obtained from the Open
Data catalogue at the following URL: 
 - (2017): https://data.edmonton.ca/Transit
                  /ETS-Bus-Schedule-GTFS-Data-Schedules-zipped-files/gzhc-5ss6 
       or: http://goo.gl/To5qec
 - (2019): https://data.edmonton.ca/Transit
                  /ETS-Bus-Schedule-GTFS-Data-Schedules-zipped-files/urjq-fvmq

MILESTONES

MS1 .........................................................
This focuses on: 
  a) loading ETS files Trips.txt and Shapes.txt, into proper data structures
  b) developing a text menu-based interface to access these data structures
     (selection numbering refers to final case in MS3):
       (1) Load shape IDs from GTFS file
       (2) Load shapes from GTFS file
       (4) Print shape IDs for a route
       (5) Print points for a shape ID
       (0) Quit
       Enter command: 

MS2..........................................................
This involves creating a graphics.py-based GUI, by which the user
can plot bus routes as lines. The menu presents additional options:
       (7) Save shapes and shape IDs in a pickle file
       (8) Load shapes and shape IDs from a pickle file
       (9) Display interactive map

IMPORTANT DETAIL: After selecting 9-GUI in the menu, the menu system does not
become active again until the user closes the GUI, i.e. the menu system calls
a function that implements the GUI, which returns only after the user closes
the window by clicking on [X] in the Windows app.

After creating the window, setCoords() is executed, with arguments:
 -113.7136, 53.39576, -113.2714, and 53.71605. Subsequent mouse clicks return
geographic (lat, lon) coordinates, ex. 53.61624646675359, -113.44574912559618
Method toScreen() can be used to convert to pixels, ex. (x, y): (381, 239)
When interacting with GUI, print() output may be queued up and not immediately
display anything; execute sys.stdout.flush(), which will require: import sys
When user enters a bus valid route number in the text entry box and clicks on 
PLOT "button", a bus route is plotted (using lines) using the one shape for that
bus route with the most points, using colour "gray50" with width 3.

MS3 ............................................................
This involves:
  a) extending the text interface to access this data structure:
       (3) Load stops from GTFS file: to load file Stops.txt
       (6) Print stops for a location: to display contents from the above
  b) extending the GUI to plot bus stops near where the user clicks the mouse
       
--------------------------------------------------------------------------------
C) DATA FILE DETAILS
NOTE: refer to further file details below
Data files: contents and purpose:

  FILES:     --> DICTIONARY    PURPOSE
  Trips.txt      route_shapes  Every route_id defines a set of unique shape_id's
  Shapes.txt     shapes        Every shape_id defines a set of geographical
                               coordinates to plot a bus route on the map
  Stops.txt      stops         Plot dots at bus stop locations near mouse click

FILE DETAILS
Trips.txt (MS1) - underline identify items pertinent to this program:
   route_id,service_id,trip_id,trip_headsign,direction_id,block_id,shape_id
   1,1-Saturday-1-DEC16-0000010,12300994,"1",0,3271662,1-30-1
   -                                                   ------
   ...
   113,113-Saturday-1-DEC16-0000010,12302515,"1",0,3271595,113-23-1
   ---                                                     --------
   ...
   For our purposes, for every 1-3 digit route_id, before first comma, there are
   several lines with various shape_id 
      ex. '113' --> '113-22-1', '113-23-1', '113-24-1' ...
           ---                               --------
   Thus, a dictionary must be constructed to collect for every route_id a 
   collection of all unique shape_id strings, ex.:
      dict['113'] = collection of '113-22-1', '113-23-1', '113-24-1' ...
            ---                    --------    --------    --------
   NOTE: In MS1, this collection consists of space-separated shape_id strings
   NOTE: In MS3, this collection consists of a list of these shape_id strings
   !!! ==> Accordingly, MS1 should be "fixed" for consistency with MS3
   
Shapes.txt (MS1):
   shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence
   1-30-1,53.53864,-113.42325,1
   1-30-1,53.53863,-113.42329,2
   ...
   For every shape_id, there is a collection of geographical latitude-longitude
   coordinates over several lines (maybe hundreds) with which to plot a bus 
   route. Thus, a dictionary is required to define something like:
     '1-30-1' : [ (53.53864, -113.42325), (53.53863, -113.42329), ... ]

   So, a route, ex. '1', ... '104' ... '304' ... '966' ... '99' (408 of'em)
   defines a set of shape_id strings, ex. 
        '99' : [ '99-26-1', '99-25-1', '99-8-1', '99-21-1' ]
   and every shape_id defines a set of geographical coordinates, ex.:
        '845-40-1' : [ (53.60622, -113.45084), (53.60827, -113.4496), ... ]
   with which to plot a bus route.
   
Stops.txt (MS3):
   stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url, ...
                                                ... location_type,parent_station
   1001,1001,"Abbottsfield Transit Centre",,  53.571965,-113.390362,,,0,
   1002,1002,"Abbottsfield Transit Centre",,  53.572087,-113.390058,,,0,
   ...
   This file assigns to every bus stop a name, a numerical stop_id, and 
   geographical coordinates, which will serve to determine the distance to a
   mouse click on the map, and to construct a list, from which the 5 with
   shortest distance values will be used to plot on the map.
--------------------------------------------------------------------------------
D) DEVELOPMENT PLAN

MS1
 1. Examine all three files, to determine their structure, and how to extract
    the components of interest to construct the respective dictionaries.
 2. Present text menu to user, prompt to enter selection, and ensure validity
 3. Anticipating to open 3 files from 3 menu selections, prompting user for 
    file name for each, and seeing similar structure of all 3 files (Trips.txt,
    Shapes.txt, and Stops.txt by MS3), envisage:
     - a common function to prompt user for file name, with specified default
     - a common function to open file and return contents in a common type of 
       structure, ex. list of line strings
     - 3 distinct functions (2 in MS1, and 1 in MS3) to obtain file contents
       and each to build a dictionary specific to information of interest
    NOTE: useful point to keep in mind: in MS2 and MS3, the internal data 
    structures will be saved to a pickle file and subsequently retrieved.
    HOWEVER, in MS2 only two such structures are saved & retrieved, and all 3
    in MS3. BUT, it may happen that a pickle file is created in MS3, ex. by
    instructor for test purposes, and retrieved in MS2, ex. by student during
    development. Thus, it is useful to anticipate this aspect.
 4. develop functions to display information for first two dictionaries

MS2
 5. open and display map
 6. display mouse click coordinates
 7. develop functions to create a "button" and detect click in button
 8. develop function to create a user Entry box

MS3
 9. develop function print top five stops when user clicks anywhere on the map
 10. develop function to display top five spots in the location the user clicks on in the map
 11. expand menu to include these functionalities
 12.develop function to display stops

--------------------------------------------------------------------------------
E) PROGRAM ORGANIZATION

MS1:
 - menu()
 - fPath = get_fPath(fName)
 - file_contents_list = read_file(fPath)
 - route_shape_ids = load_shape_ids(fPath)
 - route_shapes = load_shapes(fPath)
 - print_shape_ids(route_shape_ids)
 - print_points(route_shapes)
 - main()

MS2:
 - pickle_data(route_shapes, shapes) : save data to pickle file
 - unpickle_data()                   : load data from pickle file
 - enter(window)                     : create Entry object to input route
 - plot_button(window)               : create Plot button object
 - get_long_lat(point)
 - max_points_shape(routes_dict, shapes_dict, route)
 - draw_route(window, shapes_dict, max_shape)
 - iMap(route_shapes, shapes, img_fName)
 - menu() : updated for MS2
 - main() : updated for MS2
 
MS3:
 - load_stops(filename)
 - print_stops(stops_dict)
 - haversine(lat1, lon1, lat2, lon2)
 - calc_closest(lat, long, stops)
 - print_closest_stops(five_closest)
 - plot_stops(closest_stops, win)
 - menu() : updated for MS3
 - main() : updated for MS3
*****************************************************************************