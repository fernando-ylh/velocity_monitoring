import numpy as np
import pandas as pd
import cartopy.crs as ccrs
from cartopy import crs
import geoviews as gv
import holoviews as hv
import geoviews.tile_sources as gts
import xarray as xr
import panel as pn
import os, sys, shutil, time, datetime
from collections import defaultdict

pn.extension()
gv.extension("bokeh", logo=False)
hv.extension("bokeh", logo=False)
hv.Dimension.type_formatters[np.datetime64] = '%Y-%m-%d'
gv.Dimension.type_formatters[np.datetime64] = '%Y-%m-%d'
    


#### Header Object #####
def make_header_html(header_html_path=None):
    logo = "https://www.kyushu-u.ac.jp/img/common_en/logo.png"
    title = '<p style="font-size:30px">Passive Seismic Monitoring System</p>'
#     creator = 'Created by: Fernando Lawrens Hutapea, Takeshi Tsuji, and Tatsunori Ikeda <br>'
    info = "(Ambient noise data is provided by National Research Institute for Earth Science and Disaster Prevention (NIED) Japan)"
    creator = 'Presently the monitoring result is updated weekly (Saturday) <br> Please use Firefox or Google Chrome or Microsoft Edge <br>'
    current = np.datetime64(datetime.datetime.now(), "s").astype(str) 
    last_update = "Last update: {} <br>".format(current) # today's date
    header = pn.Row(logo, pn.Spacer(width=30),
                     pn.Column(pn.Spacer(height=0), pn.Pane(title, height=16, width=900), 
                               pn.Spacer(height=18), pn.Pane(info, height=20, width=900), 
                               pn.Spacer(height=8), pn.Pane(creator, height=20,width=900), 
                               last_update)
                   )
    print("Finish Create Header {}".format(current))
    return(header)



#### Spatio Temporal Velocity Grid Object #####
def make_spatio_temporal_vel_grid_obj(date):
    vdims = [('e_max', 'Seismic Velocity Changes (%)')]
    kdims = [('latitude', 'Latitude'), ('longitude', 'Longitude')]
    slice_ds = hv.Dataset(spatio_temporal_vel_data_grid.sel(date=date), kdims, vdims)
    spatio_temporal_vel_grid_obj = slice_ds.to(gv.Image, [ "longitude", "latitude"], 
                                               "e_max", crs=ccrs.PlateCarree())
    opts = dict(alpha=0.8)
    opts.update(opts1)
    spatio_temporal_vel_grid_obj = spatio_temporal_vel_grid_obj.opts(**opts)
    print("make_spatio_temporal_vel_grid_obj {}".format(date))
    return(spatio_temporal_vel_grid_obj)


#### Spatio Temporal Velocity Point Object #####
def make_spatio_temporal_vel_point_obj(date):
    opts = dict(color='w', marker='v', size=3, line_color="r", tools=["hover"])
    idx = spatio_temporal_vel_data_tab_df["starttime"] == date
    emax_avg_df = spatio_temporal_vel_data_tab_df[idx]
    ds = gv.Dataset((emax_avg_df["longitude"],emax_avg_df["latitude"], 
                     emax_avg_df["e_max"], emax_avg_df["station"]),
                    ["Longitude", "Latitude"], ["Velocity Changes (%)","Station"], 
                    crs=crs.PlateCarree()
                   )
    vdims =[("e_max","Velocity Changes (%)"),"Station"]
    spatio_temporal_vel_point_obj = ds.to(gv.Points, ["Longitude", "Latitude"], crs=ccrs.PlateCarree())
    spatio_temporal_vel_point_obj = spatio_temporal_vel_point_obj.opts(**opts)
    print("make_spatio_temporal_vel_point_obj {}".format(date))
    return(spatio_temporal_vel_point_obj)


#### Spatio Temporal Velocity Curve Object #####
def make_spatio_temporal_vel_curve_obj(spatio_temporal_vel_data_tab_df):
    kdims = [('starttime', 'Date'), ('station', 'Station')]
    vdims = [("e_max", "Velocity Changes (%)")]
    emax_avg_ds = hv.Dataset(spatio_temporal_vel_data_tab_df, kdims, vdims)
    spatio_temporal_vel_curve_obj = emax_avg_ds.to(hv.Curve, "starttime", "e_max")
    return(spatio_temporal_vel_curve_obj)


#### Temporal Velocity Pair Path Object #####                
def make_temporal_vel_pair_path_obj(date):
    ttt = date.astype('datetime64[D]') 
    kdims=["Longitude", "Latitude"]
    vdims=[("e_max", "Velocity changes (%)"), "Pairname"]
    opts = dict(color='grey', alpha=0.5)
    temporal_vel_pair_path_obj = gv.Path(data_pair[ttt], crs=ccrs.PlateCarree())
    temporal_vel_pair_path_obj = temporal_vel_pair_path_obj.opts(**opts)
    print("make_temporal_vel_pair_path_obj {}".format(date))
    return(temporal_vel_pair_path_obj)


