import matplotlib  # TODO :needed?
import numpy as np # import needed?
matplotlib.use('PDF')  # save plots as PDF
font = {'size': 20,
}
        #'serif': 'Times New Roman',
        #'family': 'serif'}
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

def subplots(num_row, num_col, width_scale=1, height_scale=1):
    # TODO: anything helpful we could do here?
    fig, ax_array = plt.subplots(num_row, num_col)
    width, height = fig.get_size_inches()
    fig.set_size_inches(width*width_scale, height*height_scale)
    return fig, ax_array

def save_plot(filename):
    #plt.tight_layout()
    plt.savefig(filename)

def plot(xs, ys, labels=None, xlabel=None, ylabel=None, title=None,\
         additional_ylabels=None, num_series_on_addl_y_axis=0,\
         axis_assignments=None, additional_ylims=None,\
         xlabel_size=20, ylabel_size=20, labelspacing=0.2, handletextpad=0.5,\
         marker='o', linestyles=None, legend='best', show_legend=True,\
         legend_cols=1, linewidths=None, legend_border=False,\
         colors=None, axis=None, legend_text_size=20, filename=None,\
         xscale=None, yscale=None, type='series', bins=10, yerrs=None,\
         width_scale=1, height_scale=1, xlim=None, ylim=None,\
         bar_width=0.35, label_bars=False, bar_padding=0,\
         show_y_tick_labels=True, show_x_tick_labels=True,\
         fig=None, ax=None,\
         **kwargs):
     # TODO: split series and hist into two different functions?
     # TODO: change label font size back to 20
     # TODO: clean up multiple axis stuff 
     # TODO: legend loc, replace 'bottom' with lower and 'top' with 'upper'
     # TODO: what is the default labelspacing?

    default_colors = ['b', 'g', 'r', 'c', 'm', 'y']
    #default_colors = ['#348ABD', '#7A68A6', '#A60628', '#467821', '#CF4457', '#188487', '#E24A33']
    default_linestyles = ['-', '--', '-.', ':']
    
    # if we want to do subplots, caller may have passed in an existing figure
    if not fig or not ax:
        fig, ax = plt.subplots()
        width, height = fig.get_size_inches()
        fig.set_size_inches(width*width_scale, height*height_scale)

    if xlabel: ax.set_xlabel(xlabel, fontsize=xlabel_size)
    if ylabel: ax.set_ylabel(ylabel, fontsize=ylabel_size)
    if not show_x_tick_labels: ax.set_xticklabels([])
    if not show_y_tick_labels: ax.set_yticklabels([])
    if title: ax.set_title(title)
    if axis: 
        ax.set_xlim(axis[0:2])
        ax.set_ylim(axis[2:4])
    if xscale: ax.set_xscale(xscale)
    if yscale: ax.set_yscale(yscale)
    if xlim: ax.set_xlim(xlim)
    if ylim: ax.set_ylim(ylim)
    lines = [None]*len(ys)

    show_legend = show_legend and labels != None
    if not labels: labels = ['']*len(ys)
    if not linewidths: linewidths = [3]*len(ys)
    if not axis_assignments: axis_assignments = [0]*len(ys)
    if not colors:
        colors = []
        for i in range(len(ys)):
            colors.append(default_colors[i%len(default_colors)])
    else:
        for i in range(len(colors)):
            if isinstance(colors[i], int):
                colors[i] = default_colors[colors[i]]
    if not linestyles:
        linestyles = []
        for i in range(len(ys)):
            linestyles.append(default_linestyles[i%len(default_linestyles)])

    if type == 'series':
        for i in range(len(ys)):
            if axis_assignments[i] != 0: continue
            line, = ax.plot(xs[i], ys[i], linestyle=linestyles[i], marker=marker,\
                linewidth=linewidths[i], color=colors[i], label=labels[i], **kwargs)
            lines[i] = line
            if yerrs:
                ax.fill_between(xs[i], numpy.array(ys[i])+numpy.array(yerrs[i]),\
                numpy.array(ys[i])-numpy.array(yerrs[i]), color=colors[i], alpha=0.5)
    elif type == 'bar':
        color_squares = []
        for i in range(len(ys)):
            N = len(ys[i])
            ind = np.arange(N) + bar_padding
            rects = ax.bar(ind + i*bar_width, ys[i], bar_width)
            color_squares.append(rects[0])
            if label_bars: autolabel(rects, ax)
        ax.set_xticks(ind + len(ys)/2.0*bar_width)
        ax.set_xticklabels(xs[0], rotation=25)
        ax.set_xlim(0, ind[-1]+(len(ys))*bar_width+bar_padding)
        if labels: ax.legend(color_squares, labels)
    elif type == 'hist':
        ax.hist(xs, bins=bins, **kwargs)
    elif type == 'stackplot':
        lines = ax.stackplot(xs, ys)
        ax.set_xticks(np.arange(min(xs), max(xs)+1, 1.0))

    # Additional axes?
    if additional_ylabels:
        addl_y_axes = []
        for label in additional_ylabels:
            new_ax = ax.twinx()
            addl_y_axes.append(new_ax)
            new_ax.set_ylabel(label, fontsize=ylabel_size)
            #new_ax.set_yticklabels([]) # temp
            if additional_ylims:
                new_ax.set_ylim(additional_ylims[0])  # TODO: use real index!

        # plot the extra series
        for i in range(len(ys)):
            # FIXME: index the correct addl y axis!
            if axis_assignments[i] != 1: continue
            line, = addl_y_axes[0].plot(xs[i], ys[i], linestyle=linestyles[i], marker=marker,\
                color=colors[i], label=labels[i], **kwargs)
            lines[i] = line
            if yerrs:
                addl_y_axes[0].fill_between(xs[i], numpy.array(ys[i])+numpy.array(yerrs[i]),\
                numpy.array(ys[i])-numpy.array(yerrs[i]), color=colors[i], alpha=0.5)

    if show_legend and labels: 
        if type == 'stackplot':
            lines = [matplotlib.patches.Rectangle((0,0), 0,0, facecolor=pol.get_facecolor()[0]) for pol in lines]
        ax.legend(lines, labels, loc=legend, ncol=legend_cols, frameon=legend_border,\
            labelspacing=labelspacing, handletextpad=handletextpad, prop={'size':legend_text_size})
            
    else:
        ax.legend_ = None  # TODO: hacky

    # make sure no text is clipped along the boundaries
    plt.tight_layout()

    if filename:
        plt.savefig(filename)
    #plt.show()

    return lines, labels  # making an overall figure legend

