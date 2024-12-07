import panel as pn
from vsxplore_api import VSXAPI
import matplotlib.pyplot as plt
import astrocalc as ac
import pandas as pd
import numpy as np
import datashader as ds
import colorcet as cc


# Loads javascript dependencies and configures Panel (required)
pn.extension()

# Connect to the vsx API
api = VSXAPI()
database = 'vsx.db'
debug = True
PATH_TO_DB = '../data/vsx/' + database
print("Connecting to", PATH_TO_DB, database)
api.connect(PATH_TO_DB, debug=debug)


# connect_api(database)

# DASHBOARD DATA INITIALIZATION
constellations = api.constellation_list()
all_types = api.all_types()
cat_type = api.category_type_map()
cat_type['Any'] = all_types

columns = """ 
        oid,name,con,varcat,vartype,nobs,
        magmax,magmin,magmean,amplitude,
        period,spectype,ra,dec,ra2000,dec2000,glat,glon"""

hidden_columns = ['ra', 'dec', 'glat', 'glon', 'vtype', 'vtype_unc', 'glon180']

widths = {'oid':75, 'con':100, 'name':185, 'varcat':100, 'vartype':100, 'nobs':80,
          'magmax':100, 'magmin':100, 'magmean':100, 'amplitude':120, 'period':100,
          'spectype':150, 'ra':150, 'dec':150}  # , 'vtype':100, 'vtype_unc':100}

align = {col:'center' for col in columns.split(",")}

plot_label = {'nobs':'# Observations',
              'log(nobs)':'# Observations (log_10)',
              'period':'Period (Days)',
              'amplitude':'Amplitude (M_min - M_max)',
              'ra':'Right Ascension (J2000.0)',
              'dec':'Declination (J2000.0)',
              'glon': 'Galactic Longitude (deg)',
              '|glon|': '|Galactic Longitude| (deg)',
              'glat': 'Galactic Latitude (deg)',
              '|glat|': '|Galactic Latitude| (deg)',
              'magmax':'M_max',
              'magmin':'M_min',
              'magmean':'M_mean',
              'varcat':'Variable Category',
              'vartype':'Variable Type'}

# plot_limits = {'ra':(24,0), 'dec':(-90,90), 'glon':(360, 0), 'glat':(-90,90)}
plot_limits = {'ra':(24,0), 'dec':(-90,90), 'glon':(-180,180), 'glat':(-90,90)}

# vsx = None
# summary = None

# WIDGET DECLARATIONS

# Time Widgets
lt = pn.widgets.StaticText(name='Local', value='hh:mm:ss')
gmt = pn.widgets.StaticText(name='GMT', value='hh:mm:ss')
lst = pn.widgets.StaticText(name='LST', value='Coming Soon')
jd = pn.widgets.StaticText(name='JD', value='xxx.xxxxx')
mjd = pn.widgets.StaticText(name='MJD', value='xxx.xxxxx')

# Search Widgets

varname = pn.widgets.TextInput(name='Name', placeholder='Enter search substring...', value='')
varcat = pn.widgets.Select(name="Category", options=['Any'] + list(cat_type.keys())[:-1], value='Any')
# vartype = pn.widgets.Select(name='Variability Type', options=[])
# vartype_list = pn.widgets.TextInput(name='Variability Type List (Override)', placeholder="Enter list of variable types...", value='')
vartype = pn.widgets.MultiSelect(name='Variability Type', options=[], height=200)
vartype_unc = pn.widgets.Checkbox(name="Include Uncertain Types", value=True)
multitype =   pn.widgets.Checkbox(name="Include Multi-Type Stars", value=True)
unobserved = pn.widgets.Checkbox(name="Include Unobserved Stars", value=False)

constellation = pn.widgets.Select(name="Constellation", options=['Any']+constellations, value='Any')
amplitude = pn.widgets.RangeSlider(name="Amplitude", start=0, end=10, value_end=30, value_start=0, step=0.1)
# period = pn.widgets.RangeSlider(name="Period", start=0, end=500, value_start=1, value_end=1000)
period = pn.widgets.RangeSlider(name=f"Period (10\u02E3 Days)", start=-3, end=5, value_start=-3, value_end=5, step=0.1)