#### Temporal Velocity Pair Poin Object #####
def make_temporal_vel_pair_point_obj(date):
    ttt = date.astype('datetime64[D]') 
    kdims=["Longitude", "Latitude"]
    vdims=[("e_max", "Velocity changes (%)"), "Pairname"]
    opts = dict(color='e_max', cmap="jet_r", size=5, tools=["hover"], marker='s')
    opts.update(opts1)
    temporal_vel_pair_point_obj = gv.Points(data_mid_point_pair[ttt], kdims=kdims,
                                             vdims=vdims, crs=ccrs.PlateCarree())
    temporal_vel_pair_point_obj = temporal_vel_pair_point_obj.opts(**opts)
    print("make_temporal_vel_pair_point_obj {}".format(date))
    return(temporal_vel_pair_point_obj)


#### Create Monitoring Object ####
def make_all_object(spatio_temporal_vel_data_grid_path=None, spatio_temporal_vel_data_tab_path = None,
                         temporal_velocity_point_data_path = None, output_data_folder=None):
    script_name = "web_application"
    start_time = time.time()
    
    print("#### Process: monitoring_web_app_v1 (make_all_object)\n#### Status: START!!! \n")    
    if os.path.isfile(spatio_temporal_vel_data_grid_path) == False or spatio_temporal_vel_data_grid_path == None:
        sys.exit("#### Process: monitoring_web_app_v1 (make_all_object)\n#### Status: Stop spatio_temporal_vel_data_grid_path does not exist or None! \n{}\n")
    if os.path.isfile(spatio_temporal_vel_data_tab_path) == False or spatio_temporal_vel_data_tab_path == None:
        sys.exit("#### Process: monitoring_web_app_v1 (make_all_object)\n#### Status: Stop spatio_temporal_vel_data_tab_path does exist or None! \n{}\n")
    if os.path.isfile(temporal_velocity_point_data_path) == False or temporal_velocity_point_data_path == None:
        sys.exit("#### Process: monitoring_web_app_v1 (make_all_object)\n#### Status: Stoptemporal_velocity_point_data_path does not exist or None!\n{}\n")
    
    global opts1, opts2
    opts1 = dict(height=400, width=400, cmap="jet_r", colorbar_position="bottom",colorbar=True,             
                colorbar_opts={"title": "Seismic Velocity Changes(%)", "title_text_align":"left"},
                 zlim = (-0.5, 0.5)
                )
    opts2 = dict(height=400, width=400)
    
    #### Load spatio temporal grid data ####
    global spatio_temporal_vel_data_grid
    spatio_temporal_vel_data_grid = xr.open_dataset(spatio_temporal_vel_data_grid_path)
    spatio_temporal_vel_data_grid["e_max"] = spatio_temporal_vel_data_grid["e_max"].astype(np.float16) 
    
    #### Load spatio temporal tabular data ####
    global spatio_temporal_vel_data_tab, spatio_temporal_vel_data_tab_df
    spatio_temporal_vel_data_tab = np.load(spatio_temporal_vel_data_tab_path)
    spatio_temporal_vel_data_tab["e_max"] = spatio_temporal_vel_data_tab["e_max"] *100
    names = list(spatio_temporal_vel_data_tab.dtype.names)
    if 'index' in names:
        names.remove("index")
    spatio_temporal_vel_data_tab_df = pd.DataFrame({name:spatio_temporal_vel_data_tab[name] for name in names})
    
    #### Load temporal tabular data ####
    global temporal_velocity_point_data
    temporal_velocity_point_data = np.load(temporal_velocity_point_data_path)
    
    #### Make data for pair object ####
    global data_pair, data_mid_point_pair
    data_pair = defaultdict(list)
    data_mid_point_pair = defaultdict(list)
    times = np.unique(temporal_velocity_point_data["starttime"])
    times = times.astype('datetime64[D]')
    times_b = []
    for tt in times:
        result = temporal_velocity_point_data[temporal_velocity_point_data["starttime"] == tt]
        duplicate_check = []
        if(len(result) > 0):
            times_b.append(tt)
            for A_lon, A_lat, B_lon, B_lat, e, t, A_stn, B_stn in zip(result["longitude"], result["latitude"], 
                                                          result['pair_lon'], result['pair_lat'],
                                                          result["e_max"], result["starttime"],
                                                          result["station"], result["pair_name"]):
                pairname = [A_stn, B_stn[0:6]]
                pairname = sorted(pairname)
                pairname = '{}--{}'.format(pairname[0], pairname[1])
                if pairname not in duplicate_check:
                    duplicate_check.append(pairname)
                    buff1 = {'Longitude' : [A_lon, B_lon], 'Latitude' : [A_lat, B_lat],
                             "e_max": e * 100, "date": t, "Pairname": pairname
                            }
                    data_pair[tt].append(buff1)
                    buff2 = [np.mean([A_lon, B_lon]), np.mean([A_lat, B_lat]), e * 100, pairname]
                    data_mid_point_pair[tt].append(buff2)
    
    dates = np.unique(temporal_velocity_point_data["starttime"])
    
    ### Object 1
    spatio_temporal_vel_hm = gv.HoloMap({date:make_spatio_temporal_vel_grid_obj(date) *
                                         make_spatio_temporal_vel_point_obj(date) 
                                          for date in dates}, kdims="Date") 
    
    ### Object 2
    temporal_vel_pair_hm = gv.HoloMap({date:make_temporal_vel_pair_point_obj(date) * 
                                       make_temporal_vel_pair_path_obj(date) * 
                                       make_spatio_temporal_vel_point_obj(date)
                                       for date in dates}, kdims="Date")
    
    ### Object 3
    spatio_temporal_vel_curve_hm = make_spatio_temporal_vel_curve_obj(spatio_temporal_vel_data_tab_df)
    spatio_temporal_vel_curve_hm = spatio_temporal_vel_curve_hm.options(width=800)
    
    ### overlay object 1, 2, basemap
    monitoring_hm = (spatio_temporal_vel_hm + temporal_vel_pair_hm) * gts.EsriTerrain
    monitoring_hm = monitoring_hm.redim.range(e_max=(-0.5, 0.5))
    
    ### Object 4
    header = make_header_html()
    
    ### Export to html files
    if output_data_folder == None:
        output_data_folder = os.path.abspath('')
        os.makedirs(output_data_folder, exist_ok=True)

    monitoring_hm_path = os.path.join(output_data_folder, "monitoring_hm.html")
    hv.save(monitoring_hm, monitoring_hm_path, fmt='scrubber')

    spatio_temporal_vel_curve_hm_path =  os.path.join(output_data_folder, "curve_hm.html")
    hv.save(spatio_temporal_vel_curve_hm, spatio_temporal_vel_curve_hm_path)

    header_path = os.path.join(output_data_folder, "header.html")
    header.save(header_path)
    files = [monitoring_hm_path, spatio_temporal_vel_curve_hm_path, header_path]
    print("#### Process: monitoring_web_app_v1 (make_all_object)\n#### Status: Result HTML Files !!!\n{}\n".format(files))

    result = pn.Column(header, monitoring_hm,spatio_temporal_vel_curve_hm)
    ptime = time.time() - start_time   
    print("#### Process: monitoring_web_app_v1 (make_all_object)\n#### Status: FINISH!!! {}s \n".format(ptime))
    
    if result != None:
        return(result)


