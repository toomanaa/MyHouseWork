"""
Termini example.
Scenario:
  A Road has  three servers and defines
  a dwell processes that takes some (random) time.
  Cars arrive at the road at a random time. If one server
  is available, it starts the process of send, process and receive.
  If not then the car chooses another server.
  Conflicts and movement authoritites have been captured.
"""

### Setup animation ### 
show_animation = True
hide_plots = False
# importing libraries to use (libraries contain code shortcuts)
import random
import simpy # DES
import numpy as np # a maths and plotting module
import pandas as pd # more data analysis
import matplotlib.pyplot as plt # 
import seaborn as sns
import math
import time
#matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

from tkinter import *

# Analyse the overall headway
def headway_analysis(time):
	time2 = time[1:]
	time3 = time[:-1]
	headway = []
	for i in range(len(time2)):
		headway.append(time2[i] - time3[i])
	return headway

################ SET UP ANIMATION CANVAS #################
class Car:
    def __init__(self, canvas, x1, y1, x2, y2, tag):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas = canvas
        self.car = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red", tags = tag)
        self.car_number = canvas.create_text(((self.x2 - self.x1)/2 + self.x1), ((self.y2 - self.y1)/2 + self.y1), text = tag)
        self.canvas.update()

    def move_car(self, deltax, deltay):
        self.canvas.move(self.car, deltax, deltay)
        self.canvas.move(self.car_number, deltax, deltay)
        self.canvas.update()
        
    def remove_car(self):
        self.canvas.delete(self.car)
        self.canvas.delete(self.car_number)
        self.canvas.update()


"""A server has a limited number of cpus to
    process tasks in parallel.
    Cars have to request one of the containers. When they got one, they
    can start the  processes and wait for it to finish (which
    takes ``delay`` ms).
    """
class Server(object):
   
    def __init__(self, env, num_vm):
        self.env = env
        self.server = simpy.Resource(env, num_vm)
        self.processingTime = np.random.normal(50, 10, 1)

    def process(self, car):
        with self.server.request() as request:
            yield request 
            yield self.env.timeout(self.processingTime)
    
    def load():
        return self.processingTime

class Clock:
    def __init__(self, canvas, x1, y1, x2, y2, tag):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas = canvas
        self.car = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="#fff")
        self.time = canvas.create_text(((self.x2 - self.x1)/2 + self.x1), ((self.y2 - self.y1)/2 + self.y1), text = "Time = "+str(tag)+"s")
        self.canvas.update()

    def tick(self, tag):
        self.canvas.delete(self.time)
        self.time = canvas.create_text(((self.x2 - self.x1)/2 + self.x1), ((self.y2 - self.y1)/2 + self.y1), text = "Time = "+str(tag)+"s")
        self.canvas.update()




if show_animation == True:
    animation = Tk()
    #bitmap = BitmapImage(file="uxbridge.bmp")

    #im = PhotoImage(file="uxbridge_resized.gif")

    canvas = Canvas(animation, width = 800, height = 400)
    #canvas.create_image(0,0, anchor=NW, image=im)
    animation.title("Mobile Edge Computing Environment")

    canvas.pack()

#### matplotlib plots
    

if show_animation == True and hide_plots == False:
    f = plt.Figure(figsize=(5,4), dpi=100)

    a1 = f.add_subplot(221) # mean headway
    #a2 = f.add_subplot(222) # TPH meter
    #a3 = f.add_subplot(223) # headway distribution
    #a4 = f.add_subplot(224) # train count

    a1.plot()
    #a2.plot()
    #a3.plot()
    #a4.plot()

    from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
    
    dataPlot = FigureCanvasTkAgg(f, master=animation)
    dataPlot.draw()
    dataPlot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    f.tight_layout()

    canvas.pack()

# platforms
if show_animation == True:
    canvas.create_rectangle(100, 100, 200, 150, fill = "yellow")
    canvas.create_rectangle(300, 100, 400, 150, fill = "yellow")
    canvas.create_rectangle(500, 100, 600, 150, fill = "yellow")

   
    

    canvas.create_line(50, 75, 200, 75, fill="green", width=3) # platform 4
    canvas.create_line(50, 175, 200, 175, fill="green", width=3) # platform 2/3
    #canvas.create_line(50, 275, 200, 275, fill="green", width=3) # platform 1

    canvas.create_text(150, 110, text = "Server 3")
    canvas.create_text(350, 110, text = "Server 2")
    canvas.create_text(550, 110, text = "Server 1")
    
    #canvas.create_text(125, 210, text = "Platform 2")
    #canvas.create_text(125, 240, text = "Platform 1")

