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
import csv
import xlsxwriter
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
   
    def __init__(self, env, num_vm, id):
        self.env = env
        self.server = simpy.Resource(env, num_vm)
        self.processingTime = np.random.normal(50, 10, 1)
        self.id = id
        self.queueLength = len(self.server.queue)

    def process(self, car):
        yield self.env.timeout(self.processingTime)
    
   

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
    canvas.create_rectangle(50, 100, 100, 150, fill = "yellow")
    canvas.create_rectangle(150, 100, 200, 150, fill = "yellow")
    canvas.create_rectangle(250, 100, 300, 150, fill = "yellow")
    canvas.create_rectangle(350, 100, 400, 150, fill = "yellow")
    canvas.create_rectangle(450, 100, 500, 150, fill = "yellow")
    canvas.create_rectangle(550, 100, 600, 150, fill = "yellow")
    canvas.create_rectangle(650, 100, 700, 150, fill = "yellow")

    canvas.create_line(50, 75, 200, 75, fill="green", width=3) # platform 4
    canvas.create_line(50, 175, 200, 175, fill="green", width=3) # platform 2/3
    #canvas.create_line(50, 275, 200, 275, fill="green", width=3) # platform 1

    canvas.create_text(75, 125, text = "S7")
    canvas.create_text(175, 125, text = "S6")
    canvas.create_text(275, 125, text = "S5")
    canvas.create_text(375, 125, text = "S4")
    canvas.create_text(475, 125, text = "S3")
    canvas.create_text(575, 125, text = "S2")
    canvas.create_text(675, 125, text = "S1")
    #canvas.create_text(125, 210, text = "Platform 2")
    #canvas.create_text(125, 240, text = "Platform 1")

# track
    canvas.create_line(200, 75, 800, 75, fill="green", width=3) # platform 4 run out
    canvas.create_line(200, 175, 800, 175, fill="green", width=3) # platform 2/3 run in
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
NUM_SERVERS = 7  # Number of platforms in the termini (needs to match how many platforms are initially set to "False" occupancy