magmax = pn.widgets.RangeSlider(name="Max Magnitude", start=0, end=15, value=(0,15), step=0.1)
magmin = pn.widgets.RangeSlider(name="Min Magnitude", start=0, end=15, value=(0,15), step=0.1)
magmean = pn.widgets.RangeSlider(name="Mean Magnitude", start=0, end=15, value=(0,13), step=0.1)
spec = pn.widgets.TextInput(name='Spectral Type', placeholder='Enter search substring...', value='')

# Plotting widgets

plot_grid = pn.widgets.Checkbox(name="Show Grid", value=True)
plot_color = pn.widgets.ColorPicker(name="Background Color", value='#FFFFFF')

marker_color = pn.widgets.Select(name="Marker Color", options=['None', 'nobs', 'log(nobs)', 'varcat', 'vartype',
                                                               'period', 'amplitude', 'magmax', 'magmin', 'magmean',
                                                               'ra', 'dec', 'glat', '|glat|', 'glon', '|glon|'], value='varcat')

marker_size = pn.widgets.Select(name="Marker Size", options=['None', 'nobs', 'log(nobs)', 'varcat', 'vartype',
                                                               'period', 'amplitude', 'magmax', 'magmin', 'magmean',
                                                               'ra', 'dec', 'glat', 'glon'], value='nobs')

marker_scaling = pn.widgets.FloatSlider(name="Marker Scaling", start=-10, end=10, value=0, step=.1)
marker_alpha = pn.widgets.FloatSlider(name="Marker Alpha", start=0.0, end=1.0, value=1.0, step=.01)

marker_cmap = pn.widgets.Select(name="Color Map",
                                options=['viridis', 'plasma', 'cividis', 'inferno', 'magma',
                                         'ocean', 'jet', 'gist_earth',
                                         'turbo', 'twilight', 'winter',
                                         'Accent', 'Dark2', 'Set1', 'Set2', 'Set3',
                                         'tab10', 'tab20', 'tab20b', 'tab20c'],
                                value='viridis')


x_log = pn.widgets.Checkbox(name="Log Scaling", value=True)
y_log = pn.widgets.Checkbox(name="Log Scaling", value=True)
x_reverse = pn.widgets.Checkbox(name="Reverse", value=False)
y_reverse = pn.widgets.Checkbox(name="Reverse", value=False)

x_axis = pn.widgets.Select(name="X Axis", options=['nobs', 'period', 'amplitude', 'magmax', 'magmin', 'magmean',
                                                   'ra', 'dec', 'glon', 'glat'], value='period')
y_axis = pn.widgets.Select(name="Y Axis", options=['nobs', 'period', 'amplitude', 'magmax', 'magmin', 'magmean',
                                                   'ra', 'dec', 'glon', 'glat'], value='amplitude')

map_coord = pn.widgets.Select(name="Map Coordinates", options=['RA/DEC (Equatorial)', 'GLON/GLAT (Galactic)'],
                              value='RA/DEC (Equatorial)')

# Location Widgets
gpslat = pn.widgets.TextInput(name='GPS Latitude  ( -90.0 ...  90.0)', value='')  # 33.6
gpslon = pn.widgets.TextInput(name='GPS Longitude (-180.0 ... 180.0)', value='')  # -111.7

# Data set widget
database = pn.widgets.Select(name="Database (Future)", options=['vsx6.db', 'vsx7.db', 'vsx8.db',
                                                                'vsx9.db', 'vsx13.db', 'vsx.db'],
                             value=database, disabled=False)

# Reset all widgets
reset = pn.widgets.Button(name="Reset", button_type="primary")


def update_vartype_options(varcat_value):
    """ Update vartype selector options """

    vartype.options = cat_type[varcat_value]
    vartype.value = []  # default value

# Initialize vartype options based on the initial varcat value
update_vartype_options(varcat.value)


# CALLBACK FUNCTIONS

def clock_update():
    lt.value = ac.local().strftime('%Y-%m-%d %Hh %Mm %Ss')
    gmt.value = ac.GMT().strftime(' %Y-%m-%d %Hh %Mm %Ss')
    jdnow = ac.julian_now()
    jd.value = "%.5f" % round(jdnow, 5)
    mjd.value = "%.5f" % round(jdnow - 2400000.5, 5)

    if gpslon.value is not None and gpslon.value != '':
        lstdec = ac.LST(float(gpslon.value))
        h, m, s = ac.dec2hms(lstdec)
        s = round(s)
        lst.value = f"{h:02}h {m:02}m {s:02}s"
    else:
        lst.value = 'Set GPS Longitude'


