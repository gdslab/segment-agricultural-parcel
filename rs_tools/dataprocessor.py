import os
from osgeo import gdal, ogr, osr
from .rs3 import LightImage
import numpy as np



class DataProcessor(LightImage):
    
    def __init__(self, fn):
        
        # inherite super class init method
        super().__init__(fn)
        # get filename
        path_name, extension = os.path.splitext(self.fn)
        self.path = path_name
        self.fid = path_name.split('/')[-1]
        
    def get_image(self):
        
        # Initialize numpy array
        image = np.zeros((self.nrow, self.ncol,self.nband), dtype=self.dtype)

        # Read file onto memory
        for i in range(self.nband):
            self.band = self.ds.GetRasterBand(i+1)
            image[:,:,i] = self.band.ReadAsArray(0, 0, self.ncol, self.nrow)
            
        return image

    def clip_vector_by_image_extent(self, vector_in_path, vector_out_path, field_name=''):
        # vector file format is ESRI geodatabse (.gdbtable)
        
        # format the extent coords
        extent = f"{self.ext_left} {self.ext_up} {self.ext_right} {self.ext_down}"
        # make clip command with ogr2ogr - default to shapefile format
        cmd = f"ogr2ogr -spat {extent} -clipsrc spat_extent {vector_out_path}/{self.fid}.shp {vector_in_path} {field_name} -f \"ESRI Shapefile\""
        # run system command
        os.system(cmd)

    def vector2raster(self, vector_in, raster_out_path, format='GTiff'):
        # Get layer name
        ds = ogr.Open(vector_in)
        layer = ds.GetLayer()
        layer_name = layer.GetName()
        # format the extent coords
        extent = f"{self.ext_left} {self.ext_up} {self.ext_right} {self.ext_down}"        
        cmd = f"gdal_rasterize -l {layer_name} -burn {1.0} -tr {abs(self.x_spacing)} {abs(self.y_spacing)} -init {0.0} -a_nodata {0.0} -te {extent} -ot UInt16 -of {format} {vector_in} {raster_out_path}/{self.fid}.{format2extension(format)}"
        # run system command
        print(f"Rasterizing '{layer_name}'")
        os.system(cmd)
        
    def warp(self, source_img, out_path, interp_method="near"):
        # source img requires Label class
        
        # get target crs
        target_crs = source_img.projection.GetAttrValue('AUTHORITY',1)
        # write command line
        cmd = f"gdalwarp -t_srs EPSG:{target_crs} -r {interp_method} -of GTiff {self.fn} {out_path}/{self.fid}.tif"
        # run system command
        print(f"Reprojecting FID '{self.fid}'")
        os.system(cmd)
        
    def clip_raster_by_image_extent(self, target_img, out_path):
        # check if the target image extent is within the source image extent
        if target_img.ext_left >= self.ext_left and target_img.ext_up <= self.ext_up and target_img.ext_right <= self.ext_right and target_img.ext_down >= self.ext_down:
            # write command line
            cmd = f"gdal_translate -projwin {target_img.ext_left} {target_img.ext_up} {target_img.ext_right} {target_img.ext_down} -of GTiff {self.fn} {out_path}/{target_img.fid}.tif"
            # run system command
            print(f"Saving FID '{target_img.fid}'")
            os.system(cmd)
        else:
            # print error and pass
            print(f"FID '{target_img.fid}' : Image out of extent")
            pass
        
    def resample(self, source_img, out_path, interp_method="near"):
        # source img requires Label class

        # write command line
        cmd = f"gdalwarp -r {interp_method} -tr {abs(source_img.x_spacing)} {abs(source_img.y_spacing)} -of GTiff {self.fn} {out_path}/{self.fid}.tif"
        # run system command
        print(f"Resampling FID '{self.fid}'")
        os.system(cmd)
        
    def save_as(self, out_format, out_dtype, out_path):
        
        # write command line
        cmd = f"gdal_translate -of {out_format} -ot {out_dtype} {self.fn} {out_path}/{self.fid}.{format2extension(out_format)}"
        # run system command
        print(f"Save FID: '{self.fid}' as {out_format} File")
        os.system(cmd)



def polygons2lines(polygon_path, line_path, filename):
    # vector format is ESRI shapefiles
    
    # open datasource
    ds = ogr.Open(os.path.join(polygon_path,filename))
    layer = ds.GetLayer()
    # create new vector file
    driver = ogr.GetDriverByName("ESRI Shapefile")
    outds = driver.CreateDataSource(os.path.join(line_path,filename))
    outlayer = outds.CreateLayer(filename[:-4], layer.GetSpatialRef())
    # read polygon and save as line to new file
    for feature in layer:
        # polygon to line
        geom = feature.GetGeometryRef()
        line = geom.Boundary()
        # set geometry to line
        feature.SetGeometry(line)
        # save feature
        outlayer.CreateFeature(feature)
    # close temporary files
    outds = outlayer = feature = None


def format2extension(format):
    if format == "GTiff":
        extension = "tif"
    elif format == "HFA":
        extension = "img"
    elif format == "BMP":
        extension = "bmp"
    elif format == "PNG":
        extension = "png"
    
    return extension