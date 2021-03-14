import random
import math
from datetime import datetime

# generate random numbers in the right format
def random_generator():
    rand_list_of_tuples = []  # list of tuples is the accepted format
    for num in range(0, 10):
        # we use this to convert the random number to tuple (int -> list -> tuple)
        rand_list_of_tuples.append(tuple([math.floor(random.random() * 10000), datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')]))
    print(rand_list_of_tuples)
    return rand_list_of_tuples