# setting up empty lists to store results in
time = []
headway = []
moving_avg_headway = []
moving_stdev_headway = []
car_number = []
processingTime = []
waiting_time = []
simulationInformation = [("Car Id", "Requesting Time", "Accessing Time", "Finishing Time","serverProcessingTime", "Waiting time", "NumofUsers","ServerId")]
n = 0
observedDelay = []
# set up general parameters
RANDOM_SEED = 45
T_INTER = 5 # Arrival headway: create a car on average every T_INTER seconds, setting this to "1" is a reasonable approximation to "as fast as possible" without slowing down the simulation
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
def car(env, name):
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
    global server4
    global server5
    global server6
    global server7
    global baseLine_Load 
    #global platform_4_occupied
    global headway
    global a
    global f
    global dataplot
    global n
    global baseLine_Load 
    global d
    global arrival_time


   
    
    car_id = name
    
    
    server1 =  Server(env,1,1)
    server2 =  Server(env,1,2)
    server3 =  Server(env,1,3)
    server4 =  Server(env,1,4)
    server5 =  Server(env,1,5)

    baseLine_Load = 50
    


    run_time = 66.8
    car = Car(canvas, 800,165,750,185, name)
    yield env.timeout(run_time/3)
    #move to server 2
    car.move_car(-145, 0)
    arrival_time = env.now
    print("Queu length before getting into")
    print(len(server1.server.queue))
    if(len(server1.server.queue) ==0):
        print("server queue length")
        print(len(server1.server.queue))
        with server1.server.request() as request:
            print(f'{name} requesting at {env.now}')
            requestingTime = env.now
            yield request
            serverStatus = len(server1.server.queue)
            print(f'{name} got resource at {env.now}')
            gettingTime = env.now
            yield env.process(server1.process(car))
            print("server queue length")
            print(len(server1.server.queue))
            serverProcessingTime = server1.processingTime
            processDuration =  env.now - gettingTime
            car.remove_car()
            server = server1.id
            waiting_time.append(gettingTime - requestingTime)
            waiting_time2 = gettingTime- requestingTime
            simulationInformation.append((car_id, requestingTime, gettingTime, env.now, serverProcessingTime ,processDuration ,waiting_time2, serverStatus, server))
    elif(len(server2.server.queue) ==0):
        print("server queue length")
        print(len(server2.server.queue))
        with server2.server.request() as request:
            print(f'{name} requesting at {env.now}')
            requestingTime = env.now
            yield request
            serverStatus = len(server2.server.queue)
            print(f'{name} got resource at {env.now}')
            gettingTime = env.now
            yield env.process(server2.process(car))
            serverProcessingTime = server2.processingTime
            processDuration =  env.now - gettingTime
            car.remove_car()
            server = server2.id
            waiting_time.append(gettingTime - requestingTime)
            waiting_time2 = gettingTime- requestingTime
            simulationInformation.append((car_id, requestingTime, gettingTime, env.now, serverProcessingTime ,processDuration ,waiting_time2, serverStatus, server))
    elif(len(server3.server.queue) ==0):
        print("server queue length")
        print(len(server3.server.queue))
        #pass to server 3
        car.move_car(-150, 0)
        with server3.server.request() as request:
            print(f'{name} requesting at {env.now}')
            requestingTime = env.now
            yield request
            serverStatus = len(server3.server.queue)
            print(f'{name} got resource at {env.now}')
            gettingTime = env.now
            yield env.process(server3.process(car))
            serverProcessingTime = server3.processingTime
            processDuration = gettingTime - env.now
            car.remove_car()
            server = server3.id
            waiting_time.append(gettingTime - requestingTime)
            waiting_time2 = gettingTime- requestingTime
            simulationInformation.append((car_id, requestingTime, gettingTime, env.now, serverProcessingTime ,processDuration ,waiting_time2, serverStatus, server))
    elif(len(server4.server.queue) ==0):
        #pass to server 4
        print("server queue length")
        print(len(server4.server.queue))
        car.move_car(-250, 0)
        with server4.server.request() as request:
            print(f'{name} requesting at {env.now}')
            requestingTime = env.now
            yield request
            serverStatus = len(server4.server.queue)
            print(f'{name} got resource at {env.now}')
            gettingTime = env.now
            yield env.process(server4.process(car))
            serverProcessingTime = server4.processingTime
            processDuration = gettingTime - env.now
            car.remove_car()
            server = server4.id
            waiting_time.append(gettingTime - requestingTime)
            waiting_time2 = gettingTime- requestingTime
            simulationInformation.append((car_id,requestingTime, gettingTime, env.now, serverProcessingTime ,processDuration ,waiting_time2, serverStatus, server))
    else:
        #pass to server 5
        print("server queue length")
        print(len(server4.server.queue))
        car.move_car(-350, 0)
        with server5.server.request() as request:
            print(f'{name} requesting at {env.now}')
            requestingTime = env.now
            yield request
            serverStatus = len(server5.server.queue)
            print(f'{name} got resource at {env.now}')
            gettingTime = env.now
            yield env.process(server5.process(car))
            serverProcessingTime = server5.processingTime
            processDuration = gettingTime - env.now
            car.remove_car()
            server = server5.id
            waiting_time.append(gettingTime - requestingTime)
            waiting_time2 = gettingTime- requestingTime
            simulationInformation.append((car_id,requestingTime, gettingTime, env.now, serverProcessingTime ,processDuration ,waiting_time2, serverStatus, server))

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
    #simulationInformation.append(env.now)
    #print(simulationInformation)
    headway = headway_analysis(time)
    #print(np.mean(headway))
    #print(observedDelay)
    with open("out.csv", mode="w", newline="\n") as f:
        writer = csv.writer(f)
        for car in simulationInformation:
            writer.writerow([[car]])
       
    moving_avg_headway.append(np.mean(headway))
    moving_stdev_headway.append(np.std(headway))
    #print("====================")
    #print("mean")
    #print(np.mean(processingTime))
    if show_animation == True and hide_plots == False:
        a1.cla()
        a1.set_xlabel("Time")
        a1.set_ylabel("waiting Time")
        a1.plot(waiting_time)

       
    
        dataPlot.draw()
        canvas.update()

        

# create the simulated world
def setup(env, t_inter):
    #road = Road(env, num_servers)
    # Create x initial cars
    #for i in range(1):
       # env.process(car(env, 'Car %d' % i, road))
        

    # Create more cars while the simulation is running
    #while True:
    # Create more cars while the simulation is running
    
    yield env.timeout(arrival_interval(t_inter))
    env.process(car(env, 1))
    yield env.timeout(arrival_interval(t_inter))
    env.process(car(env, 2)) 
    yield env.timeout(arrival_interval(t_inter))
    env.process(car(env, 3))
    yield env.timeout(arrival_interval(t_inter))
    env.process(car(env, 4))
    yield env.timeout(arrival_interval(t_inter))
    env.process(car(env, 5))
    yield env.timeout(arrival_interval(t_inter))
    env.process(car(env, 6))  
    yield env.timeout(arrival_interval(t_inter))
    env.process(car(env, 7))
    yield env.timeout(arrival_interval(t_inter))
    env.process(car(env, 8))
    yield env.timeout(arrival_interval(t_inter))
    env.process(car(env, 9))
    yield env.timeout(arrival_interval(t_inter))
    env.process(car(env, 10))
    yield env.timeout(arrival_interval(t_inter))
    env.process(car(env, 11))
    yield env.timeout(arrival_interval(t_inter))
    env.process(car(env, 12))


    for i in range(1):
        env.process(car(env, 'Car %d' % i))
    while True:
        yield env.timeout(arrival_interval(t_inter))
        i += 1
        env.process(car(env, 'Car %d' % i))
    


def create_clock(env):
    clock = Clock(canvas, 500,250,700,300, env.now)
    while True:
        yield env.timeout(1)
        clock.tick(env.now)
        


random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
#env = simpy.Environment()

# Real time sim
env = simpy.rt.RealtimeEnvironment(factor = 0.01, strict = False)

# Start the process
env.process(setup(env, T_INTER))
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