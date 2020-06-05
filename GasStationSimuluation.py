"""
Gas Station Refueling example

Covers:

- Resources: Resource
- Resources: Container
- Waiting for other processes

Scenario:
  A gas station has a limited number of gas pumps that share a common
  fuel reservoir. Cars randomly arrive at the gas station, request one
  of the fuel pumps and start refueling from that reservoir.

  A gas station control process observes the gas station's fuel level
  and calls a tank truck for refueling if the station's level drops
  below a threshold.

"""
import itertools
import random
import numpy as np
import simpy


RANDOM_SEED = 42
GAS_STATION_SIZE = 200     # liters
THRESHOLD = 2            # Threshold for calling the tank truck (in %)
FUEL_TANK_SIZE = 50        # liters
COMPUTING_CAPACITY = 100    #the computation capacity (i.e., CPU cycles per unit time) of device n at time t.
REQIRED_CAPACITY = [1, 6]
PROCESSING_SPEED = 2        # bits / second
TANK_TRUCK_TIME = 300      # Seconds it takes the tank truck to arrive
T_INTER = [1, 2]        # Create a car every [min, max] seconds
SIM_TIME = 10       # Simulation time in seconds



class Server(object):
    def __init__(self, env, cpu):
        self.env = env
        self.server = simpy.Resource(env, 1)
        self.cpu = simpy.Container(env, 2, init=2)

        


def car(name, env, server, cpu):
    """A car passes by a server for offloading.

    It requests one of the server's vm and tries to offload. If the server is
    busy, the car has to wait in the queue.

    """
    print('%s arriving at server at %.1f' % (name, env.now))
    arrival_time = env.now
    print("Check the level of the load")
    
    print(cpu.level)
    print(cpu.capacity)
    with server.request() as req:
        start = env.now
        # Request one of the vm
        yield req
        start = env.now
        yield cpu.get(2)
        reqired_CPU_CYC = np.random.normal(50,10,1)
        print('%s requires  %.1f' % (name, reqired_CPU_CYC))
        # The "actual" task process takes some time
        yield env.timeout(reqired_CPU_CYC)

        print('%s finished processing in %.1f seconds.' % (name,
                                                          env.now - start))
        

        



def car_generator(env, name ,server, cpu):
    """Generate new cars that passes by a server."""
    yield env.timeout(random.randint(*T_INTER))
    env.process(car('Car %d' % name, env, server, cpu))

def server_generator(env, cpu):
    """Generate new cars that passes by a server."""
    yield env.timeout(random.randint(*T_INTER))
    server = Server(env, cpu)

def offload_control(env, name, server, cpu):
    """Periodically check the level of the *fuel_pump* and call the tank
    truck if the level falls below a threshold."""
    while True:
        if cpu.level / cpu.capacity * 100 < 15:
            # We need to find better server!
            print('Calling tank truck at %d' % env.now)
            # Wait for till a mec server
            yield env.process(car_generator(env, name ,server, cpu))

        yield env.timeout(10)  # Check every 10 seconds

# Setup and start the simulation
print('Deploying servers')
random.seed(RANDOM_SEED)

env = simpy.Environment()
cpu = simpy.Container(env, 2, init=2)
server1 = Server(env, cpu)
server2 = Server(env, cpu)
# Create environment and start processes

env.process(car_generator(env, 1, server1.server,server1.cpu))
env.process(car_generator(env, 2, server1.server,server1.cpu))
env.process(car_generator(env, 3, server1.server,server1.cpu))

env.process(car_generator(env, 4, server1.server,server1.cpu))
# Execute!
env.run(100)