# track
    canvas.create_line(200, 75, 650, 75, fill="green", width=3) # platform 4 run out
    canvas.create_line(200, 175, 650, 175, fill="green", width=3) # platform 2/3 run in
   # canvas.create_line(300, 175, 400, 75, fill="green", width=3)
    #canvas.create_line(450, 75, 600, 175, fill="green", width=3)
    #canvas.create_line(450, 175, 600, 75, fill="green", width=3)
    #canvas.create_line(200, 275, 300, 275, fill="green", width=3)
   # canvas.create_line(300, 275, 400, 175, fill="green", width=3)

############ END OF CANVAS #################

# set platform status - changing one of these to "True" at this stage will permanently close the platform as no train will actually be present in the platform, so the platform will never become free
server_1_occupied = False
server_2_occupied = False
server_3_occupied = False
#platform_4_occupied = False
NUM_SERVERS = 3  # Number of platforms in the termini (needs to match how many platforms are initially set to "False" occupancy

# setting up empty lists to store results in
time = []
headway = []
moving_avg_headway = []
moving_stdev_headway = []
car_number = []
processingTime = []
n = 0

# set up general parameters
RANDOM_SEED = 45
T_INTER = 60   # Arrival headway: create a car on average every T_INTER seconds, setting this to "1" is a reasonable approximation to "as fast as possible" without slowing down the simulation
SIM_TIME = 100000     # Simulation time in seconds
dwelltime = 60

# set up random variable for train arrival times
def arrival_interval(T_INTER):
    t = random.expovariate(1.0/T_INTER) # exponential distribution, not particularly useful for "as fast as possible", more useful if we want to try to reproduce real world arrival times
    return t

# set up the dwell variable
def dwell():
	# a few different options here - lognormal is normally most representative of human error and general dwell times
	#t = random.randint(120, 240) # uniformly distributed
    t = random.lognormvariate(math.log(dwelltime), 1) # lognormally distributed
        #t = random.triangular(dwelltime * 0.9, dwelltime * 1.1, dwelltime) # triangular distribution (low, high, mid)
        #t = dwelltime # fixed dwell
    return t

# define empty dictionary
output_dict = {'Car ID':[], 'Time':[], 'Event Type': [], 'Event Description': []}
ID = []
t_now = []
e_type = []
e_description = []


# define the termini
class Road(object):
    """A termini has a limited number of platforms (``NUM_platforms``) to
    clean trains in parallel.
    Trains have to request one of the platforms. When they got one, they
    can start the washing processes and wait for it to finish (which
    takes ``dwelltime`` minutes).
    """
    def __init__(self, env, num_servers):
        self.env = env
	# below are the "resources" the termini has which trains compete for
        self.server = simpy.Resource(env, num_servers)
        self.run_out_authority = simpy.Resource(env, 1)
        self.run_in_authority = simpy.Resource(env, 1)
        self.s1_outbound = simpy.Resource(env, 1)
        self.s2_outbound = simpy.Resource(env, 1)
        self.s2_outbound = simpy.Resource(env, 1)

    def dwell(self, car, server):
        """The dwell processes."""
        yield self.env.timeout(dwell()) # this calls the dwell time

def write_data(car_id, time, event, description):
    output_dict['Car ID'].append(car_id)
    output_dict['Time'].append(time)
    if event == 'req':
        output_dict['Event Type'].append('Request resource')
    elif event == 'sei':
        output_dict['Event Type'].append('Seize resource')
    elif event == 'rel':
        output_dict['Event Type'].append('Release resource')
    elif event == 'sp':
        output_dict['Event Type'].append('Start process')
    elif event == 'fp':
        output_dict['Event Type'].append('Finish process')
    else:
        raise Exception('Event type code not properly defined in data write')
    output_dict['Event Description'].append(description)
    

