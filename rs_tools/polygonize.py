#!/bin/python

import numpy as np
from shapely.geometry import Polygon as sPolygon
from matplotlib.patches import Polygon as mPolygon
import fiona
from osgeo import ogr
from skimage.measure import find_contours,label


def load_polygons(fn:str)->list:
    
    with fiona.open(fn, 'r', 'ESRI Shapefile') as output:
    
        coords = [poly['geometry']['coordinates'] for poly in output.values()]
    
    polygons = [sPolygon(np.squeeze(xy)) for xy in coords]

    return polygons

    
def plot_patch_image(ax, raster=None, contours=None):
    
    '''
    raster should be an image array.
    contours should be either a list of numpy arrays or shapely polygons.
    '''
    
    ax.axis('off')
    # show image
    if raster is not None:
        ax.imshow(raster)

    # Iterate over the polygons and plot each one
    for coords_ in contours:
        
        if isinstance(coords_,np.ndarray):
            coords = np.squeeze(coords_)
        else:
            coords = np.array(coords_.exterior.xy).transpose()

        color = np.random.random((1, 3))
        patch = mPolygon(coords, color=color, fill=True, alpha=0.3)
        ax.add_patch(patch)
        ax.scatter(coords[:,0],coords[:,1], s=15, color=color)

        
        
def polygonize(mask, convex=None, simplify_tolerance=None):
    
    '''
    masks takes input as the binary mask image.
    '''
    
    # convert data type
    if mask.dtype != 'uint8':
        polygon_raster = np.array(mask, dtype=np.uint8)
    else:
        polygon_raster = mask
    
    labels = label(polygon_raster)
    
    polygons=[]
    for lab in range(1,labels.max()+1):
        # Find contours in the binary image
        contours = find_contours(labels==lab)
        for con in contours:
            polygon = sPolygon(con[:,[1,0]])
            if simplify_tolerance is not None:
                polygon = polygon.simplify(tolerance=simplify_tolerance)
            if convex:
                polygons.append(polygon.convex_hull)
            else:
                polygons.append(polygon)

    return polygons


def save_polygons(out_fn, polygons, projection):
    
    # Save polygons to a shapefile
    schema = {
        'geometry': 'Polygon',
        'properties': {},
    }
    
    # proj = pyproj.Proj(projection)
    
    with fiona.open(out_fn, 'w', 'ESRI Shapefile', schema, crs=projection) as output:
        for polygon in polygons:
            output.write({
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [list(polygon.exterior.coords)],
                },
                'properties': {},
            })