import matplotlib.pyplot as plt
import numpy as np
import yaml

pdata_files = ['raijin.yaml',
               'ht.yaml',
               '12ppn.yaml',
               'ladder.yaml',
               'snake.yaml']

platforms = [p.rstrip('.yaml') for p in pdata_files]

prof_data = {}
for platform, fname in zip(platforms, pdata_files):
    with open(fname) as pfile:
        prof_data[platform] = yaml.load(pfile)

# Remove the 3840 cpu job
prof_data['12ppn'].pop(3840)

ncpus = {}
wtime = {}
speedup = {}
effcy = {}
for p in prof_data:
    pdata = prof_data[p]
    wdata = sorted([(n, pdata[n]['runtime']['total']) for n in pdata])
    ncpus_raw, wtime_raw = zip(*wdata)

    ncpus[p] = np.array(ncpus_raw)
    wtime[p] = np.array(wtime_raw)
    speedup[p] = wtime[p][1] / np.array(wtime[p])
    effcy[p] = ((ncpus[p][1] * wtime[p][1])
                    / (np.array(ncpus[p]) * np.array(wtime[p])))

print(effcy)

# Wall time across platforms
fig_wt, ax_wt = plt.subplots()
fig_sp, ax_sp = plt.subplots()
fig_eff, ax_eff = plt.subplots()

xticks = ncpus['12ppn']
xticks = np.insert(xticks, 1, 160)

for ax in (ax_wt, ax_eff):
    ax.set_xscale('log')
    ax.set_xlim(100, 2000)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks)

ax_eff.set_title('Scaling efficiency relative to 240 CPUs')
ax_eff.set_ylim(0., 1.05)

ax_eff.axhline(1.0, color='k', linestyle='--')
ax_eff.axhline(0.8, color='k', linestyle=':', linewidth=0.5)

ax_data = {ax_wt: wtime,
           ax_sp: speedup,
           ax_eff: effcy}
ax_lines = {ax_wt: [],
            ax_sp: [],
            ax_eff: []}

titles = ['Default', 'Hyperthr.', '12 PPN', 'Ladder', 'Snake']
for ax in (ax_wt, ax_sp, ax_eff):
    for p in ('raijin', 'ht', '12ppn', 'ladder', 'snake'):
        ax_l, = ax.plot(ncpus[p], ax_data[ax][p], marker='+')
        ax_lines[ax].append(ax_l)

    ax.legend(ax_lines[ax], titles, loc='best')

plt.show()
