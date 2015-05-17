''' 
Customizing matplotlib
The actions below cannot be done through matplotlibrc file
'''


def modifyaxesrasi( axes ):
    '''
    Removes top and right axes. Shifts left axis
    by 5pt
    '''
    axes.get_xaxis().set_ticks_position('bottom')
    axes.get_yaxis().set_ticks_position('left')
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    axes.spines['left'].set_position(('outward',5))