pn.state.add_periodic_callback(clock_update, period=1000)


def get_catalog(varname, varcat, vartype, vartype_unc, multitype, unobserved, constellation,
                period, amplitude, magmax, magmin, magmean, spec,
                database):

    vcat = varcat if varcat != 'Any' else None
    vtype = ",".join(vartype) if len(vartype)>0 else None

    # vtype = vartype if vartype != 'Any' else None
    con = constellation if constellation != 'Any' else None
    spec = spec.replace("*", "%") if spec != '' else None
    varname = varname.replace("*", "%") if varname != '' else None

    period_min, period_max = period
    if period_min == -3:
        period_min = None
    else:
        period_min = 10 ** period_min

    if period_max == 5:
        period_max = None
    else:
        period_max = 10 ** period_max

    amplitude_min, amplitude_max = amplitude
    if amplitude_min == 0:
        amplitude_min = None
    if amplitude_max == 10:
        amplitude_max = None

    magmax_min, magmax_max = magmax
    if magmax_min == 0:
        magmax_min = None
    if magmax_max == 15:
        magmax_max = None

    magmin_min, magmin_max = magmin
    if magmin_min == 0:
        magmin_min = None
    if magmin_max == 15:
        magmin_max = None

    magmean_min, magmean_max = magmean
    if magmean_min == 0:
        magmean_min = None
    if magmean_max == 15:
        magmean_max = None

    nobs = None if unobserved else (1, None)

    global vsx
    vsx = api.getvsx(columns=columns,
                     varname=varname,
                     varcat=vcat,
                     vartype=vtype,
                     vartype_unc=vartype_unc,
                     nobs=nobs,
                     multitype=multitype,
                     constellation=con,
                     spectype=spec,
                     period=(period_min, period_max),
                     amplitude=(amplitude_min, amplitude_max),
                     magmax=(magmax_min, magmax_max),
                     magmin=(magmin_min, magmin_max),
                     magmean=(magmean_min, magmean_max))

    vsx['vtype'] = vsx['vartype'].str.replace(":", "")
    vsx['vtype_unc'] = vsx['vartype'].str.contains(":").astype(int)


    vsx.set_index('oid', inplace=True)

    table =  pn.widgets.Tabulator(vsx, widths=widths, selectable=False,
                                  header_align=align, text_align=align, hidden_columns=hidden_columns)

    return table


def get_summary(varname, varcat, vartype, vartype_unc, multitype, unobserved, constellation,
                period, amplitude, magmax, magmin, magmean, spec,
                database):

    global vsx
    global summary

    grouped = vsx.groupby(['varcat', 'vtype'])

    summary = grouped.agg(
        num=('vtype', 'size'),
        uncertain=('vtype_unc', 'mean'),
        nobs=('nobs', 'sum'),
        nobs_max=('nobs', 'max'),
        period_min=('period', 'min'),
        period_avg=('period', 'mean'),
        period_max=('period', 'max'),
        amplitude_min=('amplitude', 'min'),
        amplitude_avg=('amplitude', 'mean'),
        amplitude_max=('amplitude', 'max')
    ).reset_index()

    summary.sort_values(by='num', ascending=False, inplace=True)
    summary['uncertain'] = summary['uncertain'].round(3)
    table =  pn.widgets.Tabulator(summary, widths=widths, selectable=False, show_index=False,
                                  header_align=align, text_align=align)
    return table


