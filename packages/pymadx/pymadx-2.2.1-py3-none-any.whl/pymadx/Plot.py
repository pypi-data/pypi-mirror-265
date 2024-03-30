"""
Various plots for madx TFS files using the pymadx Tfs class
"""
from builtins import map as _map

import numpy as _np
import math as _math
import matplotlib         as _matplotlib
import matplotlib.patches as _patches
import matplotlib.pyplot  as _plt
import re as _re
import tabulate as _tabulate

from matplotlib.backends.backend_pdf import PdfPages as _PdfPages
from matplotlib.collections import PatchCollection as _PatchCollection

class _My_Axes(_matplotlib.axes.Axes):
    """
    Inherit matplotlib.axes.Axes but override pan action for mouse.
    Only allow horizontal panning - useful for lattice axes.
    """
    name = "_My_Axes"
    def drag_pan(self, button, key, x, y):
        _matplotlib.axes.Axes.drag_pan(self, button, 'x', x, y) # pretend key=='x'

#register the new class of axes
_matplotlib.projections.register_projection(_My_Axes)


def _GetOpticalDataFromTfs(tfsobject, dispersion=True):
    """
    Utility to pull out the relevant optical functions into a simple dictionary.
    """
    d = {}
    d['s']         = tfsobject.GetColumn('S')
    d['betx']      = tfsobject.GetColumn('BETX')
    d['bety']      = tfsobject.GetColumn('BETY')
    if dispersion:
        d['dispx']     = tfsobject.GetColumn('DX')
        d['dispxbeta'] = tfsobject.GetColumn('DXBETA')
        #d['dispy']    = tfsobject.GetColumn('DY') #don't use
    d['x']         = tfsobject.GetColumn('X')
    d['y']         = tfsobject.GetColumn('Y')
    d['sigmax']    = tfsobject.GetColumn('SIGMAX')
    d['sigmay']    = tfsobject.GetColumn('SIGMAY')
    d['sigmaxp']   = tfsobject.GetColumn('SIGMAXP')
    d['sigmayp']   = tfsobject.GetColumn('SIGMAYP')
    return d


def _GetRMatrixDataFromTfs(tfsobject):
    d = {}
    for key in ['S', 'RE11', 'RE12', 'RE21', 'RE22', 'RE33', 'RE34', 'RE43', 'RE44', 'RE16', 'RE26', 'RE36', 'RE46']:
        d[key.lower()] = tfsobject.GetColumn(key)
    return d

def _GetHorizontalBendNames(tfsobject):
    t = tfsobject
    def _HBend(item):
        return abs(item['TILT']) < 1e-1 and item['KEYWORD'] in ['RBEND', 'SBEND']
    hb = [item['NAME'] for item in t if _HBend(item)]
    return hb

def _GetVerticalBendNames(tfsobject):
    t = tfsobject
    def _VBend(item):
        return abs(item['TILT'] - _np.pi*0.5) < 1e-1 and item['KEYWORD'] in ['RBEND', 'SBEND']
    vb = [item['NAME'] for item in t if _VBend(item)]
    return vb

def _RegexMatchNames(tfsobject, regex):
    t = tfsobject
    if type(regex) not in [list, tuple]:
        regex = [regex]
    def _IsMatch(name):
        return any(_re.match(reg, name) for reg in regex)
        #m = _re.match(regex, name)
        #return m is not None

    matchingNames = [item['NAME'] for item in t if _IsMatch(item['NAME'])]
    return matchingNames

