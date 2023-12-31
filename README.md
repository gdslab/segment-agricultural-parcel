# Installation




## Locate Plugin Folder

### Windows
```%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins```
### Mac
```~/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins```
### Linux
```~/.local/share/QGIS/QGIS3/profiles/default/python/plugins```




## Clone the Repository
```bash
git clone git@github.com:breadnbutter0/segment-agricultural-parcel.git
```




## Download the Checkpoint File
Download SAM checkpoint file
```bash
mkdir checkpoint & cd checkpoint
```

```bash
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -o sam_vit_h_4b8939.pth
```

(Optional) Download fast sam checkpoint file
```bash
gdown https://drive.google.com/u/0/uc?id=1m1sjY4ihXBU1fZXdQ-Xdj-mDltW-2Rqv
```





## For Linux/MacOS Users
Open the terminal and run following script

### Linux
```bash
cd /usr/bin
```

###  Mac
```bash
cd /Applications/QGIS.app/Contents/MacOS/bin
```

### Install Library Dependencies
```bash
./pip3 install segment-anything torch torchvision opencv-python fiona shapely
```







## For Windows Users

### Open OsGeo4W Shell
OsGeo4W Sheel can be found on ```Start -> All Programs -> OSGeo4W ```

### Install Library Dependencies
```PowerShell
pip3 install segment-anything torch torchvision opencv-python fiona shapely
```




## Activate Segment-Agricultural-Parcel Plugin

```Plugins -> Manage and Install Plugins..```


![activate_sap](activate.png)




# How to Run

## 









