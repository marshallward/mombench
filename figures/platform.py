import matplotlib.pyplot as plt
import yaml

pdata_files = ['raijin.yaml',
               'ht.yaml',
               '12ppn.yaml',
               'ladder.yaml',
               'snake.yaml']

prof_data = {}
for fname in pdata_files:
    with open(fname) as pfile:
        prof_data[fname] = yaml.load(pfile)

wtime = []
for platform in prof_data:
    wtime.append(prof_data[platform][480]['runtime']['total'])

print(wtime)
