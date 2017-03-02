import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as plticker
import matplotlib.patches as mpatches
import seaborn as sns
import matplotlib


font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 20}

matplotlib.rc('font', **font) 
bmap = sns.color_palette("Set2", 5)
sns.set(style='ticks', palette='Set2')
sns.despine()

def plotIntervals(ranges):
	fig = plt.figure(figsize=(13, 6))
	ax = fig.add_subplot(111)

	N = len(ranges)

	ind = np.arange(N)+1
	width = 0.6
	upper_vals = ranges[:,1]
	lower_vals = ranges[:,0]

	ax.bar(ind, upper_vals, width,bottom=lower_vals,tick_label=ind,align="center" , edgecolor="black",linewidth=1.3)
	# loc = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
	# ax.xaxis.set_major_locator(loc)
	# ax.set_ylim([0,1])
	#ax.set_xlim([0,33])
	plt.ylabel('relevance',fontsize=19)
	plt.xlabel('feature',fontsize=19)
	# names = {
	#     0:"Androgens",
	#     1:"Androgen precursors",
	#     2:"Mineralocorticoids",
	#     3:"Glucocorticoid precursors",
	#     4:"Glucocorticoids"
	# }

#	patches = []
#	for x in names:
#	    patches.append(mpatches.Patch(color=bmap[x], label=names[x]))
#	plt.legend(handles=patches,fontsize=14)
	#plt.show()
	return fig