#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 10:17:50 2016

@author: mapper
"""

import os
from osgeo import ogr
import argparse
import fnmatch

# Setup argument parsing.
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-f','--file',
                   action = 'store',
                   help = 'ENC file to survey.')
group.add_argument('-d','--directory',
                   action = 'store',
                   help = 'Directory of ENC files to survey.')
parser.add_argument('-v','--verbose',
                    action = 'count',
                    help = 'Verbose output, -vvv = more output')
parser.add_argument('-c','--comma',
                    action='store_true',
                    default=False,
                    help = 'Set the output delimiter to comma (default: \t)')
parser.add_argument('-l','--layer',
                    action='store',
                    help = 'Layer to Extract')
parser.add_argument('-F','--feature',
                    action='store',
                    help='Comma separated list of features to extract. This only works for scalar values')

class deep_obj:
    """ Method for finding deep obstacles (WL=3) that don't have a sounding."""
    def __init__(self, ENC_filename= '/home/mapper/Desktop/ENC_ROOT/US5NH01M/US5NH01M.000',
                 verbose = 0):
        self.ENC_filename = ENC_filename
        self.verbose = verbose
        self.Nrocks = 0
        self.Nwrecks = 0
        self.layerName = None
        self.featureName = None
        
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
        global comma
        # Get the name of the layer
        name = layer.GetName()
        if (name == 'UWTROC'):
            name = 'Rock'
            Nname = 1
            self.Nrocks += 1
        elif (name == 'WRECKS'):
            name = 'Wreck'
            self.Nwrecks += 1
            Nname = 2
        # Check to see if the feature has a sounding, and if it does not and is
        #   always underwater/submerged, then print the water level and 
        #   latitude and longitude.
        for i in range (layer.GetFeatureCount()):
            feat = layer.GetNextFeature()
            geom = feat.GetGeometryRef()
            # Some gemoetries do not have lat/long, producing "Incompatable geometry
            # for operation". Skip these. 
            if geom.GetX() == 0.0:
                if self.verbose >=2:
                    print "ERROR: {} ".format(self.ENC_filename)
                else:
                    continue
                
            if (feat.GetField('VALSOU')==None):
                WL_index = feat.GetField('WATLEV')
                if (WL_index == 3 or WL_index == 4 or WL_index == 5):
                    # WL = self.water_level(WL_index)
                    WL = WL_index
                    if verbose >=1:
                        if not comma:
                            print '{}\t{}\t{}\t{}\t{}'.format(os.path.basename(self.ENC_filename), Nname, WL,geom.GetX(),geom.GetY())
                        else:
                            print '{},{},{},{},{}'.format(os.path.basename(self.ENC_filename), Nname, WL,geom.GetX(),geom.GetY())
                            
                    else:
                        if not comma:
                            print '{}\t{}\t{}\t{}'.format(Nname, WL,geom.GetX(),geom.GetY())
                        else:
                            print '{},{},{},{}'.format(Nname, WL,geom.GetX(),geom.GetY())

                    #print '{} that {}, Lat: {} Long:{}'.format(name, WL, geom.GetX(), geom.GetY())

    def print_feature_info(self):
        pass
    
    def run(self):
        
        """ Actually run the method. """
        HasFeature = False
        ds = ogr.Open(self.ENC_filename)
        #rocks = ds.GetLayerByName('UWTROC')
        #wrecks = ds.GetLayerByName('WRECKS')
        
        #if rocks:
        #    self.deep_unknown_objs(rocks)
        #if wrecks:
        #    self.deep_unknown_objs(wrecks)

        #print(os.path.basename(self.ENC_filename))
        
        Nlayers = ds.GetLayerCount()
        if verbose >= 2:
            print("Found %d Layers." % Nlayers)
        
        for i in range(ds.GetLayerCount()):
            
            layer = ds.GetLayerByIndex(i)

            try:
                desc = layer.GetDescription()
                Nfeat = layer.GetFeatureCount()
                if verbose >= 2:
                    print("Found %d features in layer %s" % (Nfeat,desc))

            except:
                print("Error on layer " + str(i)) 
    
            # If 'dump' was specified just print all the layers found. 
            if self.layerName == 'dump':
                if self.featureName is None:
                    print("%s,%s" % 
                      (os.path.basename(self.ENC_filename),
                                        desc))
                    break
                
                

            # Extract the desired features from the desired layer. 
            if (desc == self.layerName or self.layerName == 'all'):

                if self.featureName == 'all':
                    #print("   LAYER:" + desc)

                    for j in range(Nfeat):
                        feat = layer.GetNextFeature()
                        print('   FEAT:' + str(feat.GetFID()))
                        for featid in feat.keys():
                            print('       ATTR:' + featid + ':' + feat.GetFieldAsString(featid))

                else:
                    #print("   LAYER:" + desc)
                    
                    #print("LAYER:" + desc)                    

                    for name in self.featureName:
                        for j in range(Nfeat):
                            feat = layer.GetNextFeature()
                            for featid in feat.keys():
                                if featid == name or name == 'all':
                                    HasFeature = True
                                    #print("   ATTR:" + featid + ':' + feat.GetFieldAsString(featid))
                                    geom = feat.GetGeometryRef()
                                    if geom is not None:
                                        poly = geom.ExportToIsoWkt()
                                    else:
                                        poly = ""
                                        
                                    print("%s,%s,%s,%s,%s" % 
                                          (os.path.basename(self.ENC_filename),
                                           desc,
                                           featid,
                                           feat.GetFieldAsString(featid),
                                           poly))
        
        
        # This prints the file name alone, even if the desired layer was not found.
        if not HasFeature:
            print(os.path.basename(self.ENC_filename))
            

if __name__ == "__main__":


    enc_files_to_process = []
    args = parser.parse_args()
    verbose = args.verbose    
    comma = args.comma
    
    
    if verbose >= 2:
        print("Arguments:")
        arguments = vars(args)
        for key, value in arguments.iteritems():
            print("\t%s:\t\t%s" % (key,str(value)))
    
    
    if args.file:
        enc_files_to_process.append(args.file)
        
    elif args.directory:
        directory = args.directory
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames,'US*.000'):
                enc_files_to_process.append(os.path.join(root,filename))
    
    for enc in enc_files_to_process:
        if verbose >= 2:
            print('Processing %s ' % enc)

        obj = deep_obj(ENC_filename = enc)
        obj.verbose = verbose
        obj.layerName = args.layer
        if args.feature is not None:
            obj.featureName = args.feature.split(',')
        obj.run()
        