### Web Server ###       
def start_web_server(port = 80, web_dir = None):
    print("Creating HTTPD Server \n\n")
    def make_web_server(port = port, web_dir = web_dir):
        import http.server
        import socketserver
        import socket
        if web_dir == None:
            web_dir = os.path.abspath('')
        if os.path.isdir(web_dir) == False:
            os.makedirs(name=web_dir, exist_ok=True)
        os.chdir(web_dir)
        print(os.path.abspath(''))
        ### Start HTTPD Service
        try:   
            Handler = http.server.SimpleHTTPRequestHandler
            httpd = socketserver.TCPServer(("", port), Handler)
            print("Starting HTTPD at port", port)
            httpd.serve_forever()
        except OSError as e:
            hostname = socket.gethostname()
            if str(e) == '[Errno 98] Address already in use':
                print("HTTPD Already Running on {}".format(hostname))
    ### Start Web Server ###
    import threading
    threading.Thread(target=make_web_server, args=(port, web_dir)).start()


def start_monitoring_web_app(web_dir = web_dir, host = "127.0.0.1", port = 8080):
    import panel as pn
    start_web_server(port = port, web_dir = web_dir)
    ### Load monitoring object ###
    a = pn.pane.HTML("""<object width="1100" height="300" type="text/html" data="http://{}:{}/header.html"> </object>
        """.format(host, port))
    b = pn.pane.HTML("""<object width="1100" height="600" type="text/html" data="http://{}:{}/monitoring_hm.html"> </object>
        """.format(host, port))
    c = pn.pane.HTML("""<object width="1100" height="600" type="text/html" data="http://{}:{}/curve_hm.html"> </object>
        """.format(host, port))
    ###
    result = pn.Column(a, pn.Spacer(height=280), 
                       b, pn.Spacer(height=550),
                       c, pn.Spacer(height=600), 
                       width=1100, height=1800)
    result.servable()


if __name__ == "__main__":
    
    web_dir = "/home/fernando/data-2tb/hinet/jupyter_code/vel_mon_html_3/web"
    host = "127.0.0.1"
    port = 8080
    
    start_monitoring_web_app(host = host, port = port)

