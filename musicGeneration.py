# Authors: Shane Moon
# Software Design
# InvadingTheRealmOfTheArts
# April 28, 2010
# File: musicGeneration.py

import sys
import random
import string


def random_times(notes, beat = 48):
    """
        Generate random <list> of <time>s,
        whose total length is the same length of the <list> 'notes.'
    """
    half_beat = beat / 2
    times = [0]
    for i in range(1, len(notes)):
        current_time = times[i-1]
        times.append(current_time + half_beat * random.choice([1,2]))
    
    return times



def constant_times(notes, duration, beat = 48):
    """
        Generate constant <list> of <time>s,
        whose total length is the same length of the <list> 'notes.'
    """
    half_beat = beat / 2
    times = [0]

    for i in range(1, len(notes)):
        current_time = times[i-1]
        times.append(current_time + half_beat * duration)
    return times

