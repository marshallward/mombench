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
effcy = {}

submodels = ['ocean', 'ice', 'coupler']
for p in prof_data:
    pdata = prof_data[p]
    wtime[p] = {}
    effcy[p] = {}

    for model in submodels:
        wdata = sorted([(n, pdata[n]['runtime'][model]) for n in pdata])
        ncpus_raw, wtime_raw = zip(*wdata)

        ncpus[p] = np.array(ncpus_raw)
        wtime[p][model] = np.array(wtime_raw)
        effcy[p][model] = ((ncpus[p][1] * wtime[p][model][1])
                         / (np.array(ncpus[p]) * np.array(wtime[p][model])))

# Wall time across platforms
fig, axes = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(8,9.5))

xticks = ncpus['12ppn']
xticks = np.insert(xticks, 1, 160)

for ax in axes:
    # Disable default ticks
    ax.tick_params(axis='x',
                   which='minor',
                   bottom='off',
                   top='off',
                   labelbottom='off')

    ax.set_xscale('log')
    ax.set_xlim(100, 2000)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks)

    ax.set_ylim(0., 1.1)

    ax.axhline(1.0, color='k', linestyle='--')
    ax.axhline(0.8, color='k', linestyle=':', linewidth=0.5)

axes[0].set_title('Scaling efficiency relative to 240 CPUs')
axes[1].set_ylabel('Scaling efficiency')
axes[2].set_xlabel('Number of CPUs')

ax_lines = []
titles = ['Default', 'Hyperthr.', '12 PPN', 'Ladder', 'Snake']
for (model, ax) in zip(submodels, axes):
    for p in ('raijin', 'ht', '12ppn', 'ladder', 'snake'):
        ax_l, = ax.plot(ncpus[p], effcy[p][model], marker='+')

        if ax == axes[0]:
            ax_lines.append(ax_l)

axes[0].legend(ax_lines, titles, loc='best')

plt.tight_layout()
plt.savefig('submodels.pdf')
#plt.show()
