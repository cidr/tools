import matplotlib
import numpy as np
matplotlib.use('PDF')  # save plots as PDF
font = {'size'   : 20}
matplotlib.rc('font', **font)

# use type 1 fonts
#matplotlib.rcParams['ps.useafm'] = True
#matplotlib.rcParams['pdf.use14corefonts'] = True
#matplotlib.rcParams['text.usetex'] = True

# use TrueType fonts
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42



import matplotlib.pyplot as plt
import numpy
from scipy.stats import cumfreq

def cdf_vals_from_data(data, numbins=None):

    # make sure data is a numpy array
    data = numpy.array(data)
    
    # by default, use numbins equal to number of distinct values
    if numbins == None:
        numbins = numpy.unique(data).size
    
    # bin the data and count each bin
    result = cumfreq(data, numbins, (data.min(), data.max()))
    cum_bin_counts = result[0]
    min_bin_val = result[1]
    bin_size = result[2]

    # normalize bin counts so rightmost count is 1
    cum_bin_counts /= cum_bin_counts.max()

    # make array of x-vals (lower end of each bin)
    x_vals = numpy.linspace(min_bin_val, min_bin_val+bin_size*numbins, numbins)

    # CDF always starts at (0, 0)
    cum_bin_counts = numpy.insert(cum_bin_counts, 0, 0)
    x_vals = numpy.insert(x_vals, 0, 0)


    return cum_bin_counts, x_vals

def autolabel(rects, ax):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

def plot(xs, ys, labels=None, xlabel=None, ylabel=None, title=None,\
         additional_ylabels=None, num_series_on_addl_y_axis=0,\
         axis_assignments=None,\
         xlabel_size=24, ylabel_size=24,\
         marker='o', linestyles=None, legend='best', show_legend=True,\
         legend_cols=1,\
         colors=None, axis=None, legend_text_size=20, filename=None,\
         xscale=None, yscale=None, type='series', bins=10, yerrs=None,\
         width_scale=1, height_scale=1,\
         bar_width=0.35, label_bars=False, bar_padding=0, **kwargs):
     # TODO: split series and hist into two different functions?
     # TODO: change label font size back to 20
     # TODO: clean up multiple axis stuff 

    #default_colors = ['b', 'g', 'r', 'c', 'm', 'y']
    default_colors = ['#348ABD', '#7A68A6', '#A60628', '#467821', '#CF4457', '#188487', '#E24A33']
    default_linestyles = ['-', '--', '-.', ':']
    
    fig, ax = plt.subplots()
    width, height = fig.get_size_inches()
    fig.set_size_inches(width*width_scale, height*height_scale)
    if xlabel: plt.xlabel(xlabel, fontsize=xlabel_size)
    if ylabel: plt.ylabel(ylabel, fontsize=ylabel_size)
    if title: plt.title(title)
    if axis: plt.axis(axis)
    if xscale: ax.set_xscale(xscale)
    if yscale: ax.set_yscale(yscale)
    lines = [None]*len(xs)

    show_legend = show_legend and labels != None
    if not labels: labels = ['']*len(xs)
    if not axis_assignments: axis_assignments = [0]*len(xs)
    if not colors:
        colors = []
        for i in range(len(xs)):
            colors.append(default_colors[i%len(default_colors)])
    else:
        for i in range(len(colors)):
            if isinstance(colors[i], int):
                colors[i] = default_colors[colors[i]]
    if not linestyles:
        linestyles = []
        for i in range(len(xs)):
            linestyles.append(default_linestyles[i%len(default_linestyles)])

    if type == 'series':
        for i in range(len(xs)):
            if axis_assignments[i] != 0: continue
            line, = plt.plot(xs[i], ys[i], linestyle=linestyles[i], marker=marker,\
                color=colors[i], label=labels[i], **kwargs)
            lines[i] = line
            if yerrs:
                plt.fill_between(xs[i], numpy.array(ys[i])+numpy.array(yerrs[i]),\
                numpy.array(ys[i])-numpy.array(yerrs[i]), color=colors[i], alpha=0.5)
    elif type == 'bar':
        color_squares = []
        for i in range(len(xs)):
            N = len(xs[i])
            ind = np.arange(N) + bar_padding
            rects = ax.bar(ind + i*bar_width, ys[i], bar_width)
            color_squares.append(rects[0])
            if label_bars: autolabel(rects, ax)
        ax.set_xticks(ind + len(xs)/2.0*bar_width)
        ax.set_xticklabels(xs[0], rotation=25)
        ax.set_xlim(0, ind[-1]+(len(xs))*bar_width+bar_padding)
        if labels: ax.legend(color_squares, labels)
    elif type == 'hist':
        plt.hist(xs, bins=bins, **kwargs)

    # Additional axes?
    if additional_ylabels:
        addl_y_axes = []
        for label in additional_ylabels:
            new_ax = ax.twinx()
            addl_y_axes.append(new_ax)
            new_ax.set_ylabel(label, fontsize=ylabel_size)

        # plot the extra series
        for i in range(len(xs)):
            # FIXME: index the correct addl y axis!
            if axis_assignments[i] != 1: continue
            line, = addl_y_axes[0].plot(xs[i], ys[i], linestyle=linestyles[i], marker=marker,\
                color=colors[i], label=labels[i], **kwargs)
            lines[i] = line
            if yerrs:
                plt.fill_between(xs[i], numpy.array(ys[i])+numpy.array(yerrs[i]),\
                numpy.array(ys[i])-numpy.array(yerrs[i]), color=colors[i], alpha=0.5)

    if show_legend and labels: 
        ax.legend(lines, labels, loc=legend, ncol=legend_cols, prop={'size':legend_text_size})
    else:
        ax.legend_ = None  # TODO: hacky

    # make sure no text is clipped along the boundaries
    plt.tight_layout()

    if filename == None:
        plt.show()
    else:
        plt.savefig(filename)

def cdf(data, numbins=None, **kwargs):
    '''Wrapper for making CDFs'''
    xs = []
    ys = []
    for d in data:
        y, x = cdf_vals_from_data(d, numbins)
        xs.append(x)
        ys.append(y)
    plot(xs, ys, ylabel='CDF', marker=None, **kwargs)
    



def main():

    # test cdf
    data = [1, 2, 3, 4, 5, 6]

    y_vals, x_vals = cdf_vals_from_data(data)
    plot(y_vals, x_vals, 'cdf')

if __name__ == '__main__':
    main()