def RMatrixOptics(tfsfile, dx=1.0, dpx=1.0, dP=1.0, dy=1.0, dpy=1.0, title=None, outputfilename=None, machine=True):
    """
    Plot the propagation of 3 rays with dx, dy, dpx, dpy, and dE independently.
    :param dx: displacement in x in mm that is propagated
    :type dx: float
    :param dpx: displacement in px (component of unit vector) in 1e-3 (e.g. mrad in small angle).
    :type dpx: float
    :param dP: displacement in momentum as a percentage
    :type dP: float
    :param dy: displacement in x in mm that is propagated
    :type dy: float
    :param dyx: displacement in px (component of unit vector) in 1e-3 (e.g. mrad in small angle).
    :type dyx: float
    """

    import pymadx.Data as _Data
    madx = _Data.CheckItsTfs(tfsfile)
    d = _GetRMatrixDataFromTfs(madx)

    xlabel   = '$x$  = '+str(round(dx,3))+' mm'
    xplabel  = "$x'$ = "+str(round(dpx,3))+' mrad'
    xdplabel = 'd$P$ = '+str(round(dP,3))+' %'

    f1 = _plt.figure(figsize=(9,5))
    axx = f1.add_subplot(111)
    axx.plot(d['s'], d['re11']*dx,  '-',  label=xlabel, color='green')
    axx.plot(d['s'], d['re12']*dpx, '--', label=xplabel, color='red')
    axx.plot(d['s'], d['re16']*dP*10.0,  '-.', label=xdplabel, color='blue')
    axx.plot([d['s'][0], d['s'][-1]], [0,0], c='grey', alpha=0.3)
    _plt.legend()
    _plt.xlabel('$S$ in m')
    _plt.ylabel('$x$ in mm')
    _plt.tight_layout()
    if machine:
        AddMachineLatticeToFigure(f1, madx)
    
    ylabel   = '$y$  = '+str(round(dy,3))+' mm'
    yplabel  = "$y$' = "+str(round(dpy,3))+' mrad'
    ydplabel = 'd$P$ = '+str(round(dP,3))+' %'
    
    f2 = _plt.figure(figsize=(9,5))
    axy = f2.add_subplot(111)
    axy.plot(d['s'], d['re33']*dy,  '-',  label=ylabel, color='green')
    axy.plot(d['s'], d['re34']*dpy, '--', label=yplabel, color='red')
    axy.plot(d['s'], d['re36']*dP*10.0,  '-.', label=ydplabel, color='blue')
    axy.plot([d['s'][0], d['s'][-1]], [0, 0], c='grey', alpha=0.3)
    _plt.legend()
    _plt.xlabel('$S$ in m')
    _plt.ylabel('$y$ in mm')
    _plt.tight_layout()
    if machine:
        AddMachineLatticeToFigure(f2, madx)

    if outputfilename:
        if '.' in outputfilename:
            outputFileNameWithout = outputfilename.split('.')[0]
            extension = outputfilename.split('.')[1]

        f1.savefig(outputFileNameWithout + '_x.' + extension)
        f2.savefig(outputFileNameWithout + '_y.' + extension)
    return f1,f2


def RMatrixOptics2(tfsfile, dx=1.0, dpx=1.0, dP=1.0, dy=1.0, dpy=1.0, title=None, outputfilename=None, machine=True,
                   collimatorHRegex=None, collimatorVRegex=None, figsize=(12, 8), grid=True):
    """
    Plot the propagation of 3 rays with dx, dy, dpx, dpy, and dE independently.
    :param dx: displacement in x in mm that is propagated
    :type dx: float
    :param dpx: displacement in px (component of unit vector) in 1e-3 (e.g. mrad in small angle).
    :type dpx: float
    :param dP: displacement in momentum as a percentage
    :type dP: float
    :param dy: displacement in x in mm that is propagated
    :type dy: float
    :param dyx: displacement in px (component of unit vector) in 1e-3 (e.g. mrad in small angle).
    :type dyx: float
    """

    import pymadx.Data as _Data
    tfs = _Data.CheckItsTfs(tfsfile)
    d = _GetRMatrixDataFromTfs(tfs)

    horizontalNames = _GetHorizontalBendNames(tfs)
    verticalNames = _GetVerticalBendNames(tfs)
    horizontalCollNames = []
    verticalCollNames = []
    if collimatorHRegex is not None:
        horizontalCollNames = _RegexMatchNames(tfs, collimatorHRegex)
    if collimatorVRegex is not None:
        verticalCollNames = _RegexMatchNames(tfs, collimatorVRegex)
    collsToMaskInHorizontal = set(verticalCollNames).difference(set(horizontalCollNames))
    collsToMaskInVertical = set(horizontalCollNames).difference(set(verticalCollNames))
    toMaskInHorizontal = list(verticalNames)
    toMaskInHorizontal.extend(list(collsToMaskInHorizontal))
    toMaskInVertical = list(horizontalNames)
    toMaskInVertical.extend(list(collsToMaskInVertical))

    xlabel = '$x$  = ' + str(round(dx, 3)) + ' mm'
    xplabel = "$x'$ = " + str(round(dpx, 3)) + ' mrad'
    xdplabel = 'd$P$ = ' + str(round(dP, 3)) + ' %'

    f = _plt.figure(figsize=figsize)
    gs = _matplotlib.gridspec.GridSpec(21, 1)

    axMachineX = f.add_subplot(gs[0, :], projection="_My_Axes")
    axx = f.add_subplot(gs[1:10, :], sharex=axMachineX)
    axMachineY = f.add_subplot(gs[12, :], sharex=axMachineX, projection="_My_Axes")
    axy = f.add_subplot(gs[13:, :], sharex=axMachineX)

    if grid:
        ds = 5.0
        smax = _math.ceil(tfs.smax / ds) * ds
        sMinor = _np.arange(tfs.smin, smax, ds)
        axx.set_xticks(sMinor, minor=True)
        axy.set_xticks(sMinor, minor=True)
        axx.grid(visible=True, color='grey', alpha=0.1, which='both')
        axy.grid(visible=True, color='grey', alpha=0.1, which='both')

    def _StyleMachineAxes(ax):
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)

    _DrawMachineLattice(axMachineX, tfs, maskNames=toMaskInHorizontal)
    _StyleMachineAxes(axMachineX)
    axx.plot(d['s'], d['re11'] * dx, '-', label=xlabel, color='red')
    axx.plot(d['s'], d['re12'] * dpx, '--', label=xplabel, color='blue')
    axx.plot(d['s'], d['re16'] * dP * 10.0, '-.', label=xdplabel, color='green')
    axx.plot([d['s'][0], d['s'][-1]], [0, 0], c='grey', alpha=0.3)
    axx.set_ylabel('$x$ in mm')
    axx.legend()

    ylabel = '$y$  = ' + str(round(dy, 3)) + ' mm'
    yplabel = "$y$' = " + str(round(dpy, 3)) + ' mrad'
    ydplabel = 'd$P$ = ' + str(round(dP, 3)) + ' %'

    _DrawMachineLattice(axMachineY, tfs, maskNames=toMaskInVertical, flipQuads=True)
    _StyleMachineAxes(axMachineY)
    axy.plot(d['s'], d['re33'] * dy, '-', label=ylabel, color='red')
    axy.plot(d['s'], d['re34'] * dpy, '--', label=yplabel, color='blue')
    axy.plot(d['s'], d['re36'] * dP * 10.0, '-.', label=ydplabel, color='green')
    axy.plot([d['s'][0], d['s'][-1]], [0, 0], c='grey', alpha=0.3)
    _plt.xlabel('$S$ in m')
    axy.set_ylabel('$y$ in mm')
    axy.legend()

    axMachineX.set_autoscale_on(False)
    axMachineY.set_autoscale_on(False)

    f.subplots_adjust(bottom=0.1, left=0.08, right=0.98, top=0.99)

    if outputfilename:
        f.savefig(outputfilename)

    return f


