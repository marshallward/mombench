import matplotlib.pyplot as plt
import numpy as np
import yaml

f_raijin = 2.601e9
f_fujin = 1.848e9

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

wtimes = np.array([prof_data[p][480]['runtime']['ocean'] for p in platforms])
pcomm = np.array([prof_data[p][480]['mpi']['mean'] for p in platforms])

cycles = np.empty(wtimes.shape)
cycles[:3] = f_raijin * wtimes[:3]
cycles[3:] = f_fujin * wtimes[3:]

calcs = (1. - pcomm) * cycles

# Wall time across platforms
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6.5,7))

rect_set = {}

r1_x86 = ax1.bar(range(3), wtimes[:3], color='b', align='center')
r1_fx10 = ax1.bar(range(3, 5), wtimes[3:], color='r', align='center')
rect_set[ax1] = (r1_x86, r1_fx10)

r2_x86 = ax2.bar(range(3), calcs[:3], color='b', align='center')
r2_fx10 = ax2.bar(range(3, 5), calcs[3:], color='r', align='center')
rect_set[ax2] = (r2_x86, r2_fx10)

ax1.set_title('Walltime on 480 CPUs across hardware configurations')
ax2.set_title('Weighted ocean submodel instruction count')

ax1.set_ylabel('Walltime (s)')
ax2.set_ylabel('Instruction count')

ax1.set_yticks(np.linspace(0., 2000., 5))
ax2.set_ylim(0., 3.2e12)

# X axis is shared
ax1.set_xticks(range(5))
ax1.set_xticklabels(('Default', 'Hyperthr.', '12 PPN', 'Ladder', 'Snake'))

v_fmt = {ax1: '{:.1f}',
         ax2: '{:.1e}'}

for ax in (ax1, ax2):
    for rset in rect_set[ax]:
        for rect in rset:
            val = rect.get_height()
            v_x = rect.get_x() + rect.get_width() / 2.
            v_y = 1.01 * val

            ax.text(v_x, v_y, v_fmt[ax].format(val), ha='center', va='bottom')

ax1.legend((r2_x86[0], r2_fx10[0]), ('Raijin', 'Fujin'), loc='best')

plt.tight_layout()
plt.savefig('platforms.pdf', bbox_inches='tight')
