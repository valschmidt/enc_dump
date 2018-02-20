# README

    enc_dump
Enc_dump.py is a python script (build on GDAL) which extracts Layers, Features and Feature Attributes from Electronic Nautical Charts.

	usage: enc_dump.py [-h] [-f FILE | -d DIRECTORY] [-v] [-l LAYER] [-F FEATURE]

	Enc_dump will dump Layer, Feature and Feature Attributes from a US Electronic
	Nautical Chart (ENC). Enc_dump will parse data from an individual file, or
	recursively walk a directory of files parsing every ENC found. One may specify
	the layer and feature ID to extract, (or <all> for all of them) Output is
	written one feature attribute per line, with prepended file name, Layer,
	Feature ID and Feature Attribute name. If a geometry is associated with the
	attribute, it is prepended to the line as WKT.

	optional arguments:
	  -h, --help            show this help message and exit
	  -f FILE, --file FILE  ENC file to survey.
	  -d DIRECTORY, --directory DIRECTORY
                        Directory of ENC files to survey.
	  -v, --verbose         Verbose output, -vvv = more output
	  -l LAYER, --layer LAYER
	                        Layer to Extract, or "all" for all of them.
	  -F FEATURE, --feature FEATURE
                        Comma separated list of features to extract. This only
                        works for scalar values. ("all" for all of them)

> Written with [StackEdit](https://stackedit.io/).