def Centroids(tfsfile, title='', outputfilename=None, machine=True):
    """
    Plot the centroid (mean) x and y from the a Tfs file or pymadx.Tfs instance.

    tfsfile        - can be either a string or a pymadx.Tfs instance.
    title          - optional title for plot
    outputfilename - optional name to save file to (extension determines format)
    machine        - if True (default) add machine diagram to top of plot
    """
    import pymadx.Data as _Data
    madx = _Data.CheckItsTfs(tfsfile)
    d    = _GetOpticalDataFromTfs(madx)
    smax = madx.smax

    f    = _plt.figure(figsize=(9,5))
    axoptics = f.add_subplot(111)

    #optics plots
    axoptics.plot(d['s'],d['x'],'b-', label=r'$\mu_{x}$')
    axoptics.plot(d['s'],d['y'],'g-', label=r'$\mu_{y}$')
    axoptics.set_xlabel('S (m)')
    axoptics.set_ylabel(r'$\mu_{(x,y)}$ (m)')
    axoptics.legend(loc=0,fontsize='small') #best position

    #add lattice to plot
    if machine:
        AddMachineLatticeToFigure(f,madx)

    _plt.suptitle(title,size='x-large')

    if outputfilename != None:
        if '.' in outputfilename:
            outputfilename = outputfilename.split('.')[0]
        _plt.savefig(outputfilename+'.pdf')
        _plt.savefig(outputfilename+'.png')


def Survey(tfsfile, title='', outputfilename=None):
    """
    Plot the x and z coordinates from a tfs file.
    """
    import pymadx.Data as _Data
    madx = _Data.CheckItsTfs(tfsfile)
    x    = madx.GetColumn('X')
    y    = madx.GetColumn('Y')
    z    = madx.GetColumn('Z')

    f = _plt.figure()
    ax1 = f.add_subplot(211)
    #ax1.set_aspect('equal')
    ax1.plot(z, x, marker='.')
    _plt.suptitle(title, size='x-large')
    _plt.xlabel('Z (m)')
    _plt.ylabel('X (m)')

    ax2 = f.add_subplot(212)
    #ax2.set_aspect('equal')
    ax2.plot(z, y, marker='.')
    _plt.suptitle(title, size='x-large')
    _plt.xlabel('Z (m)')
    _plt.ylabel('Y (m)')


