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
1) Make sure your workstation can be accessed from the network <br/> 
2) Download and install Python 3.6 from Anaconda Distribution <br/> 
3) Install Bokeh, Holoviews, Geoviews, and Panel <br/> 
`conda install -c pyviz/label/dev pyviz`


### Package Overview
In this package there are two procedures:<br/> 
1. Creating the web-application objects by using Holoviews, Geoviews, and Panel.<br/> 
2. Displaying the objects using bokeh as web-application by using Bokeh and Panel.<br/> 
All the procedures has included in monitoring_web_app.py file. There are three example files to create the monitoring object, spatio_temp_vel_grid.nc, spatio_temporal_vel_tabular.npy, and temporal_vel_tabular.npy. 

### How to Use