def get_plot(varname, varcat, vartype, vartype_unc, multitype, unobserved, constellation,
             period, amplitude, magmax, magmin, magmean, spec,
             plot_grid, plot_color, marker_color, marker_cmap, marker_size, marker_scaling, marker_alpha,
             x_axis, y_axis, x_log, y_log, x_reverse, y_reverse,
             database):

    plt.close()

    global vsx

    if marker_color == 'None':
        color = None
    elif marker_color == 'varcat' or marker_color == 'vartype':
        if marker_color == 'varcat':
            categories, unique = pd.factorize(vsx[marker_color])
        else:  # marker_color == 'vartype':
            limit = 10
            toptypes = set(summary.head(limit).vtype)
            vsx['typecolor'] = vsx['vtype'].apply(lambda x: x if x in toptypes else 'Other')
            categories, unique = pd.factorize(vsx.typecolor)
        cmap = plt.get_cmap(marker_cmap)
        color = cmap(categories / len(unique))
        marker_cmap = None
    elif marker_color == 'log(nobs)':
        color = vsx['nobs'].apply(lambda x: np.log10(x) if x > 0 else 0)
    elif marker_color == '|glat|':
        color = vsx['glat'].abs()
    elif marker_color == '|glon|':
        color = vsx['glon'].abs()
    else:
        color = vsx[marker_color]

    if marker_size == 'None':
        size = 1 * (2 ** marker_scaling)
    else:
        size = (vsx[marker_size] + 1) * (2 ** (marker_scaling-8))

    title = str(len(vsx)) + " "
    if not unobserved:
        title += 'Observed'
    if varcat != 'Any':
        title += ' ' + varcat
    title += ' Variables\n(Type: '
    vtype = ", ".join(vartype) if len(vartype) > 0 else None
    if vtype is None:
        title += 'Any)'
    else:
        title += vtype + ")"

    if len(vsx) > 0:

        fig = plt.figure(figsize=(10, 5), dpi=300)

        plt.scatter(vsx[x_axis], vsx[y_axis], marker='.',s=size, c=color, cmap=marker_cmap, alpha=marker_alpha)

        plt.title(title)
        plt.xlabel(plot_label[x_axis], fontsize='small')
        plt.ylabel(plot_label[y_axis], fontsize='small')
        if x_log and x_axis not in ['ra', 'dec', 'glon', 'glat']:
            plt.xscale('log')
        if y_log and y_axis not in ['ra', 'dec', 'glon', 'glat']:
            plt.yscale('log')

        if x_reverse:
            plt.gca().invert_xaxis()

        if y_reverse:
            plt.gca().invert_yaxis()

        if plot_grid:
            plt.grid()
        if marker_color == 'varcat' or marker_color == 'vartype':
            handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cmap(i / len(unique)), markersize=10,
                                  label=cat)
                       for i, cat in enumerate(unique)]
            legend_title = "Category" if marker_color == 'varcat' else 'Type'
            plt.legend(handles=handles, title=legend_title, bbox_to_anchor=(1,1))
            plt.tight_layout()
        elif marker_color != 'None':
            cbar = plt.colorbar()
            cbar.set_label(plot_label[marker_color], fontsize='small')
            cbar.ax.tick_params(labelsize='small')

        if x_axis in plot_limits:
            plt.xlim(plot_limits[x_axis])

        if y_axis in plot_limits:
            plt.ylim(plot_limits[y_axis])

        return fig
    else:
        return None


def get_map(varname, varcat, vartype, vartype_unc, multitype, unobserved, constellation,
            period, amplitude, magmax, magmin, magmean, spec, map_coord, database):

    if len(vsx) > 0:

        x = 'ra' if map_coord == 'RA/DEC (Equatorial)' else 'glon'
        y = 'dec' if map_coord == 'RA/DEC (Equatorial)' else 'glat'

        agg = ds.Canvas(plot_width=1000, plot_height=700).points(vsx, x, y)
        img = ds.tf.set_background(ds.tf.shade(agg, cmap=cc.fire), "black")

        # agg.opts(plot=dict(invert_axis=True))
        # arr = np.array(img)
        # fig = plt.figure(figsize=(10, 5))
        # ax = fig.add_subplot(111, projection='mollweide')
        # ax.grid()
        # rslt = ax.imshow(arr)

        return img
    else:
        return None


def get_description(vartype):
    print("Getting descriptions for ", vartype)
    rslt = ""
    if vartype is not None and len(vartype) > 0:
        for t in vartype:
            varcat, vtype, description = api.get_variability_type_description(t)
            rslt += f"""
                #
                # Category: {varcat}
        
                # Type    : {vtype}
        
                ## {description}
                """
    return pn.pane.Markdown(rslt, width=600)


# Callback Bindings
varcat.param.watch(lambda event: update_vartype_options(event.new), 'value')

