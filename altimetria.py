#!/usr/bin/env python

import sys
import gpxpy
import argparse
import itertools
import numpy as np
import geopy.distance
from numpy.lib.stride_tricks import sliding_window_view
from collections import namedtuple

Point = namedtuple('Point', 'lat lon elev dist cumdist elevdiff grade')
Segment = namedtuple('Segment', 'start end len elev_start elev_gain grade')

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def distance_km(p1, p2):
    latlon1 = (p1.latitude, p1.longitude)
    latlon2 = (p2.latitude, p2.longitude)
    return geopy.distance.geodesic(latlon1, latlon2).km


def do(filename, output_file, wlen, segment_len):
    with open(filename) as f:
        gpx = gpxpy.parse(f)

    points = []
    segments = []
    segments.append(Segment(0,0,0,0,0,0))
    cumdist = 0
    for pair in pairwise(gpx.tracks[0].segments[0].points):
        p1, p2 = pair
        distance = distance_km(p1, p2)
        cumdist += distance
        elevdiff = p2.elevation - p1.elevation
        if distance != 0:
            grade = elevdiff / (distance*1000) * 100
        else:
            grade = 0
        points.append(Point(p2.latitude, p2.longitude, p2.elevation, distance, cumdist, elevdiff, grade))

        if cumdist >= segments[-1].end + segment_len/1000:
            start = segments[-1].end
            end = cumdist
            len = end-start
            elev_start = segments[-1].elev_start + segments[-1].elev_gain
            elev_gain = p2.elevation - elev_start
            grade = elev_gain / (len*1000) * 100
            segments.append(Segment(start, end, len, elev_start, elev_gain, grade))
    segments.pop(0)

    if output_file != '-':
        fd = open(output_file, 'w')
    else:
        fd = sys.stdout

    data = np.array(points)
    data[wlen-1:,6] = np.average(sliding_window_view(data[:,6], window_shape=wlen), axis=1)
    np.savetxt(fd, data, fmt='%.5f %.5f %d %.6f %.3f %.3f %d')

    np.savetxt(fd, segments, fmt='%.2f %.2f %.2f %d %d %d')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='GPX file name')
    parser.add_argument('-o', '--output', type=str, help='Output filename (default to stdout)', default='-')
    parser.add_argument('--wlen', type=int, help='Moving average window size for grade calculation', default=10)
    parser.add_argument('--segment', type=int, help='Segment length in meters', default=500)
    args = parser.parse_args()
   
    do(args.filename, args.output, args.wlen, args.segment) 

