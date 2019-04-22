# Development of continuous crustal monitoring system of seismic velocity using ambient noise

### Authors
Fernando Lawrens Hutapea (a,b,c) fernando@mine.kyushu-u.ac.jp <br/> 
Takeshi Tsuji (a,b) tsuji@i2cner.kyushu-u.ac.jp <br/> 
Tatsunori Ikeda (b) ikeda@i2cner.kyushu-u.ac.jp <br/> 
a Department of Earth Resources Engineering, Kyushu University, Fukuoka 819-0395, Japan <br />
b International Institute for Carbon-Neutral Energy Research (I2CNER), Kyushu University, Fukuoka 819-0395, Japan <br />
c Exploration and Engineering Seismology Research Group, Institute Technology of Bandung, Bandung 40116, Indonesia <br />



### Abstract 
To continuously monitor crustal behaviors associated with earthquakes, magmatic activities and other environmental effects (e.g., tides and precipitations), we have developed a Python-based system for continuous monitoring of seismic velocity by applying seismic interferometry and stretching interpolation to ambient-noise data. The system includes four main processing procedures to obtain spatio-temporal velocity changes: (1) preparing the data, (2) creating virtual seismograms between pairs of seismometer stations, (3) estimating temporal velocity variations from virtual seismograms, and (4) mapping spatio-temporal velocity variations. We developed a data-processing scheme that removes unstable stretching interpolation results by using the median absolute deviation technique and a median filter. To obtain velocity changes with high stability and high temporal resolution during long-term, we proposed the “sliding reference method” for calculation of seismic velocity. We also developed methods to select the optimum parameters for the monitoring system.  In this study, we mainly used ambient-noise data from nearly 100 Hi-net seismometer stations around Kyushu Island, southwest Japan. To reduce computation time for continuous monitoring, we applied parallel computation methods, such as shared memory and hybrid distributed memory parallelization. Finally, we developed a web application that displays spatio-temporal velocity changes. In our monitoring results, we identified velocity variation (e.g., pore pressure variation) that could be related to earthquake, aftershock and magmatic activities. 



### Pre-Requirements
1) Make sure your workstations use Linux and it can be accessed from the network. <br/> 
2) Download and install Python 3.6 from Anaconda Distribution (https://www.anaconda.com/distribution). <br/> 
3) Install Bokeh, Holoviews, Geoviews, and Panel <br/> .
`conda install -c pyviz/label/dev -c bokeh/label/dev holoviews panel  bokeh geoviews`



### Package Overview
In this package there are two procedures:<br/> 
1. Creating the web-application objects by using Holoviews, Geoviews, and Panel.<br/> 
2. Displaying the objects using bokeh as web-application by using Bokeh of Panel.<br/> 
All the code procedures has included in monitoring_web_app.py file. 
<br/> 
<br/> 

### Input Data Format
There are three files to create the monitoring object:
#### 1. The temporal_vel_tabular.npy
This file is a binnary file of numpy stuctured array that contain the temporal velocity changes for each station pair. There are 4 keys in this binnary file, starttime,  station, longitude, latitude, station pair (pair_name), pair longitude (pair_lon), pair latitude (pair_lat), and velocity changes (e_max). The following is the structure of this binnary file
```
dtype = [('starttime', '<M8[ms]'), ('station', '<U10'), ('latitude', '<f4'), ('longitude', '<f4'), ('e_max', '<f4'), ('pair_name', '<U20'), ('pair_lon', '<f4'), ('pair_lat', '<f4')]
```
#### 2. The spatio_temporal_vel_tabular.npy  
This file is a binnary file of numpy stuctured array that contain the spatio-temporal velocity changes. There are 4 keys in this binnary file, starttime, longitude, latitude, station, and velocity changes (e_max). The following is the structure of this binnary file
```
dtype = [('starttime', '<M8[ns]'), ('station', '<U10'), ('latitude', '<f4'), ('longitude', '<f4'), ('e_max', '<f4')]
```
#### 3. The spatio_temp_vel_grid.nc 
This file is a netcdf4 binarry data format that contains grid of spatio-temporal velocity changes from file no 2. There are four keys in this file starttime, longitude, latitude, and velocity changes. 

<br/> 
<br/> 
### How to Use
Please download all the codes and data, then put it in the same directory. 

##### 1. Creating Web-application Objects
This the example code (example_1.py) how to create the  web-application objects:
```
from monitoring_web_app import *

if __name__== "__main__":
  spatio_temporal_vel_data_grid_path = "./spatio_temp_vel_grid.nc"
  spatio_temporal_vel_data_tab_path = "./spatio_temporal_vel_tabular.npy", 
  temporal_velocity_point_data_path = "./temporal_vel_tabular.npy", 
  output_data_folder = "./web"
  make_all_object(spatio_temporal_vel_data_grid_path = spatio_temporal_vel_data_grid_path, 
                  spatio_temporal_vel_data_tab_path = spatio_temporal_vel_data_tab_path, 
                  temporal_velocity_point_data_path = temporal_velocity_point_data_path, 
                  output_data_folder = output_data_folder)

```

<br/> 
<br/> 

##### 2. Display The Web-Application as Bokeh or Panel Service
This the example code (example_2.py) to start the web-application
```
from monitoring_web_app import *

if __name__== "__main__":
    web_dir = "./web" ### the folder location of step no 1
    host = "127.0.0.1"
    port = 8080
    start_monitoring_web_app(host = host, port = port)

```
Please shutdown or configure your firewall (iptable) to allow other PC access IP and PORT of your workstation. Then, you can type this in your Linuex terminal:

`panel serve example_2.py `
or 
`bokeh serve example_2.py `