# below is the process which a train follows when generated
def car(env, name, road):
    """The car process (each train has a ``name``) arrives at the server
    (``tr``) and requests a contianer.
    It then starts the process, waits for it to finish and
    leaves to never come back ...
    """
# setting global variables - this allows the processes to tell eachother when a specific platform is free/emptys
    global server_1_occupied
    global server_2_occupied
    global server_3_occupied
    global server1
    global server2 
    global server3 
    global baseLine_Load 
    #global platform_4_occupied
    global headway
    global a
    global f
    global dataplot
    global n
    global baseLine_Load
    
    car_id = name
    
   
    server1 = Server(env, 1)
    server2 = Server(env,1)
    server3 = Server(env,1)

    run_time = 66.8
    car = Car(canvas, 600,165,700,185, name)
    car.move_car(-90, 0)
    yield env.timeout(run_time/3)
    baseLine_Load = server1.processingTime
    #pass to server 1
    car.move_car(-150, 0)
    yield env.timeout(run_time/3)
    if(server2.processingTime<=baseLine_Load):
        server2.process(car)
        processingTime.append(server2.processingTime)
        car.remove_car()
        
        
    else:
        car.move_car(-180, 0)
        yield env.timeout(run_time/3) 
        server3.process(car)
        processingTime.append(server3.processingTime)
        write_data(name, env.now, 'req', 'offload at server 2')
        car.remove_car()

        #yield env.process(road.dwell(name, "server 1"))
        #yield env.timeout(run_time/3) # complete run-in to server 

        #car.move_car(-250, 0)
        #yield env.process(road.dwell(name, "server 1"))
        #yield env.timeout(run_time/3)  #complete run-in to platform 1
        #car.remove_car()
    #car.move_car(-100, 50)
    #car.move_car(-100, 0)
    

    
        
     
    
    # setup for moving average headway calculation
    time.append(env.now) # recording the time for headway calculation
    print(time)
    n += 1
    car_number.append(n)

    headway = headway_analysis(time)
    print(np.mean(headway))
    moving_avg_headway.append(np.mean(headway))
    moving_stdev_headway.append(np.std(headway))
    print("====================")
    print("mean")
    print(np.mean(processingTime))
    if show_animation == True and hide_plots == False:
        a1.cla()
        a1.set_xlabel("Time")
        a1.set_ylabel("Processing Time")
        a1.plot(processingTime)

       
    
        dataPlot.draw()
        canvas.update()

        

# create the simulated world
def setup(env, num_servers, t_inter):
    """Create a termini, a number of initial trains and keep creating trains
    approx. every ``t_inter`` seconds."""
    # Create the termini
    road = Road(env, num_servers)
    
    # Create x initial trains
    for i in range(1):
        env.process(car(env, 'Car %d' % i, road))

    # Create more cars while the simulation is running
    while True:
        yield env.timeout(arrival_interval(t_inter))
        i += 1
        env.process(car(env, 'Car %d' % i, road))

def create_clock(env):
    clock = Clock(canvas, 500,250,700,300, env.now)
    while True:
        yield env.timeout(1)
        clock.tick(env.now)
        

# Setup and start the simulation
print('Termini Simulation')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
#env = simpy.Environment()

# Real time sim
env = simpy.rt.RealtimeEnvironment(factor = 0.01, strict = False)

# Start the process
env.process(setup(env, NUM_SERVERS, T_INTER))
env.process(create_clock(env))

# Execute!
env.run(until=SIM_TIME)

# keep display open
mainloop()


#####################################
### BELOW IS FOR POST PROCESSING OF RESULTS ###
#####################################
df = pd.DataFrame(output_dict)
df.to_csv('uxbridge_sim_output_raw.csv')

headway = headway_analysis(time)

# define print descriptive statistics function
def descriptive_stats(x, name):
	print("\nDescriptive Statistics for %s" % name)
	print("count = %d" % len(x))
	print("mean = %d" % np.mean(x))
	print("std = %d" % np.std(x))
	print("min = %d" % np.min(x))
	print("25%% = %d" % np.percentile(x, 25))
	print("50%% = %d" % np.percentile(x, 50))
	print("75%% = %d" % np.percentile(x, 75))
	print("max = %d" % np.max(x))
    #print("mean headway converts to %d TPH" % (3600.0/np.mean(x) descriptive_stats(headway, "Output Headway") # run descriptive stats function