def Beta(tfsfile, title='', outputfilename=None, machine=True, dispersion=False, squareroot=True, dispersionY=False,
         legendLoc="best"):
    """
    Plot sqrt(beta x,y) as a function of S. By default, a machine diagram is shown at
    the top of the plot.

    Optionally set dispersion=True to plot x dispersion as second axis.
    Optionally turn off machine overlay at top with machine=False
    Specify outputfilename (without extension) to save the plot as both pdf and png.
    """
    import pymadx.Data as _Data
    madx = _Data.CheckItsTfs(tfsfile)

    d = {}
    d['s']    = madx.GetColumn('S')
    d['betx'] = madx.GetColumn('BETX')
    d['bety'] = madx.GetColumn('BETY')
    smax = madx.smax

    f    = _plt.figure(figsize=(9,5))
    axoptics = f.add_subplot(111)

    #optics plots
    if squareroot:
        yx = _np.sqrt(d['betx'])
        yy = _np.sqrt(d['bety'])
    else:
        yx = d['betx']
        yy = d['bety']
    axoptics.plot(d['s'], yx, 'b-', label='x')
    axoptics.plot(d['s'], yy, 'g-', label='y')
    if dispersion:
        axoptics.plot([], [], 'r--', label=r'$\mathrm{D}_{x}(S) / \beta_{lorentz}$') #fake plot for legend
    if dispersionY:
        axoptics.plot([], [], ls='--', c='orange', label=r'$\mathrm{D}_{y}(S) / \beta_{lorentz}$') #fake plot for legend
    axoptics.set_xlabel('S (m)')
    if squareroot:
        axoptics.set_ylabel(r'$\sqrt{\beta}$ ($\sqrt{\mathrm{m}}$)')
    else:
        axoptics.set_ylabel(r'$\beta$ (m)')
    axoptics.legend(loc=legendLoc,fontsize='small') #best position
    #axoptics.legend(fontsize='small')  # best position

    #plot dispersion - only in horizontal
    axDisp = None
    if dispersion or dispersionY:
        axDisp = axoptics.twinx()
        axDisp.set_ylabel(r'Dispersion / $\beta_{lorentz}$ (m)')
    if dispersion:
        d['dispxbeta'] = madx.GetColumn('DX')
        axDisp.plot(d['s'],d['dispxbeta'],'r--')
    if dispersionY:
        d['dispybeta'] = madx.GetColumn('DY')
        axDisp.plot(d['s'],d['dispybeta'],ls='--',c='orange')

    #add lattice to plot
    if machine:
        AddMachineLatticeToFigure(f,madx)

    _plt.suptitle(title,size='x-large')
    _plt.xlim((0 - 0.05*smax, 1.05*smax))
    if outputfilename != None:
        if '.' in outputfilename:
            outputfilename = outputfilename.split('.')[0]
        _plt.savefig(outputfilename+'.pdf')
        _plt.savefig(outputfilename+'.png')


def Sigma(tfsfile, title='', outputfilename=None, machine=True, dispersion=False, ax=None, figsize=(9,5)):
    """
    Plot sqrt(beta x,y) as a function of S. By default, a machine diagram is shown at
    the top of the plot.

    Optionally set dispersion=True to plot x dispersion as second axis.
    Optionally turn off machine overlay at top with machine=False
    Specify outputfilename (without extension) to save the plot as both pdf and png.
    """
    import pymadx.Data as _Data
    madx = _Data.CheckItsTfs(tfsfile)
    d    = _GetOpticalDataFromTfs(madx)
    smax = madx.smax

    if ax is None:
        f = _plt.figure(figsize=figsize)
        axoptics = f.add_subplot(111)
    else:
        axoptics = ax

    yx = d['sigmax']
    yy = d['sigmay']

    #meanSize = _np.mean(_np.mean(yx), _np.mean(yy))
    #_np.log10(meanSize)
    
    axoptics.plot(d['s'], yx*1e3, 'b-', label='x')
    axoptics.plot(d['s'], yy*1e3, 'g-', label='y')
    if dispersion:
        axoptics.plot([], [],'r--', label=r'$\mathrm{D}_{x} / \beta (S)$') #fake plot for legend
    axoptics.set_xlabel('S (m)')
    axoptics.set_ylabel(r'$\sigma$ (mm)')
    axoptics.legend(loc=0,fontsize='small') #best position

    #plot dispersion - only in horizontal
    if dispersion:
        ax2 = axoptics.twinx()
        ax2.plot(d['s'],d['dispx'],'r--')
        ax2.set_ylabel(r'Dispersion / $\beta$ (m)')

    #add lattice to plot
    if machine:
        AddMachineLatticeToFigure(f,madx)

    _plt.suptitle(title,size='x-large')
    _plt.xlim((0 - 0.05*smax, 1.05*smax))
    if outputfilename != None:
        if '.' in outputfilename:
            outputfilename = outputfilename.split('.')[0]
        _plt.savefig(outputfilename+'.pdf')
        _plt.savefig(outputfilename+'.png')