# TODO: make this handle more than red/green...
# TODO: merge this with plot()
def heatmap(matrix, xlabel=None, ylabel=None, filename=None):

    plt.pcolor(np.array(matrix), cmap='RdYlGn')
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)
    
    # make sure no text is clipped along the boundaries
    plt.tight_layout()

    # FIXME hardcoded stuff that shouldn't be
    plt.tick_params(\
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off') # labels along the bottom edge are off
    plt.tick_params(\
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left='off',
        right='off',
        labelleft='off')


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
    return plot(xs, ys, ylabel='CDF', marker=None, **kwargs)

def stackplot(ys, sortindex=-1, **kwargs):
    '''Wrapper for making stackplots'''

    # sort, maybe
    if sortindex >= 0:
        ys = zip(*sorted(zip(*ys), key=lambda x: x[sortindex]))

    x = np.arange(len(ys[0]))

    return plot(x, ys, xlim=(min(x), max(x)), type='stackplot', **kwargs)
    



def main():

    ## test cdf
    #data = [1, 2, 3, 4, 5, 6]

    #y_vals, x_vals = cdf_vals_from_data(data)
    #plot(y_vals, x_vals, 'cdf')

    ## test heatmap
    #matrix = [[1, 0, 1], [1, 0, 1], [0, 0, 1]]
    #heatmap(matrix, xlabel='App Policies', ylabel='User Policies',\
    #    filename="/Users/dnaylor/Desktop/heatmap.pdf")

    # test stackplot
    y1 = [3, 1, 7, 5]
    y2 = [1, 2, 3, 4]
    y3 = [4, 9, 8, 3]
    stackplot([y1, y2, y3], sortindex=0, filename='/Users/dnaylor/Desktop/stackplot.pdf')

if __name__ == '__main__':
    main()
