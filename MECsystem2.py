from functools import partial, wraps
import simpy
import random
import statistics
from collections import namedtuple

wait_times = []
users = []
observedProcessingTime = []
#Create a class that represents a server
#Each object will have a simpy object, a resource
#The object has a processing task that take a user and generate random number for delay
class MECServer(object):
    def __init__(self, env, num_vm):
        self.env = env
        self.server = simpy.Resource(env, num_vm)
        self.data = []
        self.processing_time = namedtuple('user', 'task_processing_time')

    #The object has a processing task that take a user and generate random number for delay
    def processing_task(self, user):
        task_processing_time = random.randint(1, 10)
        self.processing_time = (user, task_processing_time)
        yield self.env.timeout(task_processing_time)
    

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
#This function represts a user pass by a server and process a task
#It takes a simpy object, a user and mecServer
def pass_by_server(env, user, mecServer):
    arrival_time = env.now

    with mecServer.server.request() as request:
        mecServer.data.append(len(mecServer.server.queue))
        yield request
        yield env.process(mecServer.processing_task(user))
        mecServer.data.append(len(mecServer.server.queue))
    
    wait_times.append(env.now - arrival_time)


#This function is the real simulation 
def run_mecServer(env, numOfserver):
    #Create a list of servers
    serverList = []
    for i in range(numOfserver):
        x = MECServer(env, 1)
        serverList.append(x)

    #serverId = 1
    #The users starting from user number 0
    user = 0
    #user number 1 will be the user I care about. The other users are only to generate load to servers
    myUser = 1
    #for user in range(2):
        #env.process(pass_by_server(env, user, firstServer))
        #observedProcessingTime.append(firstServer.processing_time)
    print("The number of servers")
    print(len(serverList))
    while True:
        for server in range(len(serverList)):
            yield env.timeout(1)  # Wait a bit before generating a new request
            print("A user is offloading: ")
            user += 2
            print(user)
            print("at server number: ")
            print(server)
            print("start at ")
            arrival = env.now
            print(arrival)
            #The user passes by server and request to process a task
            env.process(pass_by_server(env, user, serverList[server]))
            #I use the variable: if it is 1, myuser will pass by a server, otherwise nothing happens
            decission = random.randint(1,2)
            print("Number of Queue")
            print(len(serverList[server].data))
            if(decission==1):
                print('My user is offloading')
                print(myUser)
                print("at server number: ")
                print(server)
                print("start at ")
                arrival = env.now
                print(arrival)
                env.process(pass_by_server(env,  myUser, serverList[server]))
                print("waiting Time ")
                print(env.now-arrival)
            observedProcessingTime.append(serverList[server].processing_time)
            print("Number of Queue")
            print(len(serverList[server].data))
            #monitor = partial(monitor, data)
            #patch_resource(serverList[server], post=partial(monitor, data))
        
        

def get_average_wait_time(wait_times):
    average_wait = statistics.mean(wait_times)
    # Pretty print the results
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)


    
def get_user_input():
    num_vm= input("Input # of server: ")
    params = num_vm
    return params


def main():
  # Setup
  random.seed(42)
  num_server = get_user_input()

  # Run the simulation
  env = simpy.Environment()
  env.process(run_mecServer(env, num_server))
  env.run(until=5)

  # View the results
  mins, secs = get_average_wait_time(wait_times)
  #print('minutes')
  #print('second')
  print(mins)
  print(secs)
  print(wait_times)
  print("observed Processing Time")
  print(len(observedProcessingTime))
  print(observedProcessingTime)
if __name__ == "__main__":
    main()
        