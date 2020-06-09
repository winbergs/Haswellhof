import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

import seaborn as sns
sns.set()

default_colors = sns.color_palette().as_hex()
colors = [default_colors[0], default_colors[1], default_colors[3]] 

def my_xticks(x,pos):
    exponent = np.log2(x)
    if exponent < 0.0:
        value = int(2**(-exponent))
        return r'$1 / {den:2d}$'.format(den=value)
    else:
        value = int(2**(exponent))
        return r'${{ {:2d} }}$'.format(value)

def my_yticks(y,pos):
    return r'${{ {:.1f} }}$'.format(y)

# Name of output file to save the plot to
outputFileName = 'performance_plot.png'

source_folder = 'performance_sebastian'

# Name of input files with performance data, etc.
inputFileNames = [
    os.path.join(source_folder,'compute_integral_img.csv'), 
    os.path.join(source_folder,'compute_response_layer.csv'),
    #os.path.join(source_folder,'get_interest_points.csv'),
    os.path.join(source_folder,'get_msurf_descriptors.csv'),

    os.path.join(source_folder,'compute_integral_img_faster_alg.csv'),
    os.path.join(source_folder,'compute_response_layers_Dyy_laplacian.csv'),
    os.path.join(source_folder,'get_msurf_descriptors_simd_2_24.csv'),

    os.path.join(source_folder,'compute_padded_integral_img_faster_alg.csv'), 
    os.path.join(source_folder,'compute_response_layers_sonic_Dyy_unconditional_opt.csv'),
    os.path.join(source_folder,'get_msurf_descriptors_simd_2_24_unconditional.csv')
]

# Name of labels
plotLabels = [
    '$\mathtt{ (b) iimage }$', 
    '$\mathtt{ (b) response }$',
    '$\mathtt{ (b) descriptors }$',
    '$\mathtt{ (o) iimage }$',
    '$\mathtt{ (o) response }$',
    '$\mathtt{ (o) descriptors }$',
    '$\mathtt{ (op) iimage }$',
    '$\mathtt{ (op) response }$',
    '$\mathtt{ (op) descriptors }$'
]

labelOffset = [
    (0.05, 0.0),
    (0.05, -0.15),
    (0.05, 0.05),
    (0.05, -0.025),
    (0.05, 0.15),
    (0.05, 0.0),
    (0.05, 0.01),
    (0.05, -0.025),
    (0.05, 0.0)   
]

markers = ['o', '^', '*']

# Getting current axis
ax = plt.gca()

# Initializing plot title
plt.title('SURF Program Performance Plot',  x=-0.1, y=1.05, ha='left', fontsize=16, fontweight='bold')

# Initializing plot axis labels
plt.xlabel('image size', fontsize=10)
yl = plt.ylabel('[flops/cycle]', fontsize=10, ha='left')
yl.set_rotation(0)
ax.yaxis.set_label_coords(-0.1, 1.01)

# Setting x-axis to be log axis
plt.xscale('log')
#plt.yscale('log')


# Initializing and setting axis ticks
ticks_x = []
for i in range(8, 12):
    ticks_x.append(2**(i))
ticks_y = [0, 0.5, 1, 1.5]

plt.xticks(ticks_x, va='center')
plt.yticks(ticks_y)

# Setting x and y limits (min, max)
plt.xlim(ticks_x[0] / 1.3, ticks_x[len(ticks_x) - 1] * 1.7)
plt.ylim(ticks_y[0] - 0.1, ticks_y[len(ticks_y) - 1] + 0.3)
#plt.ylim(ticks_y[0] / 2.0, ticks_y[len(ticks_y) - 1] * 2.0)

# Setting axis ticks formatter
ax.xaxis.set_major_formatter(ticker.FuncFormatter(my_xticks))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(my_yticks))

# Setting label size
ax.tick_params(axis='both', which='major', labelsize=8)

# Iterating through all input files and plotting each as a line
for i in range(0, len(inputFileNames)):

    substrings = inputFileNames[i].split('.')

    # Getting function name from file name
    functionName = substrings[0]

    # Reading csv data from input file 
    data = np.genfromtxt(inputFileNames[i], delimiter=',')

    # Getting width, height, number of interest points, average/min/max cycles, flops per cycles
    imageName = data[:, 0]
    width = data[:, 1]
    height = data[:, 2]
    num_interest_points = data[:, 3]
    num_flops = data[:, 4]
    avg_cycles = data[:, 5]
    min_cycles = data[:, 6]
    max_cycles = data[:, 7]
    flops_per_cycles = num_flops / avg_cycles

    print("Flops per cycles:")
    print(num_flops / avg_cycles)

    labelPos = (width[-1]  * (1.0 + labelOffset[i][0]), flops_per_cycles[-1] * (1.0 + labelOffset[i][1]))

    # Plotting  flops per cycles performance
    plt.plot(width, flops_per_cycles, label=plotLabels[i], color=colors[i % 3], marker=markers[i // 3])
    ax.annotate(plotLabels[i], xy=labelPos, va='center', fontsize=6)

# Adding legend to plot
#plt.legend()

# Saving plot to file
plt.savefig(outputFileName, dpi=300)