def Aperture(aperture, machine=None, outputfilename=None, plot="xy", plotapertype=True):
    """
    Plots the aperture extents vs. S from a pymadx.Data.Aperture instance.

    Inputs:
      aperture (pymadx.Data.Aperture) - the aperture model to plot from
      machine (str or pymadx.Data.Tfs) - TFS file or TFS istance to plot a machine lattice from (default: None)
      outputfilename (str) - Name without extension of the output file if desired (default: None)
      plot (str) - Indicates whcih aperture to plot - 'x' for X, 'y' for Y and 'xy' for both (default: 'xy')
      plotapertype (bool) - If enabled plots the aperture type at every definted aperture point as a color-coded dot (default: False)
    """
    import pymadx.Data as _Data
    aper = _Data.CheckItsTfsAperture(aperture)

    allowed = ["x", "y", "xy", "X", "Y", "XY"]
    if plot not in allowed:
        raise ValueError("Invalid option plot: "+plot+". Use 'x', 'y' or 'xy'")

    f = _plt.figure(figsize=(9,5))

    s = aper.GetColumn('S')
    x,y = aper.GetExtentAll()

    if plotapertype:
        t = aper.GetColumn('APERTYPE')
        c = list(_map(_ApertureTypeToColour, t))

    if "x" in plot.lower():
        line1, = _plt.plot(s, x, 'b-', label='X', alpha=0.6)
        if plotapertype:
            _plt.scatter(s, x, c=c, s=6)

    if "y" in plot.lower():
        line2, = _plt.plot(s, y, 'g-', label='Y', alpha=0.6)
        if plotapertype:
            _plt.scatter(s, y, c=c, s=6)

    _plt.xlabel('S (m)')
    _plt.ylabel('Aperture (m)')

    if plotapertype:
        _AddColourLegend(c)

    _plt.legend(loc='best', numpoints=1, scatterpoints=1, fontsize='small')

    if machine != None:
        AddMachineLatticeToFigure(_plt.gcf(), machine)

    if outputfilename != None:
        if '.' in outputfilename:
            outputfilename = outputfilename.split('.')[0]
        _plt.savefig(outputfilename+'.pdf')
        _plt.savefig(outputfilename+'.png')


def ApertureN1(aperture, machine=None, outputfilename=None):
    """
    Plot the N1 aperture value from MADX.

    Requires N1 and S column.

    Optional "machine" argument is string to or pymadx.Data.Tfs instance
    for twiss description to provide a machine diagram on top.
    """

    import pymadx.Data as _Data
    aper = _Data.CheckItsTfsAperture(aperture)

    f = _plt.figure(figsize=(9,5))

    s = aper.GetColumn('S')
    n = aper.GetColumn('N1')

    _plt.plot(s,n)
    _plt.xlabel('S (m)')
    _plt.ylabel(r'N1 ($\sigma$)')

    if machine != None:
        AddMachineLatticeToFigure(_plt.gcf(), machine)

    if outputfilename != None:
        if '.' in outputfilename:
            outputfilename = outputfilename.split('.')[0]
        _plt.savefig(outputfilename+'.pdf')
        _plt.savefig(outputfilename+'.png')


def _ApertureTypeColourMap():
    #Some nice colors
    _colourCodes = ['#C03028',
                    '#F8D030',
                    '#6890F0',
                    '#F85888',
                    '#A8B820',
                    '#F08030',
                    '#7038F8',
                    '#78C850',
                    '#A8A878']

    #_colourCodes = [_HexToRGB(c) for c in _colourCodes]

    # MADX aperture types
    _madxAperTypes = ['CIRCLE',
                      'RECTANGLE',
                      'ELLIPSE',
                      'RECTCIRCLE',
                      'LHCSCREEN',
                      'MARGUERITE',
                      'RECTELLIPSE',
                      'RACETRACK',
                      'OCTAGON']
    typeToCol = dict(list(zip(_madxAperTypes, _colourCodes)))
    return typeToCol


def _HexToRGB(h):
    h = h.strip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))


def _ApertureTypeToColour(apertype, cmap=_ApertureTypeColourMap()):
    colour = (0,0,0)
    try:
        colour = cmap[apertype.upper()]
    except:
        colour = '#BCBCBC' # greyish

    return colour


def _AddColourLegend(colours, cmap=_ApertureTypeColourMap()):
    found_cols = set(colours)
    typemap = dict((v,k) for k,v in cmap.items()) #invert to get apertype from color
    for col in found_cols:
        _plt.scatter(None,None,color=col, label=typemap[col].lower())


def _SetMachineAxesStyle(ax):
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)


def _PrepareMachineAxes(figure):
    # create new machine axis with proportions 6 : 1
    axmachine = figure.add_subplot(911, projection="_My_Axes")
    axmachine.set_facecolor('none') # make background transparent to allow scientific notation
    _SetMachineAxesStyle(axmachine)
    return axmachine


def _AdjustExistingAxes(figure, fraction=0.9, tightLayout=True):
    """
    Fraction is fraction of height all subplots will be after adjustment.
    Default is 0.9 for 90% of height.
    """
    # we have to set tight layout before adjustment otherwise if called
    # later it will cause an overlap with the machine diagram
    if (tightLayout):
        _plt.tight_layout()

    axs = figure.get_axes()

    for ax in axs:
        bbox = ax.get_position()
        bbox.y0 = bbox.y0 * fraction
        bbox.y1 = bbox.y1 * fraction
        ax.set_position(bbox)


