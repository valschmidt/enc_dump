#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 10:17:50 2016

@author: mapper
"""

from osgeo import ogr

class deep_obj:
    """ Method for finding deep obstacles (WL=3) that don't have a sounding."""
    def __init__(self, ENC_filename= '/home/mapper/Desktop/ENC_ROOT/US5NH01M/US5NH01M.000'):
        self.ENC_filename = ENC_filename
        
    def water_level(self, index):
        """ This function converts the number stored in Water Level attribute 
            in the ENC to a string.
    
        Inputs:
            index - Index in the water level attribue
    
        Outputs:
            Water Level for the desired object
        """
        index = str(index)
        if index == '1':
            return 'is Partly Submerged at High Water'
        elif index =='2':
            return 'is Alyways Dry'
        elif index =='3':
            return 'is Always Underwater/Submerged'
        elif index =='4':
            return 'Covers and Uncovers'
        elif index =='5':
            return 'is Awash'
        elif index =='6':
            return 'is Subject to Inundation or Floating'
        elif index == '7':
            return 'is Floating'
        else:
            return 'is Unknown'
            
    def deep_unknown_objs(self, layer):
        """ This function checks to see if the inputed layer contains any
            of the features are deep and do not have a sounding.
        """
        # Get the name of the layer
        name = layer.GetName()
        if (name == 'UWTROC'):
            name = 'Rock'
        elif (name == 'WRECKS'):
            name = 'Wreck'
        
        # Check to see if the feature has a sounding, and if it does not and is
        #   always underwater/submerged, then print the water level and 
        #   latitude and longitude.
        for i in range (layer.GetFeatureCount()):
            feat = layer.GetNextFeature()
            geom = feat.GetGeometryRef()
            if (feat.GetField('VALSOU')==None):
                WL_index = feat.GetField('WATLEV')
                if (WL_index == 3):
                    WL = self.water_level(WL_index)
                    print '{} that {}, Lat: {} Long:{}'.format(name, WL, geom.GetX(), geom.GetY())
    
    def run(self):
        """ Actually run the method. """
        ds = ogr.Open(self.ENC_filename)
        rocks = ds.GetLayerByName('UWTROC')
        wrecks = ds.GetLayerByName('WRECKS')
        
        self.deep_unknown_objs(rocks)
        self.deep_unknown_objs(wrecks)

if __name__ == "__main__":
    obj = deep_obj()
    obj.run()