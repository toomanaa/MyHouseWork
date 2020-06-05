import simpy
import random
import itertools
T_INTER = [20, 30] 
T_INTER2 = [2,5] 

def offloading_data(name, env, resource):
    print('Name of user:')
    print(name)
    print('request for offloading')
    print(env.now)
    request = resource.request()
    print('Name of user:')
    print(name)
    print('waiting for admission')
    print(env.now)
    yield request
    print('Name of user:')
    print(name)
    print('waiting for processing')
    print(env.now)
    yield env.timeout(1)
    print(name)
    print('Done at')
    print(env.now)
    resource.release(request)


def car_generator(env, server):
    """Generate new cars that arrive at the gas station."""
    print('new car arrives ')
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        env.process(offloading_data('Car %d' % i, env, server))




def server_generator(env ,capacity):
    """Generate new server that the user passes by ."""
    print('new server shows up ')
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER2))
        env.process(env,i, simpy.Resource(env, capacity=capacity))

env = simpy.Environment()
res = simpy.Resource(env, capacity=2)
env.process(car_generator(env, res))
env.run(until=100)
