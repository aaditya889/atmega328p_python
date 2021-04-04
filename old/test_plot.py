import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import random

# Globals
FD1_DATA = [0] * 20
FD2_DATA = [0] * 20

# Fermi-Dirac Distribution
def fermi(E: float, E_f: float, T: float) -> float:
    k_b = 8.617 * (10**-5) # eV/K
    return 1/(np.exp((E - E_f)/(k_b * T)) + 1)

# General plot parameters
mpl.rcParams['font.family'] = 'Avenir'
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['xtick.major.size'] = 10
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['ytick.major.size'] = 10
mpl.rcParams['ytick.major.width'] = 2

# Create figure and add axes
# fig = plt.figure(figsize=(10, 5))
# fig2 = plt.figure(figsize=(10, 5))
fig, axs = plt.subplots(2, sharex=True)
# ax = fig.add_subplot()
ax = axs[0]
ax2 = axs[1]
# plt.axis([0, 20, 0, 100])
ax.set_xlim(0,20)
ax2.set_xlim(0,20)
ax.set_ylim(0,100)
ax2.set_ylim(0,100)
ax.grid(True)
ax2.grid(True)
# plt.xticks(np.linspace(0, 1, 10))
# plt.yticks(np.linspace(0, 1.05, 10))

# fig, ax = plt.subplots(25,4,figsize=(14,98))
# Temperature values
T = np.linspace(100, 1000, 10)

# Get colors from coolwarm colormap
colors = plt.get_cmap('coolwarm', 100)

# Plot F-D data
# for i in range(len(T)):
#     x = np.linspace(0, 1, 100)
#     y = fermi(x, 0.5, T[i])
#     ax.plot(x, y, color=colors(i), linewidth=2.0)

# # Add legend
# labels = ['100 K', '200 K', '300 K', '400 K', '500 K', '600 K', 
#           '700 K', '800 K', '900 K', '1000 K']
# ax.legend(labels, bbox_to_anchor=(0.8, 0.5), loc='lower left', 
#           frameon=False, labelspacing=0.2)

# x = np.linspace(0, 1, 100)
# y = fermi(x, 0.5, 500)
# print(x)
# print(y)
# Create variable reference to plot
# f_d, = ax.plot(x, y, linewidth=2.5)
f_d_1, = ax.plot([], [], linewidth=1.5)
f_d_2, = ax.plot([], [], linewidth=1.5)
f_d_1.set_color('red')
f_d_2.set_color('green')

# Add text annotation and create variable reference
# temp = ax.text(1, 1, '', ha='right', va='top', fontsize=10)


def gen():
  # if FD1_DATA[0] != 0:
  #   return
  FD1_DATA.extend([random.randint(0, 100)])
  del FD1_DATA[0]
  FD2_DATA.extend([random.randint(0, 100)])
  del FD2_DATA[0]

def gen2():
  # if FD1_DATA[0] != 0:
  #   return
  FD2_DATA.extend([random.randint(0, 100)])
  del FD2_DATA[0]

# Animation function
def animate(i):
  # print("Calling")
  x = np.linspace(0, 20, 20)
  # y = fermi(x, 0.5, T[i])
  gen()
  f_d_1.set_data(x, FD1_DATA)
  f_d_2.set_data(x, FD2_DATA)
  # f_d_1.set_color(colors(i))
  # temp.set_text(str(int(T[i])) + ' K')
  # temp.set_color(colors(i))
  # ax.axis([i, i+0.1, 0, 1])
  # fig.canvas.draw_idle()
  # fig.canvas.draw()
  # plt.tight_layout()



def animate_2(i):
  gen2()
  x = np.linspace(0, 20, 20)
  f_d_2.set_data(x, FD2_DATA)

# Create animation
ani = FuncAnimation(fig=fig, func=animate, frames=range(len(T)), interval=1, repeat=True)
# ani_2 = FuncAnimation(fig=fig, func=animate_2, frames=range(len(T)), interval=500, repeat=True)

plt.show()
