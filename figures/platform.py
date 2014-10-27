import matplotlib.pyplot as plt
import yaml

f_raijin = 2601e6
f_fujin = 1848e6

pdata_files = ['raijin.yaml',
               'ht.yaml',
               '12ppn.yaml',
               'ladder.yaml',
               'snake.yaml']

platforms = [p.rstrip('.yaml') for p in pdata_files]

prof_data = {}
for plat, fname in zip(platforms, pdata_files):
    with open(fname) as pfile:
        prof_data[plat] = yaml.load(pfile)

wtime = {}
for plat in platforms:
    wtime[plat] = prof_data[plat][480]['runtime']['total']

wtimes = [wtime[p] for p in platforms]
cycles = [f_raijin * wtime[p] for p in platforms[:3]] \
        + [f_fujin * wtime[p] for p in platforms[3:]]

for i in range(5):
    print(platforms[i], cycles[i] * 1e-9)