def AddMachineLatticeToFigure(figure, tfsfile, tightLayout=True, reverse=False, offset=None):
    """
    Add a diagram above the current graph in the figure that represents the
    accelerator based on a madx twiss file in tfs format.

    Note you can use matplotlib's gcf() 'get current figure' as an argument.

    >>> pymadx.Plot.AddMachineLatticeToFigure(gcf(), 'afile.tfs')

    A pymadx.Tfs class instance or a string specifying a tfs file can be
    supplied as the second argument interchangeably.

    If the reverse flag is used, the lattice is plotted in reverse only. The tfs
    instance doesn't change.
    
    Offset can optionally be the name of an object in the lattice (exact name match).

    If both offset and reverse are used, reverse happens first. The right click searching
    works with the reverse and offset similarly.
    """
    import pymadx.Data as _Data
    tfs = _Data.CheckItsTfs(tfsfile) #load the machine description

    #check required keys
    useQuadStrength = True
    requiredKeys = ['KEYWORD', 'S', 'L', 'K1L']
    okToProceed = all([key in tfs.columns for key in requiredKeys])
    if not okToProceed:
        minimumKeys = ['KEYWORD', 'S', 'L']
        if not all([key in tfs.columns for key in minimumKeys]):
            print("The required columns aren't present in this tfs file")
            print("The required columns are: ", requiredKeys)
            raise IOError
        else:
            useQuadStrength = False

    axoptics  = figure.get_axes()[0]
    _AdjustExistingAxes(figure, tightLayout=tightLayout)
    axmachine = _PrepareMachineAxes(figure)
    axmachine.margins(x=0.02)

    _DrawMachineLattice(axmachine, tfs, reverse, offset, useQuadStrength)

    #put callbacks for linked scrolling
    def MachineXlim(ax):
        axmachine.set_autoscale_on(False)
        axoptics.set_xlim(axmachine.get_xlim())

    def Click(a) :
        if a.button == 3:
            try:
                x = a.xdata
                if reverse:
                    x = tfs.smax - x
                if offset:
                    ind = tfs.sequence.index(offset)
                    xoffset = tfs[ind]['S']
                    x += xoffset
                    if x > tfs.smax:
                        x -= tfs.smax
                print('Closest element: ',tfs.NameFromNearestS(x))
            except:
                pass # don't complain if the S is out of bounds

    MachineXlim(axmachine)
    axmachine.callbacks.connect('xlim_changed', MachineXlim)
    figure.canvas.mpl_connect('button_press_event', Click)


def MachineDiagram(tfsfile, title=None, reverse=False):
    """
    Plot just a machine diagram on its own. The S axis is shown.
    
    :param tfsfile: TFS instance or file name of lattice to plot.
    :type tfsfile:  pymadx.Data.TFS, str
    :param title: Title for plot.
    :type title: None, str
    :param reverse: Whether to reverse the direction of the machine.
    :type reverse: bool

    """
    import pymadx.Data as _Data
    tfs = _Data.CheckItsTfs(tfsfile) #load the machine description

    #check required keys
    useQuadStrength = True
    requiredKeys = ['KEYWORD', 'S', 'L', 'K1L']
    okToProceed = all([key in tfs.columns for key in requiredKeys])
    if not okToProceed:
        minimumKeys = ['KEYWORD', 'S', 'L']
        if not all([key in tfs.columns for key in minimumKeys]):
            print("The required columns aren't present in this tfs file")
            print("The required columns are: ", requiredKeys)
            raise IOError
        else:
            useQuadStrength = False

    f = _plt.figure(figsize=(10,2))
    ax = f.add_subplot(111)
    _DrawMachineLattice(ax, tfs, reverse=reverse)
    _plt.xlabel('S (m)')
    _plt.ylim(-0.3,0.3)
    ax.get_yaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    #ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if title:
        _plt.title(title)
    _plt.tight_layout()


