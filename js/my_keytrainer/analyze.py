from collections import defaultdict
from operator import itemgetter

import matplotlib.pyplot as plt

with open('keystrokes_full') as ff:
    lines = ff.readlines()

data = []
for l in lines:
    need, pressed, time = l.split(':')
    data += [
        dict(need=need, pressed=pressed, time=float(time))
    ]

counts = defaultdict(int)
all_keys = 'йцукенгшщзхъфывапролджэячсмитьбю'
for k in all_keys:
    counts[k] = 0

for d in data:
    need = d['need']
    if need != d['pressed']:
        counts[need] += 1

print(sorted(counts.items(), key=itemgetter(1), reverse=True))