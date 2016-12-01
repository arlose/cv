# use matplotlib save plot image

import numpy as np

import matplotlib
matplotlib.use('Agg')

from matplotlib.pyplot import plot,savefig

x=np.linspace(-4,4,30)
y=np.sin(x);

plot(x,y,'--*b')

savefig('./MyFig.jpg')