def TwoMachineDiagrams(tfsTop, tfsBottom, labelTop=None, labelBottom=None, title=None, reverse=False):
    """
    Plot just a machine diagram on its own. The S axis is shown.
    
    :param tfsfile: TFS instance or file name of lattice to plot.
    :type tfsfile:  pymadx.Data.TFS, str
    :param title: Title for plot.
    :type title: None, str
    :param reverse: Whether to reverse the direction of the machine.
    :type reverse: bool

    """
    import pymadx.Data as _Data
    tfsT = _Data.CheckItsTfs(tfsTop)
    tfsB = _Data.CheckItsTfs(tfsBottom)

    #check required keys
    useQuadStrength = True
    requiredKeys = ['KEYWORD', 'S', 'L', 'K1L']
    okToProceedT = all([key in tfsT.columns for key in requiredKeys])
    okToProceedB = all([key in tfsB.columns for key in requiredKeys])
    if not okToProceedT and not okToProceedB:
        minimumKeys = ['KEYWORD', 'S', 'L']
        if not all([key in tfsT.columns for key in minimumKeys]):
            print("The required columns aren't present in this tfsTop file")
            print("The required columns are: ", requiredKeys)
            raise IOError
        elif not all([key in tfsB.columns for key in minimumKeys]):
            print("The required columns aren't present in this tfsBottom file")
            print("The required columns are: ", requiredKeys)
            raise IOError
        else:
            useQuadStrength = False
    
    f,(axt,axb) = _plt.subplots(2,1,sharex=True,figsize=(10,3))
    _DrawMachineLattice(axt, tfsT, reverse=reverse)
    _DrawMachineLattice(axb, tfsB, reverse=reverse)
    axt.set_ylim(-0.3,0.3)
    axb.set_ylim(-0.3,0.3)

    _plt.subplots_adjust(hspace=0)

    _plt.xlabel('S (m)')
    
    axt.get_yaxis().set_visible(False)
    axb.get_yaxis().set_visible(False)
    axt.spines['top'].set_visible(False)
    axb.spines['top'].set_visible(False)
    #ax.spines['bottom'].set_visible(False)
    axt.spines['left'].set_visible(False)
    axt.spines['right'].set_visible(False)
    axb.spines['left'].set_visible(False)
    axb.spines['right'].set_visible(False)
    if title:
        _plt.title(title)
    _plt.tight_layout()


def _DrawMachineLattice(axesinstance, pymadxtfsobject, reverse=False, offset=None, useQuadStrength=True, maskNames=None,
                        flipQuads=False):
    ax  = axesinstance #handy shortcut
    tfs = pymadxtfsobject

    if not maskNames:
        maskNames = []
    quadFactor = -1.0 if flipQuads else 1.0

    s0 = 0 #accumulated length variable that will be used by functions
    l = 0 #length variable that will be used by functions
    #NOTE madx defines S as the end of the element by default
    #define temporary functions to draw individual objects
    def DrawBend(e,color='b',alpha=1.0):
        return _patches.Rectangle((s0,-0.1),l,0.2,color=color,alpha=alpha)
    def DrawQuad(e,color='r',alpha=1.0):
        k1l = e['K1L'] * quadFactor
        if useQuadStrength:
            if k1l > 0:
                return _patches.Rectangle((s0,0),l,0.2,color=color,alpha=alpha)
            elif k1l < 0:
                return _patches.Rectangle((s0,-0.2),l,0.2,color=color,alpha=alpha)
            else:
                #quadrupole off
                return _patches.Rectangle((s0,-0.1),l,0.2,color=color,alpha=0.1)
        else:
            return _patches.Rectangle((s0,-0.2),l,0.4,color=color,alpha=alpha)
    def DrawHex(e,color,alpha=1.0):
        edges = _np.array([[s0,-0.1],[s0,0.1],[s0+l/2.,0.13],[s0+l,0.1],[s0+l,-0.1],[s0+l/2.,-0.13]])
        return _patches.Polygon(edges,color=color,fill=True,alpha=alpha)
    def DrawRect(e,color,alpha=1.0):
        return  _patches.Rectangle((s0,-0.1),l,0.2,color=color,alpha=alpha)
    def DrawLine(e,color,alpha=1.0):
        ax.plot([s0,s0],[-0.2,0.2],'-',color=color,alpha=alpha)

    # decide on a sequence here
    sequence = tfs.sequence
    if reverse:
        sequence = sequence[::-1]
    if offset is not None:
        index = sequence.index(offset)
        sequence = sequence[index:] + sequence[:index] # cycle it
    
    # loop over elements and prepare patches
    # patches are turned into patch collection which is more efficient later
    quads, bends, hkickers, vkickers, collimators, sextupoles, octupoles, multipoles, solenoids, unknown = [],[],[],[],[],[],[],[],[], []
    for name in sequence:
        element = tfs[name]
        l = element['L']
        kw = element['KEYWORD']
        alpha = 1.0
        if name in maskNames:
            alpha = 0.1
        if kw == 'QUADRUPOLE':
            quads.append(DrawQuad(element, u'#d10000', alpha)) #red
        elif kw == 'RBEND':
            bends.append(DrawBend(element, u'#0066cc', alpha)) #blue
        elif kw == 'SBEND':
            bends.append(DrawBend(element, u'#0066cc', alpha)) #blue
        elif kw == 'HKICKER':
            hkickers.append(DrawRect(element, u'#4c33b2', alpha)) #purple
        elif kw == 'VKICKER':
            vkickers.append(DrawRect(element, u'#ba55d3', alpha)) #medium orchid
        elif kw == 'SOLENOID':
            solenoids.append(DrawRect(element, u'#ff8800', alpha)) #orange
        elif kw == 'RCOLLIMATOR':
            collimators.append(DrawRect(element,'k', alpha))
        elif kw == 'ECOLLIMATOR':
            collimators.append(DrawRect(element,'k', alpha))
        elif kw == 'COLLIMATOR':
            collimators.append(DrawRect(element,'k', alpha))
        elif kw == 'SEXTUPOLE':
            sextupoles.append(DrawHex(element, u'#ffcc00', alpha)) #yellow
        elif kw == 'OCTUPOLE':
            octupoles.append(DrawHex(element, u'#00994c', alpha)) #green
        elif kw == 'DRIFT':
            pass
        elif kw == 'MULTIPOLE':
            multipoles.append(DrawHex(element,'grey',alpha=0.5))
        else:
            #unknown so make light in alpha
            if element['L'] > 1e-1:
                unknown.append(DrawRect(element,'#cccccc',alpha=0.2)) #light grey
            else:
                #relatively short element - just draw a line
                DrawLine(element,'#cccccc',alpha=0.1)
        s0 += l

    # convert list of patches to patch collection, True means retain original colour
    # zorder to make sure small bright things don't dominate (like sextupoles)
    ax.add_collection(_PatchCollection(bends,       match_original=True, zorder=20))
    ax.add_collection(_PatchCollection(quads,       match_original=True, zorder=19))
    ax.add_collection(_PatchCollection(hkickers,    match_original=True, zorder=18))
    ax.add_collection(_PatchCollection(vkickers,    match_original=True, zorder=17))
    ax.add_collection(_PatchCollection(collimators, match_original=True, zorder=16))
    ax.add_collection(_PatchCollection(sextupoles,  match_original=True, zorder=15))
    ax.add_collection(_PatchCollection(octupoles,   match_original=True, zorder=14, edgecolor=None))
    ax.add_collection(_PatchCollection(multipoles,  match_original=True, zorder=13, edgecolor=None))
    ax.add_collection(_PatchCollection(unknown,     match_original=True, zorder=12, edgecolor=None))
    ax.add_collection(_PatchCollection(solenoids,   match_original=True, zorder=11))

    # plot beam line - make extra long in case of reversal
    # set zorder on top
    ax.plot([tfs.smin,tfs.smax],[0,0],'k-',lw=1, zorder=100)
    ax.set_ylim(-0.2,0.2)
    ax.set_xlim(tfs.smin, tfs.smax)


