#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# (c) Valik mailto:vasnake@gmail.com

r""" Map Feature Server module.
Featureserver realization for API
http://resources.arcgis.com/en/help/rest/apiref/fslayer.html

"""

import os
#import json  # http://pymotw.com/2/json/
import postgis


class DBLayerInfo(object):
    """ Information about layer DB structure:
    table name, geometry field name, OBJECTID field name
    """
    def __init__(self, tabname, geomfield, oidfield):
        self.tabname = tabname
        self.geomfield = geomfield
        self.oidfield = oidfield
#class DBLayerInfo(object):


class LayerInfo(DBLayerInfo):
    """ Information about layer:
    info about DB table; layer id, field aliases and other mentioned in spec
    http://resources.arcgis.com/en/help/rest/apiref/fslayer.html#response
    """
    def __init__(self, tabname='', geomfield='', oidfield=''):
        # json text for layer http://resources.arcgis.com/en/help/rest/apiref/fslayer.html
        self.lyrmeta = ''
        super(LayerInfo, self).__init__(tabname, geomfield, oidfield)

    def setDBInfo(self, tabname, geomfield, oidfield):
        """ Init DB part of layer info"""
        super(LayerInfo, self).__init__(tabname, geomfield, oidfield)

    def setAGInfo(self, jsontext):
        """ Init ArcGIS part of layer info """
        self.lyrmeta = jsontext

    def isValid(self):
        """ Check metadata validity """
        if not self.lyrmeta:
            return False
        if not (self.tabname and self.geomfield and self.oidfield):
            return False
        return True
#class LayerInfo(DBLayerInfo):


def layerMeta(layerid, filestor='c:/d/code/git/mapfeatureserver'):
    """ return JSON text for layer
    according http://resources.arcgis.com/en/help/rest/apiref/fslayer.html
    Return '' if file with layer metadata not exists.

    example http://vags101.algis.com/arcgis/rest/services/PATHING/FeatureServer/0?f=json
    or http://vags101.algis.com/arcgis/rest/services/PATHING/FeatureServer/0?f=pjson
    """
    fn = os.path.join(filestor, 'config', 'layer.%s.config.json' % layerid)
    if not os.path.exists(fn):
        return ''

    with open(os.path.abspath(fn)) as fo:
        res = fo.read()
        return res
#def layerMeta(layerid):


def getFields(ds, tabname, oidfname):
    """ Bridge to PostGIS.
    Extract fields spec in JSON format

    Args:
        ds: postgis.DataSource with db connection.cursor;
        tabname: db table name;
        oidfname: OBJECTID field name.

    Returns:
        JSON text with 'fields' structure according ArcGIS spec
        http://resources.arcgis.com/en/help/rest/apiref/fslayer.html
    """
    #if 0: ds = postgis.DataSource('')
    if isinstance(ds, postgis.DataSource):
        return postgis.tableFields4esri(ds, tabname, oidfname)
    raise TypeError('Unknown datasource type')
#def getFields(cur, tabname):


def getExtent(ds, tabname, fname):
    """ Bridge to PostGIS.
    Extract layer extent in JSON format.

    Args:
        ds: postgis.DataSource with db connection.cursor;
        tabname: db table name;
        fname: geometry field name.

    Returns:
        JSON text with 'extent' structure according ArcGIS spec
        http://resources.arcgis.com/en/help/rest/apiref/geometry.html#envelope
    """
    #if 0: ds = postgis.DataSource('')
    #assert isinstance(ds, postgis.DataSource)
    if isinstance(ds, postgis.DataSource):
        return postgis.layerRealExtent(ds, tabname, fname)
    raise TypeError('Unknown datasource type')
#def getExtent():