catalog = pn.bind(get_catalog, varname, varcat, vartype, vartype_unc, multitype, unobserved,
                  constellation, period.param.value_throttled, amplitude.param.value_throttled,
                  magmax.param.value_throttled,
                  magmin.param.value_throttled,
                  magmean.param.value_throttled,
                  spec, database)

summary = pn.bind(get_summary, varname, varcat, vartype, vartype_unc, multitype, unobserved,
                  constellation, period.param.value_throttled, amplitude.param.value_throttled,
                  magmax.param.value_throttled,
                  magmin.param.value_throttled,
                  magmean.param.value_throttled,
                  spec, database)

description = pn.bind(get_description, vartype)


plot = pn.bind(get_plot, varname, varcat, vartype, vartype_unc, multitype, unobserved,
               constellation, period.param.value_throttled, amplitude.param.value_throttled,
               magmax.param.value_throttled, magmin.param.value_throttled, magmean.param.value_throttled, spec,
               plot_grid, plot_color,
               marker_color, marker_cmap, marker_size,
               marker_scaling.param.value_throttled, marker_alpha.param.value_throttled,
               x_axis, y_axis, x_log, y_log, x_reverse, y_reverse,
               database)

starmap = pn.bind(get_map, varname, varcat, vartype, vartype_unc, multitype, unobserved,
                  constellation, period.param.value_throttled, amplitude.param.value_throttled,
                  magmax.param.value_throttled,
                  magmin.param.value_throttled,
                  magmean.param.value_throttled,
                  spec, map_coord, database)


# DASHBOARD LAYOUT
card_width = 320


time_card = pn.Card(
    pn.Column(
        lt,
        gmt,
        lst,
        jd,
        mjd
    ),
    title="Time", width=card_width, collapsed=False
)


search_card = pn.Card(
    pn.Column(
        varname,
        varcat,
        vartype,
        vartype_unc,
        multitype,
        unobserved,
        constellation,
        period,
        amplitude,
        magmax,
        magmin,
        magmean,
        spec,
        # reset,
        # database
    ),
    title="Search",
    width=card_width,
    collapsed=True
)

location_card = pn.Card(
    pn.Column(
        gpslat,
        gpslon

    ),
    title="Location", width=card_width, collapsed=True
)

plot_card = pn.Card(
    pn.Column(
        plot_grid,
        # plot_color,
        marker_color,
        marker_cmap,

        marker_size,
        marker_scaling,
        marker_alpha,

        x_axis,
        pn.Row(x_log, x_reverse),
        y_axis,
        pn.Row(y_log, y_reverse),
        map_coord
    ),

    title="Plot", width=card_width, collapsed=True
)


info_card = pn.Card(

    pn.Column(
        pn.pane.PNG('img/vsxplore_logo.png', width=card_width, height=300),

        pn.pane.Markdown(
            """
            #### Data Source
            Data Release: 01-Jul-2024
            Number of Stars: 2,279,174
            <a href=\"https://cdsarc.cds.unistra.fr/viz-bin/cat/B/vsx\" target="_blank">CDS Link</a> 
            
            #### Development Team
            <a href=\"https://www.khoury.northeastern.edu/home/rachlin/\">John Rachlin</a>
            Diya Jhamtani
            Jeremiah Payeur

            <a href=\"https://www.khoury.northeastern.edu/home/rachlin/img/129_Jhamtani_Diya.pdf\">RISE2024 Poster</a>    
            """)

    ),

    title="About", width=card_width, collapsed=True,
)

layout = pn.template.FastListTemplate(
    title="VSXplore: Mining the AAVSO VSX Variable Star Catalog",
    sidebar=[

        time_card,
        search_card,
        plot_card,
        location_card,
        info_card,

        pn.pane.PNG('img/aavso_logo.png', width=200),
        pn.pane.PNG('img/neu_logo.png', width=200),
    ],
    theme_toggle=False,
    main=[

        pn.Tabs(
                ("Catalog", catalog),
                ("Summary", summary),
                ("Plot", plot),
                # ("Histogram", hist),
                ("Map", starmap),
                ("Description", description),
                # ("Plot2", plot2),
                active=2
                )

    ],
    header_background='#a93226'

).servable()

layout.show()