def RMatrixTableString(tfs):
    """
    :param tfs: TFS object to inspect.
    :type tfs: pymadx.Data.Tfs

    Get the most common rmatrix terms out of the TFS file and prepare a string
    of them in a nice big table. Returns a string.
    """
    rmat = {}
    for key in ['NAME', 'S', 'RE11', 'RE12', 'RE22', 'RE33', 'RE34', 'RE44', 'RE16', 'RE26', 'RE36', 'RE46']:
        rmat[key] = tfs.GetColumn(key)
    rmat['S_End'] = rmat.pop('S')
    s = _tabulate.tabulate(rmat, headers=rmat, tablefmt="grid")
    return s


def PrintRMatrixTable(tfs):
    s = RMatrixTableString(tfs)
    print(s)


def RMatrixTableToPdf(tfs, outputfilename):
    """
    Save an rmatrix table to a pdf on multiple pages.

    :param tfs: TFS instance to get the data from.
    :type tfs: pymadx.Data.Tfs
    :param outputfilename: file name to save the pdf as
    :type outputfilename: str
    """
    rmat = {}
    columns = ['NAME', 'S', 'RE11', 'RE12', 'RE22', 'RE33', 'RE34', 'RE44', 'RE16', 'RE36']
    for key in columns:
        rmat[key] = tfs.GetColumn(key)
    columns[1] = 'S_End'
    rmat['S_End'] = rmat.pop('S')

    name = ' '.join([tfs.header[k] for k in ['TITLE', 'SEQUENCE', 'DATE', 'TIME']])

    nPerPage = 45
    rmat2 = _np.array([list(rmat[k]) for k in columns]).transpose()

    def get_every_n(a, ni):
        f = a.shape[0] // ni
        for i in range(f + 1):
            yield a[ni * i:ni * (i + 1)]

    with _PdfPages(outputfilename) as pdf:
        for i, chunk in enumerate(get_every_n(rmat2, nPerPage)):
            _plt.figure(figsize=(8.3, 11.7))  # A4 size
            tableString = _tabulate.tabulate(chunk, headers=columns, tablefmt="grid")
            l = len(chunk)
            dy = 0
            if l < nPerPage:
                # if shorter, move it up the page
                dy = 0.85 * (1.0 - l/float(nPerPage))
            _plt.figtext(0.05, 0.05 + dy, tableString, fontsize='x-small', fontfamily='monospace')
            _plt.suptitle(name + "  Pg" + str(i+1))
            pdf.savefig()
            _plt.close()