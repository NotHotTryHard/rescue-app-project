"""
Core functions for the rescue application calculations.
This module contains various utilities and algorithms for geospatial calculations,
path finding, and visualization related to rescue operations.
"""

import matplotlib as mpl
import numpy as np
import numpy.matlib
import pandas as pd
from matplotlib import path
import geopy.distance
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import networkx as nx
import scipy
import json 
import time
import pickle


shape1x = np.array([700, 802, 980, 1014, 1183, 1440, 1993, 1716, 938, 700])
shape1y = np.array([375, 311, 265, 201, 151, 200, 287, 1184, 1099, 346])

shape13x = np.array([1993, 2351, 2407, 2516, 1716, 1993])
shape13y = np.array([287, 458, 449, 505, 1184, 287])

shape23x = np.array([2516, 2658, 2744, 2348, 2208, 1716, 2516])
shape23y = np.array([505, 580, 820, 1091, 1313, 1184, 505])

shape3x = np.array([2744, 2756, 2731, 2643, 2788, 2711, 2834, 2834, 2797, 2595, 2208, 2348, 2744])
shape3y = np.array([820, 964, 1010, 1062, 1195, 1237, 1328, 1445, 1500, 1531, 1313, 1091, 820])

shape21x = np.array([938, 1716, 2208, 2595, 2797, 2846, 2669, 2136, 1966, 1846, 1668, 1589, 1512, 1048, 938])
shape21y = np.array([1099, 1184, 1313, 1531, 1500, 1723, 2042, 2136, 1987, 1955, 1936, 2359, 2398, 1449, 1099])

shape30x = np.array([2669, 2612, 2450, 2312, 2058, 2061, 2017, 1903, 1717, 1589, 1668, 1846, 1966, 2136, 2669])
shape30y = np.array([2042, 2745, 2664, 2638, 2498, 2394, 2409, 2433, 2401, 2359, 1936, 1955, 1987, 2136, 2042])

shape19x = np.array([2669, 2846, 3068, 3196, 3325, 3222, 2669])
shape19y = np.array([2042, 1723, 1835, 1826, 1867, 2107, 2042])

shape0x = np.array([3222, 3325, 3445, 3794, 3881, 3881, 3841, 3882, 4010, 3977, 3445, 3222])
shape0y = np.array([2107, 1867, 1913, 1970, 2016, 2110, 2286, 2390, 2470, 2539, 2290, 2107])

shape22x = np.array([3222, 3445, 3977, 3886, 3861, 3895, 3798, 3696, 3666, 3714, 3630, 3567, 3520, 3407, 3367, 3222])
shape22y = np.array([2107, 2290, 2539, 2525, 2585, 2619, 2726, 2762, 2873, 2937, 3030, 2991, 2994, 2959, 2964, 2107])

shape10x = np.array([2669, 3222, 3367, 3244, 3110, 2784, 2612, 2669])
shape10y = np.array([2042, 2107, 2964, 2986, 2986, 2784, 2745, 2042])

#shapeNorthx = np.array([1716, 1561, 1011, 655, 1184, 2733, 2933, 1716])
#shapeNorthy = np.array([1692, 2498, 1470, 311, 85, 463, 1489, 1692])

#shapeSouthx = np.array([1716, 1561, 3581, 4052, 3957, 2933, 1716])
#shapeSouthy = np.array([1692, 2498, 3129, 2469, 1940, 1489, 1692])

#shapeZonex = np.array([1561, 1011, 655, 1184,  2733, 2933, 3917, 4052, 3581, 1561])
#shapeZoney = np.array([2498, 1470, 311, 85, 463, 1489, 1989, 2469, 3129, 2498])

shapeNorthx = np.array([1685, 1560, 998, 628, 1184, 2026, 2754, 3016, 2806, 2106, 1880, 1802, 1685])
shapeNorthy = np.array([1907, 2555, 1475, 289, 43, 149, 439, 1489, 1499, 1627, 1647, 1687, 1907])

shapeSouthx = np.array([1685, 1560, 3082, 3794, 4074, 4046, 3016, 2806, 2106, 1880, 1802, 1685])
shapeSouthy = np.array([1907, 2555, 3069, 3077, 2589, 1877, 1489, 1499, 1627, 1647, 1687, 1907])

shapeZonex = np.array([1560, 998, 628, 1184, 2026, 2754, 3016, 4046, 4074, 3794, 3082, 1560])
shapeZoney = np.array([2555, 1475, 289, 43, 149, 439, 1489, 1877, 2589, 3077, 3069, 2555])

shapeAspawnx = np.array([1465, 1647, 1784, 1681, 1624, 1445, 1465])
shapeAspawny = np.array([1545, 1610, 1725, 1928, 1910, 1587, 1545])

shapeA1x = np.array([965, 1647, 1778, 1685, 1560, 998, 965])
shapeA1y = np.array([1367, 1610, 1722, 1907, 2555, 1475, 1367])

shapeA4x = np.array([1685, 1560, 3082, 3794, 4074, 4062, 2187, 1807, 1685])
shapeA4y = np.array([1907, 2555, 3069, 3077, 2589, 2288, 2019, 1691, 1907])

shapeBspawnx = np.array([1802, 1685, 1848, 1927, 1802])
shapeBspawny = np.array([1687, 1907, 1960, 1793, 1687])

shapeB1x = np.array([1685, 1560, 2004, 1824, 1764, 1685])
shapeB1y = np.array([1907, 2555, 2716, 1783, 1763, 1907])

shapeB2x = np.array([1685, 1560, 998, 699, 1429, 1802,  1685])
shapeB2y = np.array([1907, 2555, 1475, 524, 1531, 1687, 1907])

shapeB5x = np.array([2004, 1824, 2095, 2098, 3909, 3794, 3082, 2004])
shapeB5y = np.array([2716, 1783, 1973, 2049, 2882, 3077, 3069, 2716])

shapeCspawnx = np.array([1848, 1927, 2093, 2059, 1848])
shapeCspawny = np.array([1960, 1793, 1926, 1996, 1960])

shapeC1x = np.array([1685, 1560, 2500, 2098, 2095, 1824, 1764, 1685])
shapeC1y = np.array([1907, 2555, 2880, 2054, 1973, 1783, 1763, 1907])

shapeDspawnx = np.array([1802, 1927, 2093, 2122, 2046, 1880, 1802])
shapeDspawny = np.array([1687, 1793, 1926, 1850, 1630, 1647, 1687])

shapeD1x = np.array([3817, 4046, 3016, 2806, 2106, 1880, 1802, 1812, 3817])
shapeD1y = np.array([3039, 1877, 1489, 1499, 1627, 1647, 1687, 1681, 3039])

shapeD2x = np.array([1786, 3082, 3794, 3817, 1812, 2113, 1786])
shapeD2y = np.array([2638, 3069, 3077, 3039, 1681, 1884, 2638])

shapeD3x = np.array([1685, 1560, 1786, 2113, 1812, 1802, 1685])
shapeD3y = np.array([1907, 2555, 2638, 1884, 1681, 1687, 1907])

shapeD4x = np.array([1685, 1560, 998, 699, 1802, 1685])
shapeD4y = np.array([1907, 2555, 1475, 524, 1687, 1907])

shapeEspawnx = np.array([1465, 1484, 2046, 1880, 1802, 1784, 1647, 1465])
shapeEspawny = np.array([1545, 1504, 1630, 1647, 1687, 1725, 1610, 1545])

shapeE2x = np.array([4074, 4046, 3016, 2806, 2106, 1880, 1802, 1812, 2131, 1931, 3082, 3794, 4074])
shapeE2y = np.array([2589, 1877, 1489, 1499, 1627, 1647, 1687, 1681, 2060, 2688, 3069, 3077, 2589])

shapeKronx = np.array([1434, 1552, 1594, 1665, 1701, 1709, 1678, 1665, 1717, 1752, 1731, 1779, 1873, 1860, 1852, 1872, 1899, 1938, 1938, 1978, 2092, 2111, 2123, 2166, 2144, 2060, 2065, 1992, 1934, 2016, 1903, 1832, 1781, 1719, 1618, 1443, 1434])
shapeKrony = np.array([1550, 1602, 1606, 1693, 1770, 1828, 1858, 1906, 1918, 1862, 1852, 1769, 1815, 1854, 1898, 1917, 1872, 1886, 1915, 1959, 2053, 2037, 1973, 1948, 1892, 1840, 1825, 1751, 1732, 1624, 1625, 1648, 1626, 1622, 1562, 1523, 1550])

shapeNorthShorex = np.array([697, 799, 911, 983, 1025, 1135, 1174, 1321, 1412, 1872, 2093, 2292, 2367, 2423, 2579, 2674, 2768, 2750, 2651, 2807, 2716, 2830, 2846, 2804])
shapeNorthShorey = np.array([370, 307, 304, 265, 178, 171, 146, 154, 188, 257, 318, 431, 455, 440, 540, 580, 862, 999, 1059, 1203, 1237, 1299, 1456, 1508])

shapeSouthShorex = np.array([2804, 2839, 2856, 2826, 2830, 2848, 3066, 3203, 3390, 3442, 3672, 3755, 3768, 3800, 3946, 3935, 3893, 3892, 3979, 3972, 3889, 3849, 3904, 3945, 3961, 3983, 3973, 4087, 4088, 3978, 3898, 3865, 3902, 3854, 3802, 3813, 3694, 3711, 3671, 3735, 3762, 3722, 3699, 3660, 3590, 3571, 3369, 3254, 3166, 3132, 2968, 2877, 2781, 2643, 2531, 2453, 2300, 2054, 2039, 2069, 2001, 1907, 1606, 1600, 1577, 1512])
shapeSouthShorey = np.array([1508, 1518, 1608, 1610, 1700, 1731, 1828, 1824, 1874, 1909, 1924, 1947, 1903, 1969, 1978, 2021, 2020, 2058, 2088,  2139, 2154, 2284, 2405, 2416, 2401, 2423, 2440, 2509, 2531, 2549, 2530, 2589, 2617, 2684, 2721, 2749, 2764, 2795, 2876, 2899, 2935, 2936, 2997, 3023, 3023, 2998, 2964, 2992, 2979, 3000, 2918, 2837, 2786, 2771, 2737, 2679, 2649, 2527, 2473, 2400, 2424, 2442, 2380, 2333, 2372, 2406])

shapeNorthxPrec = np.array([697, 799, 911, 983, 1025, 1135, 1174, 1321, 1412, 1872, 2093, 2292, 2367, 2423, 2579, 2674, 2768, 2750, 2651, 2807, 2716, 2830, 2846, 2804, 2806, 2106, 1880, 1802, 1685, 1600, 1577, 1512, 1049, 697])
shapeNorthyPrec = np.array([370, 307, 304, 265, 178, 171, 146, 154, 188, 257, 318, 431, 455, 440, 540, 580, 862, 999, 1059, 1203, 1237, 1299, 1456, 1508, 1499, 1627, 1647, 1687, 1907, 2333, 2372, 2406, 1450, 370])

shapeSouthxPrec = np.array([2804, 2839, 2856, 2826, 2830, 2848, 3066, 3203, 3390, 3442, 3672, 3755, 3768, 3800, 3946, 3935, 3893, 3892, 3979, 3972, 3889, 3849, 3904, 3945, 3961, 3983, 3973, 4087, 4088, 3978, 3898, 3865, 3902, 3854, 3802, 3813, 3694, 3711, 3671, 3735, 3762, 3722, 3699, 3660, 3590, 3571, 3369, 3254, 3166, 3132, 2968, 2877, 2781, 2643, 2531, 2453, 2300, 2054, 2039, 2069, 2001, 1907, 1606, 1600, 1685, 1802, 1880, 2106, 2806, 2804])
shapeSouthyPrec = np.array([1508, 1518, 1608, 1610, 1700, 1731, 1828, 1824, 1874, 1909, 1924, 1947, 1903, 1969, 1978, 2021, 2020, 2058, 2088,  2139, 2154, 2284, 2405, 2416, 2401, 2423, 2440, 2509, 2531, 2549, 2530, 2589, 2617, 2684, 2721, 2749, 2764, 2795, 2876, 2899, 2935, 2936, 2997, 3023, 3023, 2998, 2964, 2992, 2979, 3000, 2918, 2837, 2786, 2771, 2737, 2679, 2649, 2527, 2473, 2400, 2424, 2442, 2380, 2333, 1907, 1687, 1647, 1627, 1499, 1508])

shapeZonexPrec = np.array([697, 799, 911, 983, 1025, 1135, 1174, 1321, 1412, 1872, 2093, 2292, 2367, 2423, 2579, 2674, 2768, 2750, 2651, 2807, 2716, 2830, 2846, 2804, 2839, 2856, 2826, 2830, 2848, 3066, 3203, 3390, 3442, 3672, 3755, 3768, 3800, 3946, 3935, 3893, 3892, 3979, 3972, 3889, 3849, 3904, 3945, 3961, 3983, 3973, 4087, 4088, 3978, 3898, 3865, 3902, 3854, 3802, 3813, 3694, 3711, 3671, 3735, 3762, 3722, 3699, 3660, 3590, 3571, 3369, 3254, 3166, 3132, 2968, 2877, 2781, 2643, 2531, 2453, 2300, 2054, 2039, 2069, 2001, 1907, 1606, 1600, 1577, 1512, 1049, 697])
shapeZoneyPrec = np.array([370, 307, 304, 265, 178, 171, 146, 154, 188, 257, 318, 431, 455, 440, 540, 580, 862, 999, 1059, 1203, 1237, 1299, 1456, 1508, 1518, 1608, 1610, 1700, 1731, 1828, 1824, 1874, 1909, 1924, 1947, 1903, 1969, 1978, 2021, 2020, 2058, 2088,  2139, 2154, 2284, 2405, 2416, 2401, 2423, 2440, 2509, 2531, 2549, 2530, 2589, 2617, 2684, 2721, 2749, 2764, 2795, 2876, 2899, 2935, 2936, 2997, 3023, 3023, 2998, 2964, 2992, 2979, 3000, 2918, 2837, 2786, 2771, 2737, 2679, 2649, 2527, 2473, 2400, 2424, 2442, 2380, 2333, 2372, 2406, 1450, 370])

def shapeToPath(shapex, shapey):
    """
    Convert shape coordinates to a matplotlib Path object.
    
    Parameters:
        shapex (numpy.array): Array of x-coordinates
        shapey (numpy.array): Array of y-coordinates
    
    Returns:
        matplotlib.path.Path: Path object created from the coordinates
    """
    arr = []
    for i in range(np.size(shapex)):
        arr.append((shapex[i], shapey[i]))
    return path.Path(arr)


def MeshFromShapeEdge(shapex, shapey, n=100):
    """
    Create a mesh from shape edges with evenly distributed points.
    
    Parameters:
        shapex (numpy.array): Array of x-coordinates
        shapey (numpy.array): Array of y-coordinates
        n (int, optional): Number of points to generate. Defaults to 100.
    
    Returns:
        numpy.array: Array of mesh points
    """
    per = 0
    for i in range(1, np.size(shapex, axis=0)):
        dist = np.sqrt((shapex[i - 1] - shapex[i])**2 + (shapey[i - 1] - shapey[i])**2)
        per += dist
    dots = np.linspace(np.array([shapex[0], shapey[0]]), np.array([shapex[1], shapey[1]]), int(n * dist / per))
    for i in range(1, np.size(shapex, axis=0)):
        dist = np.sqrt((shapex[i - 1] - shapex[i])**2 + (shapey[i - 1] - shapey[i])**2)
        dots = np.vstack((dots, np.linspace(np.array([shapex[i - 1], shapey[i - 1]]), np.array([shapex[i], shapey[i]]), int(n * dist / per))))
    return dots


pathNorth = shapeToPath(shapeNorthx, shapeNorthy)
pathSouth = shapeToPath(shapeSouthx, shapeSouthy)
pathZone = shapeToPath(shapeZonex, shapeZoney)
pathNorthPrec = shapeToPath(shapeNorthxPrec, shapeNorthyPrec)
pathSouthPrec = shapeToPath(shapeSouthxPrec, shapeSouthyPrec)
pathZonePrec = shapeToPath(shapeZonexPrec, shapeZoneyPrec)
pathAspawn = shapeToPath(shapeAspawnx, shapeAspawny)
pathA1 = shapeToPath(shapeA1x, shapeA1y)
pathA4 = shapeToPath(shapeA4x, shapeA4y)
pathBspawn = shapeToPath(shapeBspawnx, shapeBspawny)
pathB1 = shapeToPath(shapeB1x, shapeB1y)
pathB2 = shapeToPath(shapeB2x, shapeB2y)
pathB5 = shapeToPath(shapeB5x, shapeB5y)
pathCspawn = shapeToPath(shapeCspawnx, shapeCspawny)
pathC1 = shapeToPath(shapeC1x, shapeC1y)
pathC2 = pathB2
pathDspawn = shapeToPath(shapeDspawnx, shapeDspawny)
pathD1 = shapeToPath(shapeD1x, shapeD1y)
pathD2 = shapeToPath(shapeD2x, shapeD2y)
pathD3 = shapeToPath(shapeD3x, shapeD3y)
pathD4 = shapeToPath(shapeD4x, shapeD4y)
pathEspawn = shapeToPath(shapeEspawnx, shapeEspawny)
pathE2 = shapeToPath(shapeE2x, shapeE2y)
pathE4 = pathD4
pathKron = shapeToPath(shapeKronx, shapeKrony)


def DegreesToDecimal(deg, min, sec):
    """
    Convert degrees, minutes, seconds to decimal degrees.
    
    Parameters:
        deg (float): Degrees
        min (float): Minutes
        sec (float): Seconds
    
    Returns:
        float: Decimal degrees
    """
    return deg + min/60 + sec/3600

def DecimalToDegrees(dec):
    """
    Convert decimal degrees to degrees, minutes, seconds.
    
    Parameters:
        dec (float): Decimal degrees
    
    Returns:
        tuple: (degrees, minutes, seconds)
    """
    return int(dec // 1), int((dec % 1) // (1/60)), int((dec % (1/60)) // (1/3600))

def DegreesToDecimalVec(degminsec):
    """
    Convert a tuple of (degrees, minutes, seconds) to decimal degrees.
    
    Parameters:
        degminsec (tuple): Tuple containing (degrees, minutes, seconds)
    
    Returns:
        float: Decimal degrees
    """
    deg = degminsec[0]
    min = degminsec[1]
    sec = degminsec[2]
    return deg + min/60 + sec/3600

def DecimalToPixel(latitude, longitude):
    """
    Convert decimal coordinates to pixel coordinates on the map.
    
    Parameters:
        latitude (float): Latitude in decimal degrees
        longitude (float): Longitude in decimal degrees
    
    Returns:
        tuple: (x, y) pixel coordinates
    """
    pinpoint1pix = [2270, 1820]
    pinpoint2pix = [3685, 1820]
    pinpoint3pix = [2270, 408]
    latpix = pinpoint1pix[1] + (latitude - DegreesToDecimal(60, 0, 0)) / DegreesToDecimal(0, 10, 0) * (pinpoint3pix[1] - pinpoint1pix[1])
    longpix = pinpoint1pix[0] + (longitude - DegreesToDecimal(29, 50, 0)) / DegreesToDecimal(0, 20, 0) * (pinpoint2pix[0] - pinpoint1pix[0])
    return int(longpix), int(latpix)


def PixelToDecimal(longpix, latpix):
    """
    Convert pixel coordinates to decimal coordinates.
    
    Parameters:
        longpix (int): X-coordinate in pixels
        latpix (int): Y-coordinate in pixels
    
    Returns:
        tuple: (latitude, longitude) in decimal degrees
    """
    pinpoint1pix = [2270, 1820]
    pinpoint2pix = [3685, 1820]
    pinpoint3pix = [2270, 408]
    latitude = (latpix - pinpoint1pix[1]) / (pinpoint3pix[1] - pinpoint1pix[1]) * DegreesToDecimal(0, 10, 0) + DegreesToDecimal(60, 0, 0)
    longitude =  (longpix - pinpoint1pix[0]) / (pinpoint2pix[0] - pinpoint1pix[0]) * DegreesToDecimal(0, 20, 0) + DegreesToDecimal(29, 50, 0)
    return latitude, longitude

def DecimalToPixelVec(latlong):
    """
    Convert a tuple of (latitude, longitude) to pixel coordinates.
    
    Parameters:
        latlong (tuple): Tuple containing (latitude, longitude) in decimal degrees
    
    Returns:
        tuple: (x, y) pixel coordinates
    """
    latitude = latlong[0]
    longitude = latlong[1]
    pinpoint1pix = [2270, 1820]
    pinpoint2pix = [3685, 1820]
    pinpoint3pix = [2270, 408]
    latpix = pinpoint1pix[1] + (latitude - DegreesToDecimal(60, 0, 0)) / DegreesToDecimal(0, 10, 0) * (pinpoint3pix[1] - pinpoint1pix[1])
    longpix = pinpoint1pix[0] + (longitude - DegreesToDecimal(29, 50, 0)) / DegreesToDecimal(0, 20, 0) * (pinpoint2pix[0] - pinpoint1pix[0])
    return int(longpix), int(latpix)


def PixelToDecimalVec(longlatpix):
    """
    Convert (x, y) pixel coordinates to decimal coordinates.
    
    Parameters:
        longlatpix (tuple): Tuple containing (x, y) pixel coordinates
    
    Returns:
        tuple: (latitude, longitude) in decimal degrees
    """
    latpix = longlatpix[0]
    longpix = longlatpix[1]
    pinpoint1pix = [2270, 1820]
    pinpoint2pix = [3685, 1820]
    pinpoint3pix = [2270, 408]
    latitude = (latpix - pinpoint1pix[1]) / (pinpoint3pix[1] - pinpoint1pix[1]) * DegreesToDecimal(0, 10, 0) + DegreesToDecimal(60, 0, 0)
    longitude =  (longpix - pinpoint1pix[0]) / (pinpoint2pix[0] - pinpoint1pix[0]) * DegreesToDecimal(0, 20, 0) + DegreesToDecimal(29, 50, 0)
    return latitude, longitude


#img2 = plt.imread("data/canvas_new_fish.png")
width = 4113
height = 3145

#fig, ax = plt.subplots()
#ax.imshow(img2, extent=[0, width, 0, height])
#ax.axis('equal')

n = 1000
spotDict = {}
#1
mean1 = [1123, -784 + height]
mean2 = [1152, -692 + height]
mean3 = [1173, -619 + height]
mean4 = [1199, -522 + height]
mean5 = [1221, -446 + height]

spotDict = {1:[100, [1, 0.2, 0.2, 0.2, 1]]}
cov = 4 * 100
cov1 = [[cov, 0], [0, cov]]
cov2 = [[0.2 * cov, 0], [0, 0.2 * cov]]
cov3 = [[0.2 * cov, 0], [0, 0.2 * cov]]
cov4 = [[0.2 * cov, 0], [0, 0.2 * cov]]
cov5 = [[cov, 0], [0, cov]]
spotDict[1] = [[mean1, mean2, mean3, mean4, mean5], [cov1, cov2, cov3, cov4, cov5], cov, [0, 1, 0.2, 0.2, 0.2, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean2, cov2, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean3, cov3, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean4, cov4, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean5, cov5, n)))

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#2
mean1 = [1540, -424 + height]
mean2 = [1638, -435 + height]
mean3 = [1728, -446 + height]
mean4 = [1838, -463 + height]
mean5 = [1959, -486 + height]

cov = 4 * 100
cov1 = [[cov, 0], [0, cov]]
cov2 = [[0.2 * cov, 0], [0, 0.2 * cov]]
cov3 = [[cov, 0], [0, cov]]
cov4 = [[0.2 * cov, 0], [0, 0.2 * cov]]
cov5 = [[cov, 0], [0, cov]]
spotDict[2] = [[mean1, mean2, mean3, mean4, mean5], [cov1, cov2, cov3, cov4, cov5], cov, [0, 1, 0.2, 1, 0.2, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean2, cov2, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean3, cov3, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean4, cov4, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean5, cov5, n)))

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#3
mean1 = [2331, -569 + height]

cov = 4 * 100
cov1 = [[cov, 0], [0, cov]]
spotDict[3] = [[mean1], [cov1], cov, [0, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#4
mean1 = [2209, -1179 + height]

cov = 4 * 800
cov1 = [[cov, 0], [0, cov]]
spotDict[4] = [[mean1], [cov1], cov, [0, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#5
mean1 = [1667, -1298 + height]

cov = 4 * 400
cov1 = [[cov, 0], [0, cov]]
spotDict[5] = [[mean1], [cov1], cov, [0, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#6
mean1 = [2637, -927 + height]
mean2 = [2585, -1144 + height]
mean3 = [2441, -924 + height]
mean4 = [2562, -968 + height]

cov = 4 * 100
cov1 = [[cov, 0], [0, cov]]
cov2 = [[cov, 0], [0, cov]]
cov3 = [[cov, 0], [0, cov]]
cov4 = [[1.5 * cov, 0], [0, 1.5 * cov]]
spotDict[6] = [[mean1, mean2, mean3, mean4], [cov1, cov2, cov3, cov4], cov, [0, 1, 1, 1, 1.5]]

tmp = np.random.multivariate_normal(mean1, cov1, n)
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean2, cov2, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean3, cov3, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean4, cov4, n)))

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#7
#~~~~~вне нашей зоны~~~~~

#8
mean1 = [3021, -1937 + height]
mean2 = [3117, -1969 + height]
mean3 = [3224, -2009 + height]

cov = 4 * 100
cov1 = [[cov, 0], [0, cov]]
cov2 = [[0.4 * cov, 0], [0, 0.4 * cov]]
cov3 = [[cov, 0], [0, cov]]
spotDict[8] = [[mean1, mean2, mean3], [cov1, cov2, cov3], cov, [0, 1, 0.4, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean2, cov2, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean3, cov3, n)))

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#9
mean1 = [2184, -1612 + height]
mean2 = [2279, -1594 + height]
mean3 = [2404, -1573 + height]
mean4 = [2520, -1580 + height]
mean5 = [2621, -1655 + height]

cov = 4 * 100
cov1 = [[cov, 0], [0, cov]]
cov2 = [[cov, 0], [0, cov]]
cov3 = [[cov, 0], [0, cov]]
cov4 = [[cov, 0], [0, cov]]
cov5 = [[cov, 0], [0, cov]]
spotDict[9] = [[mean1, mean2, mean3, mean4, mean5], [cov1, cov2, cov3, cov4, cov5], cov, [0, 1, 1, 1, 1, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean2, cov2, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean3, cov3, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean4, cov4, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean5, cov5, n)))

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#10
shift = 25
mean1 = [1210 - shift, -1504 + height]
mean2 = [1172 - shift , -1399 + height]
mean3 = [1139 - shift, -1300 + height]

cov = 4 * 170
cov1 = [[cov, 0], [0, cov]]
cov2 = [[0.4 * cov, 0], [0, 0.4 * cov]]
cov3 = [[cov, 0], [0, cov]]
spotDict[10] = [[mean1, mean2, mean3], [cov1, cov2, cov3], cov, [0, 1, 0.4, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean2, cov2, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean3, cov3, n)))

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#11
mean1 = [1607, -2288 + height]
mean2 = [1637, -2159 + height]
mean3 = [1659, -2036 + height]

cov = 4 * 100
cov1 = [[0.25 * cov, 0], [0, 0.25 * cov]]
cov2 = [[cov, 0], [0, cov]]
cov3 = [[0.25 * cov, 0], [0, 0.25 * cov]]
spotDict[11] = [[mean1, mean2, mean3], [cov1, cov2, cov3], cov, [0, 0.25, 1, 0.25]]

tmp = np.random.multivariate_normal(mean1, cov1, n)
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean2, cov2, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean3, cov3, n)))

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#12
mean1 = [2173, -2343 + height]
mean2 = [2298, -2376 + height]
mean3 = [2437, -2416 + height]
mean4 = [2552, -2466 + height]
mean5 = [2635, -2508 + height]
mean6 = [2745, -2579 + height]

cov = 4 * 145
cov1 = [[cov, 0], [0, cov]]
cov2 = [[0.4 * cov, 0], [0, 0.4 * cov]]
cov3 = [[cov, 0], [0, cov]]
cov4 = [[0.25 * cov, 0], [0, 0.25 * cov]]
cov5 = [[0.15 * cov, 0], [0, 0.15 * cov]]
cov6 = [[cov, 0], [0, cov]]
spotDict[12] = [[mean1, mean2, mean3, mean4, mean5, mean6], [cov1, cov2, cov3, cov4, cov5, cov6], cov, [0, 1, 0.4, 1, 0.25, 0.15, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean2, cov2, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean3, cov3, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean4, cov4, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean5, cov5, n)))
tmp = np.concatenate((tmp, np.random.multivariate_normal(mean6, cov6, n)))

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#13
mean1 = [2443, -2143 + height]

cov = 4 * 120
cov1 = [[cov, 0], [0, cov]]
spotDict[13] = [[mean1], [cov1], cov, [0, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#14
mean1 = [3287, -2676 + height]

cov = 4 * 120
cov1 = [[cov, 0], [0, cov]]
spotDict[14] = [[mean1], [cov1], cov, [0, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#15
mean1 = [3551, -2808 + height]

cov = 4 * 120
cov1 = [[cov, 0], [0, cov]]
spotDict[15] = [[mean1], [cov1], cov, [0, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#16
mean1 = [3624, -2607 + height]

cov = 4 * 100
cov1 = [[cov, 0], [0, cov]]
spotDict[16] = [[mean1], [cov1], cov, [0, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#17
mean1 = [1493, -1698 + height]

cov = 4 * 100
cov1 = [[cov, 0], [0, cov]]
spotDict[17] = [[mean1], [cov1], cov, [0, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)

#18
mean1 = [3473 + 25, -2033 + height]

cov = 4 * 100
cov1 = [[cov, 0], [0, cov]]
spotDict[18] = [[mean1], [cov1], cov, [0, 1]]

tmp = np.random.multivariate_normal(mean1, cov1, n)

#plt.plot(tmp[:, 0], tmp[:, 1], '.', alpha=0.5)
#plt.rcParams['figure.figsize'] = (9, 6)
#plt.show()


def GenSpotPts(n, i, dict=spotDict):
    """
    Generate spot points based on predefined locations.
    
    Parameters:
        n (int): Number of points to generate
        i (int): Index of the spot location to use
        dict (dict, optional): Dictionary containing spot information. Defaults to spotDict.
    
    Returns:
        tuple: (x, y) arrays of generated points or None if invalid parameters
    """
    if i+1 == 7 or n == 0:
        return None

    spotInfo = dict[i + 1]
    weightsLocal = np.array(spotInfo[3])
    intervalsLocal = np.cumsum(weightsLocal)
    sampleLocal = np.random.rand(n) * np.sum(weightsLocal)
    countLocal = []
    for j in range(np.size(weightsLocal) - 1):
        countLocal.append(np.size(sampleLocal[(sampleLocal > intervalsLocal[j]) * (sampleLocal < intervalsLocal[j + 1])]))
    pts = np.array([])

    means = np.array(spotInfo[0])
    covs = np.array(spotInfo[1])

    x = np.array([])
    y = np.array([])
    for i in range(0, means.shape[0]):
        xtmp, ytmp = np.random.multivariate_normal(means[i], covs[i], countLocal[i]).T
        x = np.append(x, xtmp, axis=0)
        y = np.append(y, ytmp, axis=0)
    return x, y


def GenWinterPts(n, dict=spotDict, numbers=[]):
    """
    Generate winter points based on predefined locations and probabilities.
    
    Parameters:
        n (int): Number of points to generate
        dict (dict, optional): Dictionary containing spot information. Defaults to spotDict.
        numbers (list, optional): List of specific spot indices to use. Defaults to [].
    
    Returns:
        tuple: (x, y) arrays of generated points
    """
    spotWeights = np.array([0, (50 + 500)/2, (500 + 700)/2, (30 + 200)/2, (100 + 1000)/2,
     (100 + 1000)/2, (30 + 150)/2, (50 + 500)/2, (20 + 300)/2, (100 + 2000)/2,
      (100 + 1000)/2, (50 + 500)/2, (50 + 600)/2, (10 + 100)/2, (20 + 200)/2,
       (50 + 300)/2, (10 + 150)/2, (50 + 500)/2, (5 + 200)/2])
    intervals = np.cumsum(spotWeights)
    sample = np.random.rand(n) * np.sum(spotWeights)

    count = []
    for i in range(np.size(spotWeights) - 1):
        count.append(np.size(sample[(sample > intervals[i]) * (sample < intervals[i + 1])]))
    # print(count)

    x = np.array([])
    y = np.array([])
    if len(numbers) == 0:
        for i in range(0, np.size(count)):
            if i+1 == 7 or count[i] == 0:
                continue
            xtmp, ytmp = GenSpotPts(count[i], i, dict)
            x = np.append(x, xtmp, axis=0)
            y = np.append(y, ytmp, axis=0)
    else:
        numbers = np.array(numbers) - 1
        for i in numbers:
            if i+1 == 7 or count[i] == 0:
                continue
            xtmp, ytmp = GenSpotPts(count[i], i, dict)
            x = np.append(x, xtmp, axis=0)
            y = np.append(y, ytmp, axis=0)
    return x, y


def drawPts(x, y):
    """
    Draw points on the map.
    
    Parameters:
        x (numpy.array): Array of x-coordinates
        y (numpy.array): Array of y-coordinates
    """
    img = plt.imread("data/canvas_new_fish.png")
    width = 4113
    height = 3145

    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, width, 0, height])
    ax.axis('equal')

    plt.plot(x, y, '.', alpha=0.5)


pinpoint1pix = (862, 1111)
pinpoint2pix = (1569, 1111)
pinpoint3pix = (862, 408)
vertMetersInPix = geopy.distance.geodesic(PixelToDecimalVec(pinpoint1pix), PixelToDecimalVec(pinpoint3pix)).km / (pinpoint1pix[1] - pinpoint3pix[1])
horzMetersInPix = geopy.distance.geodesic(PixelToDecimalVec(pinpoint1pix), PixelToDecimalVec(pinpoint2pix)).km / (pinpoint2pix[0] - pinpoint1pix[0])

def distPointToPoint(pt1pix, pt2pix):
    """
    Calculate distance between two points in kilometers.
    
    Parameters:
        pt1pix (numpy.array): First point coordinates
        pt2pix (numpy.array): Second point coordinates
    
    Returns:
        float: Distance in kilometers
    """
    return np.sqrt(np.sum(((np.array([pt1pix]) - np.array([pt2pix])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]

def distPointToPointArr(pt1pix, pt2pix):
    """
    Calculate distance between a point and an array of points in kilometers.
    
    Parameters:
        pt1pix (numpy.array): Point coordinates
        pt2pix (numpy.array): Array of point coordinates
    
    Returns:
        float: Distance in kilometers
    """
    return np.sqrt(np.sum(((np.array([pt1pix]) - pt2pix) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]

def distPointToArray(pt1pix, arrpix):
    """
    Calculate distances from a point to an array of points in kilometers.
    
    Parameters:
        pt1pix (numpy.array): Point coordinates
        arrpix (numpy.array): Array of point coordinates
    
    Returns:
        numpy.array: Array of distances in kilometers
    """
    return np.sqrt(np.sum(((arrpix - pt1pix) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))

def DotsFromSegment(pt1, pt2, n=40):
    """
    Generate evenly spaced dots along a line segment.
    
    Parameters:
        pt1 (numpy.array): Start point coordinates
        pt2 (numpy.array): End point coordinates
        n (int, optional): Number of dots to generate. Defaults to 40.
    
    Returns:
        numpy.array: Array of dot coordinates
    """
    return np.linspace(pt1, pt2, n)

def nodeFromIndex(i, j, px):
    """
    Convert 2D grid indices to a 1D node index.
    
    Parameters:
        i (int): Row index
        j (int): Column index
        px (int): Width of the grid
    
    Returns:
        int: Node index
    """
    return i * px + j


def makeHalfGraph(mask2d, mesh, checkFreq=40): 
    """
    Create a graph from a 2D mask, connecting adjacent nodes with valid paths.
    
    Parameters:
        mask2d (numpy.array): 2D boolean mask indicating valid nodes
        mesh (numpy.array): Array of node coordinates
        checkFreq (int, optional): Frequency of intermediate points for path validation. Defaults to 40.
    
    Returns:
        networkx.Graph: Graph with nodes and weighted edges
    """
    shape = np.shape(mask2d)
    px = shape[1]
    py = shape[0]
    G = nx.Graph()
    
    for i in range(py):
        for j in range(px):
            fromInd = nodeFromIndex(i, j, px)
            pt1 = mesh[fromInd]
            if mask2d[i][j] == True:
                if i != 0:
                    if mask2d[i - 1][j] == True:
                        toInd = nodeFromIndex(i - 1, j, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j != px - 1:
                    if mask2d[i][j + 1] == True:
                        toInd = nodeFromIndex(i, j + 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i != py - 1:
                    if mask2d[i + 1][j] == True:
                        toInd = nodeFromIndex(i + 1, j, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j != 0:
                    if mask2d[i][j - 1] == True:
                        toInd = nodeFromIndex(i, j - 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i != 0 and j != px - 1:
                    if mask2d[i - 1][j + 1] == True:
                        toInd = nodeFromIndex(i - 1, j + 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j != px - 1 and i != py - 1:
                    if mask2d[i + 1][j + 1] == True:
                        toInd = nodeFromIndex(i + 1, j + 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i != py - 1 and j != 0:
                    if mask2d[i + 1][j - 1] == True:
                        toInd = nodeFromIndex(i + 1, j - 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j != 0 and i != 0:
                    if mask2d[i - 1][j - 1] == True:
                        toInd = nodeFromIndex(i - 1, j - 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                #2й уровень
                if i >= 2 and j != px - 1:
                    if mask2d[i - 2][j + 1] == True:
                        toInd = nodeFromIndex(i - 2, j + 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i >= 2 and j != 0:
                    if mask2d[i - 2][j - 1] == True:
                        toInd = nodeFromIndex(i - 2, j - 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j <= px - 3 and i != py - 1:
                    if mask2d[i + 1][j + 2] == True:
                        toInd = nodeFromIndex(i + 1, j + 2, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j <= px - 3 and i != 0:
                    if mask2d[i - 1][j + 2] == True:
                        toInd = nodeFromIndex(i - 1, j + 2, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i <= py - 3 and j != 0:
                    if mask2d[i + 2][j - 1] == True:
                        toInd = nodeFromIndex(i + 2, j - 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i <= py - 3 and j != px - 1:
                    if mask2d[i + 2][j + 1] == True:
                        toInd = nodeFromIndex(i + 2, j + 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j >= 2 and i != 0:
                    if mask2d[i - 1][j - 2] == True:
                        toInd = nodeFromIndex(i - 1, j - 2, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j >= 2 and i != py - 1:
                    if mask2d[i + 1][j - 2] == True:
                        toInd = nodeFromIndex(i + 1, j - 2, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                #3й уровень
                if i > 2 and j < px - 1:
                    if mask2d[i - 3][j + 1] == True:
                        toInd = nodeFromIndex(i - 3, j + 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i > 2 and j < px - 2:
                    if mask2d[i - 3][j + 2] == True:
                        toInd = nodeFromIndex(i - 3, j + 2, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i > 2 and j > 0:
                    if mask2d[i - 3][j - 1] == True:
                        toInd = nodeFromIndex(i - 3, j - 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i > 2 and j > 1:
                    if mask2d[i - 3][j - 2] == True:
                        toInd = nodeFromIndex(i - 3, j - 2, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j < px - 3 and i < py - 1:
                    if mask2d[i + 1][j + 3] == True:
                        toInd = nodeFromIndex(i + 1, j + 3, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j < px - 3 and i < py - 2:
                    if mask2d[i + 2][j + 3] == True:
                        toInd = nodeFromIndex(i + 2, j + 3, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j < px - 3 and i > 0:
                    if mask2d[i - 1][j + 3] == True:
                        toInd = nodeFromIndex(i - 1, j + 3, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j < px - 3 and i > 1:
                    if mask2d[i - 2][j + 3] == True:
                        toInd = nodeFromIndex(i - 2, j + 3, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i < py - 3 and j > 0:
                    if mask2d[i + 3][j - 1] == True:
                        toInd = nodeFromIndex(i + 3, j - 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i < py - 3 and j > 1:
                    if mask2d[i + 3][j - 2] == True:
                        toInd = nodeFromIndex(i + 3, j - 2, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i < py - 3 and j < px - 1:
                    if mask2d[i + 3][j + 1] == True:
                        toInd = nodeFromIndex(i + 3, j + 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i < py - 3 and j < px - 2:
                    if mask2d[i + 3][j + 2] == True:
                        toInd = nodeFromIndex(i + 3, j + 2, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j > 2 and i > 0:
                    if mask2d[i - 1][j - 3] == True:
                        toInd = nodeFromIndex(i - 1, j - 3, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j > 2 and i > 1:
                    if mask2d[i - 2][j - 3] == True:
                        toInd = nodeFromIndex(i - 2, j - 3, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j > 2 and i < py - 1:
                    if mask2d[i + 1][j - 3] == True:
                        toInd = nodeFromIndex(i + 1, j - 3, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j > 2 and i < py - 2:
                    if mask2d[i + 2][j - 3] == True:
                        toInd = nodeFromIndex(i + 2, j - 3, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                #4й уровень
                if i > 3 and j < px - 1:
                    if mask2d[i - 4][j + 1] == True:
                        toInd = nodeFromIndex(i - 4, j + 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i > 3 and j < px - 2:
                    if mask2d[i - 4][j + 2] == True:
                        toInd = nodeFromIndex(i - 3, j + 2, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i > 3 and j < px - 3:
                    if mask2d[i - 4][j + 3] == True:
                        toInd = nodeFromIndex(i - 3, j + 3, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i > 3 and j > 0:
                    if mask2d[i - 4][j - 1] == True:
                        toInd = nodeFromIndex(i - 4, j - 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i > 3 and j > 1:
                    if mask2d[i - 4][j - 2] == True:
                        toInd = nodeFromIndex(i - 4, j - 2, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i > 3 and j > 2:
                    if mask2d[i - 4][j - 3] == True:
                        toInd = nodeFromIndex(i - 4, j - 3, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j < px - 4 and i < py - 1:
                    if mask2d[i + 1][j + 4] == True:
                        toInd = nodeFromIndex(i + 1, j + 4, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j < px - 4 and i < py - 2:
                    if mask2d[i + 2][j + 4] == True:
                        toInd = nodeFromIndex(i + 2, j + 4, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j < px - 4 and i < py - 3:
                    if mask2d[i + 3][j + 4] == True:
                        toInd = nodeFromIndex(i + 3, j + 4, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j < px - 4 and i > 0:
                    if mask2d[i - 1][j + 4] == True:
                        toInd = nodeFromIndex(i - 1, j + 4, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j < px - 4 and i > 1:
                    if mask2d[i - 2][j + 4] == True:
                        toInd = nodeFromIndex(i - 2, j + 4, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j < px - 4 and i > 2:
                    if mask2d[i - 3][j + 4] == True:
                        toInd = nodeFromIndex(i - 3, j + 4, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i < py - 4 and j > 0:
                    if mask2d[i + 4][j - 1] == True:
                        toInd = nodeFromIndex(i + 4, j - 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i < py - 4 and j > 1:
                    if mask2d[i + 4][j - 2] == True:
                        toInd = nodeFromIndex(i + 4, j - 2, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i < py - 4 and j > 2:
                    if mask2d[i + 4][j - 3] == True:
                        toInd = nodeFromIndex(i + 4, j - 3, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i < py - 4 and j < px - 1:
                    if mask2d[i + 4][j + 1] == True:
                        toInd = nodeFromIndex(i + 4, j + 1, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i < py - 4 and j < px - 2:
                    if mask2d[i + 4][j + 2] == True:
                        toInd = nodeFromIndex(i + 4, j + 2, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if i < py - 4 and j < px - 3:
                    if mask2d[i + 4][j + 3] == True:
                        toInd = nodeFromIndex(i + 4, j + 3, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j > 3 and i > 0:
                    if mask2d[i - 1][j - 4] == True:
                        toInd = nodeFromIndex(i - 1, j - 4, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j > 3 and i > 1:
                    if mask2d[i - 2][j - 4] == True:
                        toInd = nodeFromIndex(i - 2, j - 4, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j > 3 and i > 2:
                    if mask2d[i - 3][j - 4] == True:
                        toInd = nodeFromIndex(i - 3, j - 4, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j > 3 and i < py - 1:
                    if mask2d[i + 1][j - 4] == True:
                        toInd = nodeFromIndex(i + 1, j - 4, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j > 3 and i < py - 2:
                    if mask2d[i + 2][j - 4] == True:
                        toInd = nodeFromIndex(i + 2, j - 4, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                if j > 3 and i < py - 3:
                    if mask2d[i + 3][j - 4] == True:
                        toInd = nodeFromIndex(i + 3, j - 4, px)
                        pt2 = mesh[toInd]
                        dots = DotsFromSegment(pt1, pt2, checkFreq)
                        if not pathKron.contains_points(dots).any():
                            weight = distPointToPoint(pt1, pt2)
                            G.add_edge(fromInd, toInd, weight=weight)
                            #if toInd in dict:
                            #    dict[toInd].append(fromInd)
                            #else:
                            #    dict[toInd] = [fromInd]
                #l-й уровень
                for l in range(5, 50):
                    if i >= l and j != px - 1:
                        if mask2d[i - l][j + 1] == True:
                            toInd = nodeFromIndex(i - l, j + 1, px)
                            pt2 = mesh[toInd]
                            dots = DotsFromSegment(pt1, pt2, checkFreq)
                            if not pathKron.contains_points(dots).any():
                                weight = distPointToPoint(pt1, pt2)
                                G.add_edge(fromInd, toInd, weight=weight)
                                #if toInd in dict:
                                #    dict[toInd].append(fromInd)
                                #else:
                                #    dict[toInd] = [fromInd]
                    if i >= l and j != 0:
                        if mask2d[i - l][j - 1] == True:
                            toInd = nodeFromIndex(i - l, j - 1, px)
                            pt2 = mesh[toInd]
                            dots = DotsFromSegment(pt1, pt2, checkFreq)
                            if not pathKron.contains_points(dots).any():
                                weight = distPointToPoint(pt1, pt2)
                                G.add_edge(fromInd, toInd, weight=weight)
                                #if toInd in dict:
                                #    dict[toInd].append(fromInd)
                                #else:
                                #    dict[toInd] = [fromInd]
                    if j <= px - 1 - l and i != py - 1:
                        if mask2d[i + 1][j + l] == True:
                            toInd = nodeFromIndex(i + 1, j + l, px)
                            pt2 = mesh[toInd]
                            dots = DotsFromSegment(pt1, pt2, checkFreq)
                            if not pathKron.contains_points(dots).any():
                                weight = distPointToPoint(pt1, pt2)
                                G.add_edge(fromInd, toInd, weight=weight)
                                #if toInd in dict:
                                #    dict[toInd].append(fromInd)
                                #else:
                                #    dict[toInd] = [fromInd]
                    if j <= px - 1 - l and i != 0:
                        if mask2d[i - 1][j + l] == True:
                            toInd = nodeFromIndex(i - 1, j + l, px)
                            pt2 = mesh[toInd]
                            dots = DotsFromSegment(pt1, pt2, checkFreq)
                            if not pathKron.contains_points(dots).any():
                                weight = distPointToPoint(pt1, pt2)
                                G.add_edge(fromInd, toInd, weight=weight)
                                #if toInd in dict:
                                #    dict[toInd].append(fromInd)
                                #else:
                                #    dict[toInd] = [fromInd]
                    if i <= py - 1 - l and j != 0:
                        if mask2d[i + l][j - 1] == True:
                            toInd = nodeFromIndex(i + l, j - 1, px)
                            pt2 = mesh[toInd]
                            dots = DotsFromSegment(pt1, pt2, checkFreq)
                            if not pathKron.contains_points(dots).any():
                                weight = distPointToPoint(pt1, pt2)
                                G.add_edge(fromInd, toInd, weight=weight)
                                #if toInd in dict:
                                #    dict[toInd].append(fromInd)
                                #else:
                                #    dict[toInd] = [fromInd]
                    if i <= py - 1 - l and j != px - 1:
                        if mask2d[i + l][j + 1] == True:
                            toInd = nodeFromIndex(i + l, j + 1, px)
                            pt2 = mesh[toInd]
                            dots = DotsFromSegment(pt1, pt2, checkFreq)
                            if not pathKron.contains_points(dots).any():
                                weight = distPointToPoint(pt1, pt2)
                                G.add_edge(fromInd, toInd, weight=weight)
                                #if toInd in dict:
                                #    dict[toInd].append(fromInd)
                                #else:
                                #    dict[toInd] = [fromInd]
                    if j >= l and i != 0:
                        if mask2d[i - 1][j - l] == True:
                            toInd = nodeFromIndex(i - 1, j - l, px)
                            pt2 = mesh[toInd]
                            dots = DotsFromSegment(pt1, pt2, checkFreq)
                            if not pathKron.contains_points(dots).any():
                                weight = distPointToPoint(pt1, pt2)
                                G.add_edge(fromInd, toInd, weight=weight)
                                #if toInd in dict:
                                #    dict[toInd].append(fromInd)
                                #else:
                                #    dict[toInd] = [fromInd]
                    if j >= l and i != py - 1:
                        if mask2d[i + 1][j - l] == True:
                            toInd = nodeFromIndex(i + 1, j - l, px)
                            pt2 = mesh[toInd]
                            dots = DotsFromSegment(pt1, pt2, checkFreq)
                            if not pathKron.contains_points(dots).any():
                                weight = distPointToPoint(pt1, pt2)
                                G.add_edge(fromInd, toInd, weight=weight)
                                #if toInd in dict:
                                #    dict[toInd].append(fromInd)
                                #else:
                                #    dict[toInd] = [fromInd]
    #for key in dict:
    #    if len(dict[key]) == 1:
    #        print(key)
    #        print(mesh[key])
    #        print(mask[key])
    #        print(dict[key])
    return G


def closestNodeInMesh(mesh, mask, pt):
    """
    Find the closest node in a mesh to a given point.
    
    Parameters:
        mesh (numpy.array): Array of node coordinates
        mask (numpy.array): Boolean mask indicating valid nodes
        pt (numpy.array): Target point coordinates
    
    Returns:
        tuple: (closest_node_coordinates, node_index)
    """
    height = 3145
    ptTmp = np.copy(pt)
    ptTmp[1] = -ptTmp[1] + height
    dists = distPointToArray(ptTmp, mesh)
    dists[np.logical_not(mask)] = 10000000
    i = np.argmin(dists)
    answ = np.copy(mesh[i])
    return answ, i


def plotGraph(mesh, mask, G):
    """
    Plot a graph visualization.
    
    Parameters:
        mesh (numpy.array): Array of node coordinates
        mask (numpy.array): Boolean mask indicating valid nodes
        G (networkx.Graph): Graph to plot
    """
    fig, ax = plt.subplots()
    plt.scatter(mesh.T[0], -mesh.T[1] + height, s=1)
    plt.scatter(mesh[mask].T[0], -mesh[mask].T[1] + height, s=1)
    
    for i, j in G.edges():
        x = [mesh[i][0], mesh[j][0]]
        y = [-mesh[i][1] + height, -mesh[j][1] + height]
        plt.plot(x, y)
        
        
def makeGraph(l=40, checkFreq=40):
    """
    Create a navigation graph by combining north and south region graphs.
    
    Parameters:
        l (int, optional): Grid cell size. Defaults to 40.
        checkFreq (int, optional): Frequency of intermediate points for path validation. Defaults to 40.
    
    Returns:
        tuple: (graph, mesh, mask) - The created graph, node coordinates, and valid node mask
    """
    width = 4113
    height = 3145
    px, py = (int(width/l), int(height/l))
    x = np.linspace(0, width, px)
    y = np.linspace(0, height, py)
    xv, yv = np.meshgrid(x, y)
    x = xv.flatten()
    y = yv.flatten()
    yrev = -(y - height)
    mesh = np.append(np.array([x]), np.array([yrev]), axis=0).T
    
    mask = np.logical_and(pathZonePrec.contains_points(mesh), np.logical_not(pathKron.contains_points(mesh)))
    mask2d = np.reshape(mask, np.shape(xv))
    maskNorth = np.logical_and(pathNorthPrec.contains_points(mesh), np.logical_not(pathKron.contains_points(mesh)))
    maskNorth2d = np.reshape(maskNorth, np.shape(xv))
    maskSouth = np.logical_and(pathSouthPrec.contains_points(mesh), np.logical_not(pathKron.contains_points(mesh)))
    maskSouth2d = np.reshape(maskSouth, np.shape(xv))
    
    #соединяем северный и южный графы
    G1 = makeHalfGraph(maskNorth2d, mesh, checkFreq)
    G2 = makeHalfGraph(maskSouth2d, mesh, checkFreq)
    G = nx.compose(G1, G2)
    
    #координаты ворот
    gate1cords = np.array((1674, -1954 + height))
    gate2cords = np.array((2282, -1598 + height))
    
    gate1NorthPt, gate1NorthInd = closestNodeInMesh(mesh, maskNorth, gate1cords)
    gate1SouthPt, gate1SouthInd = closestNodeInMesh(mesh, maskSouth, gate1cords)
    gate2NorthPt, gate2NorthInd = closestNodeInMesh(mesh, maskNorth, gate2cords)
    gate2SouthPt, gate2SouthInd = closestNodeInMesh(mesh, maskSouth, gate2cords)
    G.add_edge(gate1NorthInd, gate1SouthInd, weight=distPointToPoint(gate1NorthPt, gate1SouthPt))
    G.add_edge(gate2NorthInd, gate2SouthInd, weight=distPointToPoint(gate2NorthPt, gate2SouthPt))
    
    #plotGraph(mesh, mask, G)
    return G, mesh, mask
#G, Gmesh, Gmask = makeGraph(70, 40) ######################

# Засекаем текущее время
'''  
start_time = time.time()
G, Gmesh, Gmask = makeGraph(70, 40)
end_time = time.time()

with open('graphs/saved_graph_70_40.pkl', 'wb') as f:
    pickle.dump({'G': G, 'Gmesh': Gmesh, 'Gmask': Gmask}, f)
elapsed_time = end_time - start_time
print(f"Время выполнения: {elapsed_time} секунд")

start_time = time.time()
G, Gmesh, Gmask = makeGraph(40, 40)
end_time = time.time()

with open('graphs/saved_graph_40_40.pkl', 'wb') as f:
    pickle.dump({'G': G, 'Gmesh': Gmesh, 'Gmask': Gmask}, f)
elapsed_time = end_time - start_time
print(f"Время выполнения: {elapsed_time} секунд")

start_time = time.time()
G, Gmesh, Gmask = makeGraph(20, 40)
end_time = time.time()

with open('graphs/saved_graph_20_40.pkl', 'wb') as f:
    pickle.dump({'G': G, 'Gmesh': Gmesh, 'Gmask': Gmask}, f)
elapsed_time = end_time - start_time
print(f"Время выполнения: {elapsed_time} секунд")

# Код, время выполнения которого нужно измерить


#G, Gmesh, Gmask = makeGraph(70, 40)

# Сохраняем массивы в файл
#with open('saved_graph.pkl', 'wb') as f:
#    pickle.dump({'G': G, 'Gmesh': Gmesh, 'Gmask': Gmask}, f)

# Засекаем текущее время после выполнения кода
#end_time = time.time()

# Вычисляем разницу времени
#elapsed_time = end_time - start_time

#print(f"Время выполнения: {elapsed_time} секунд")
'''  

def ClosestPathWithTraceNew(ptsFrom, ptsTo, velocities):
    """
    Calculate optimal paths from multiple starting points to multiple destination points
    using direct path calculations.
    
    Parameters:
        ptsFrom (numpy.array): Array of starting point coordinates
        ptsTo (numpy.array): Array of destination point coordinates
        velocities (numpy.array): Array of velocities for each starting point
    
    Returns:
        tuple: (filtered_destinations, minimum_times, plot_data) - Filtered destination points,
               minimum travel times, and data for plotting
    """
    # подсчёт метров в пикселе по вертикали и по горизонтали
    pinpoint1pix = (862, 1111)
    pinpoint2pix = (1569, 1111)
    pinpoint3pix = (862, 408)
    vertMetersInPix = geopy.distance.geodesic(PixelToDecimalVec(pinpoint1pix), PixelToDecimalVec(pinpoint3pix)).km / (pinpoint1pix[1] - pinpoint3pix[1])
    horzMetersInPix = geopy.distance.geodesic(PixelToDecimalVec(pinpoint1pix), PixelToDecimalVec(pinpoint2pix)).km / (pinpoint2pix[0] - pinpoint1pix[0])

    #координаты ворот
    gate1cords = np.array((1674, 1954))
    gate2cords = np.array((2282, 1598))

    #обходные координаты
    bypassA1A2cords = np.array((1399, 1517))
    bypassA1A4A3cords = np.array((2187, 2019))
    bypassB2B3cords = np.array((1414, 1524))
    bypassB1B5cords = np.array((1858, 1943))
    bypassB5B4cords = np.array((2162, 2081))
    bypassCcords = np.array((2044, 2053))
    bypassD1D2cords = np.array((2185, 1937))
    bypassD2D3cords = np.array((2089, 2093))
    bypassE2E3cords = np.array((2126, 2070))

    # сам подсчёт времён
    ptsTo = ptsTo[pathZone.contains_points(ptsTo)]
    ptsTo = ptsTo[np.logical_not(pathKron.contains_points(ptsTo))]
    ptsToMinTimes = np.ones(np.size(ptsTo, axis=0)) * 100000
    gateNums = np.zeros(np.size(ptsTo, axis=0))
    Traces = np.matlib.repmat(np.array([-1, 0]), np.size(ptsTo, axis=0), 1) # ptsFrom and gateNum


    northMask = pathNorth.contains_points(ptsTo)
    southMask = np.logical_not(northMask)
    divNorth = ptsTo[northMask]
    divSouth = ptsTo[southMask]
    TracesNorth = np.matlib.repmat(np.array([-1, 0]), np.size(divNorth, axis=0), 1)
    TracesSouth = np.matlib.repmat(np.array([-1, 0]), np.size(divSouth, axis=0), 1)
    gateNumsNorth = np.zeros(np.size(divNorth, axis=0))
    gateNumsSouth = np.zeros(np.size(divSouth, axis=0))

    A1Mask = pathA1.contains_points(ptsTo)
    A2Mask = np.logical_and(np.logical_not(A1Mask), northMask)
    A4Mask = pathA4.contains_points(ptsTo)
    A3Mask = np.logical_and(np.logical_not(A4Mask), southMask)
    A1NorthMask = pathA1.contains_points(divNorth)
    A2NorthMask = np.logical_not(A1NorthMask)
    A4SouthMask = pathA4.contains_points(divSouth)
    A3SouthMask = np.logical_not(A4SouthMask)
    divA1 = ptsTo[A1Mask]
    divA2 = ptsTo[A2Mask]
    divA3 = ptsTo[A3Mask]
    divA4 = ptsTo[A4Mask]
    gateNumsA1 = np.zeros(np.size(divA1, axis=0))
    gateNumsA2 = np.zeros(np.size(divA2, axis=0))
    gateNumsA3 = np.zeros(np.size(divA3, axis=0))
    gateNumsA4 = np.zeros(np.size(divA4, axis=0))

    B1Mask = pathB1.contains_points(ptsTo)
    B2Mask = pathB2.contains_points(ptsTo)
    B3Mask = np.logical_and(np.logical_not(B2Mask), northMask)
    B5Mask = pathB5.contains_points(ptsTo)
    B4Mask = np.logical_and(np.logical_not(np.logical_or(B1Mask, B5Mask)), southMask)
    B1SouthMask = pathB1.contains_points(divSouth)
    B2NorthMask = pathB2.contains_points(divNorth)
    B3NorthMask = np.logical_not(B2NorthMask)
    B5SouthMask = pathB5.contains_points(divSouth)
    B4SouthMask = np.logical_not(np.logical_or(B1SouthMask, B5SouthMask))
    divB1 = ptsTo[B1Mask]
    divB2 = ptsTo[B2Mask]
    divB3 = ptsTo[B3Mask]
    divB4 = ptsTo[B4Mask]
    divB5 = ptsTo[B5Mask]
    gateNumsB1 = np.zeros(np.size(divB1, axis=0))
    gateNumsB2 = np.zeros(np.size(divB2, axis=0))
    gateNumsB3 = np.zeros(np.size(divB3, axis=0))
    gateNumsB4 = np.zeros(np.size(divB4, axis=0))
    gateNumsB5 = np.zeros(np.size(divB5, axis=0))

    C1Mask = pathC1.contains_points(ptsTo)
    C2Mask = pathC2.contains_points(ptsTo)
    C3Mask = np.logical_and(np.logical_not(C2Mask), northMask)
    C4Mask = np.logical_and(np.logical_not(C1Mask), southMask)
    C1SouthMask = pathC1.contains_points(divSouth)
    C2NorthMask = pathC2.contains_points(divNorth)
    C3NorthMask = np.logical_not(C2NorthMask)
    C4SouthMask = np.logical_not(C1SouthMask)
    divC1 = ptsTo[C1Mask]
    divC2 = ptsTo[C2Mask]
    divC3 = ptsTo[C3Mask]
    divC4 = ptsTo[C4Mask]
    gateNumsC1 = np.zeros(np.size(divC1, axis=0))
    gateNumsC2 = np.zeros(np.size(divC2, axis=0))
    gateNumsC3 = np.zeros(np.size(divC3, axis=0))
    gateNumsC4 = np.zeros(np.size(divC4, axis=0))

    D1Mask = pathD1.contains_points(ptsTo)
    D2Mask = pathD2.contains_points(ptsTo)
    D3Mask = pathD3.contains_points(ptsTo)
    D4Mask = pathD4.contains_points(ptsTo)
    D5Mask = np.logical_and(np.logical_not(D4Mask), northMask)
    D1SouthMask = pathD1.contains_points(divSouth)
    D2SouthMask = pathD2.contains_points(divSouth)
    D3SouthMask = pathD3.contains_points(divSouth)
    D4NorthMask = pathD4.contains_points(divNorth)
    D5NorthMask = np.logical_not(D4NorthMask)
    divD1 = ptsTo[D1Mask]
    divD2 = ptsTo[D2Mask]
    divD3 = ptsTo[D3Mask]
    divD4 = ptsTo[D4Mask]
    divD5 = ptsTo[D5Mask]
    gateNumsD1 = np.zeros(np.size(divD1, axis=0))
    gateNumsD2 = np.zeros(np.size(divD2, axis=0))
    gateNumsD3 = np.zeros(np.size(divD3, axis=0))
    gateNumsD4 = np.zeros(np.size(divD4, axis=0))
    gateNumsD5 = np.zeros(np.size(divD5, axis=0))

    E4Mask = pathE4.contains_points(ptsTo)
    E1Mask = np.logical_and(np.logical_not(E4Mask), northMask)
    E2Mask = pathE2.contains_points(ptsTo)
    E3Mask = np.logical_and(np.logical_not(E2Mask), southMask)
    E4NorthMask = pathE4.contains_points(divNorth)
    E1NorthMask = np.logical_not(E4NorthMask)
    E2SouthMask = pathE2.contains_points(divSouth)
    E3SouthMask = np.logical_not(E2SouthMask)
    divE1 = ptsTo[E1Mask]
    divE2 = ptsTo[E2Mask]
    divE3 = ptsTo[E3Mask]
    divE4 = ptsTo[E4Mask]
    gateNumsE1 = np.zeros(np.size(divE1, axis=0))
    gateNumsE2 = np.zeros(np.size(divE2, axis=0))
    gateNumsE3 = np.zeros(np.size(divE3, axis=0))
    gateNumsE4 = np.zeros(np.size(divE4, axis=0))

    ToNorth1Mask = E4Mask
    ToNorth2Mask = E1Mask
    ToNorth1NorthMask = pathE4.contains_points(divNorth)
    ToNorth2NorthMask = np.logical_not(ToNorth1NorthMask)
    divToNorth1 = ptsTo[ToNorth1Mask]
    divToNorth2 = ptsTo[ToNorth2Mask]
    gateNumsToNorth1 = np.zeros(np.size(divToNorth1, axis=0))
    gateNumsToNorth2 = np.zeros(np.size(divToNorth2, axis=0))

    ToSouth1Mask = E3Mask
    ToSouth2Mask = E2Mask
    ToSouth2SouthMask = pathE2.contains_points(divSouth)
    ToSouth1SouthMask = np.logical_not(ToSouth2SouthMask)
    divToSouth1 = ptsTo[ToSouth1Mask]
    divToSouth2 = ptsTo[ToSouth2Mask]
    gateNumsToSouth1 = np.zeros(np.size(divToSouth1, axis=0))
    gateNumsToSouth2 = np.zeros(np.size(divToSouth2, axis=0))

    #print(divNorth)
    #print(divSouth)
    for ptFrom, vel, i in zip(ptsFrom, velocities, range(np.size(ptsFrom, axis=0))):
        if pathNorth.contains_points([ptFrom]):
            if pathAspawn.contains_points([ptFrom]):
                TracesA1 = TracesNorth[A1NorthMask]
                TracesA2 = TracesNorth[A2NorthMask]
                TracesA3 = TracesSouth[A3SouthMask]
                TracesA4 = TracesSouth[A4SouthMask]

                # если точка в A1, то траектория прямая (gate = 0)
                distsA1 = np.sqrt(np.sum(((divA1 - ptFrom) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))
                timesA1 = distsA1 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[A1Mask], timesA1]), axis=0)
                TracesA1[t12 == 1] = np.array([i, 0])
                ptsToMinTimes[A1Mask] = np.min(np.array([ptsToMinTimes[A1Mask], timesA1]), axis=0)

                # если точка в A2, то траектория - минимальная между 1. траекторией через bypassA1A2 (gate = 121) и 2. траекторией через {gate1, bypassA1A4A3, gate2} (gate = 122)
                distToBypassA1A2 = np.sqrt(np.sum(((ptFrom - np.array([bypassA1A2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists1A2 = np.sqrt(np.sum(((divA2 - bypassA1A2cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassA1A2

                distToGate1 = np.sqrt(np.sum(((ptFrom - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromGate1ToBypassA1A4A3 = np.sqrt(np.sum(((np.array([bypassA1A4A3cords]) - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassA1A4A3ToGate2 = np.sqrt(np.sum(((np.array([bypassA1A4A3cords]) - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists2A2 = np.sqrt(np.sum(((divA2 - gate2cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate1 + distFromGate1ToBypassA1A4A3 + distFromBypassA1A4A3ToGate2

                gateNumsA2[np.argmin(np.array([dists1A2, dists2A2]), axis=0) == 0] = 121
                gateNumsA2[np.argmin(np.array([dists1A2, dists2A2]), axis=0) == 1] = 122
                timesA2 = np.min(np.array([dists1A2, dists2A2]), axis=0) / vel

                variantsPart = np.append([np.array([i] * np.size(divA2, axis=0))], [gateNumsA2], axis=0).T
                variants = np.stack((TracesA2, variantsPart), axis=1)

                TracesA2 = variants[range(np.size(variants, axis=0)), np.argmin(np.array([ptsToMinTimes[A2Mask], timesA2]), axis=0)]
                ptsToMinTimes[A2Mask] = np.min(np.array([ptsToMinTimes[A2Mask], timesA2]), axis=0)

                # если точка в A3, то траектория - минимальная между 1. траекторией через {bypassA1A2, gate2} (gate = 131) и 2. траекторией через {gate1, bypassA1A4A3} (gate = 132)
                distToBypassA1A2 = np.sqrt(np.sum(((ptFrom - np.array([bypassA1A2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassA1A2ToGate2 = np.sqrt(np.sum(((np.array([bypassA1A2cords]) - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists1A3 = np.sqrt(np.sum(((divA3 - gate2cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassA1A2 + distFromBypassA1A2ToGate2

                distToGate1 = np.sqrt(np.sum(((ptFrom - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromGate1ToBypassA1A4A3 = np.sqrt(np.sum(((np.array([bypassA1A4A3cords]) - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists2A3 = np.sqrt(np.sum(((divA3 - bypassA1A4A3cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate1 + distFromGate1ToBypassA1A4A3

                gateNumsA3[np.argmin(np.array([dists1A3, dists2A3]), axis=0) == 0] = 131
                gateNumsA3[np.argmin(np.array([dists1A3, dists2A3]), axis=0) == 1] = 132
                timesA3 = np.min(np.array([dists1A3, dists2A3]), axis=0) / vel

                variantsPart = np.append([np.array([i] * np.size(divA3, axis=0))], [gateNumsA3], axis=0).T
                variants = np.stack((TracesA3, variantsPart), axis=1)

                TracesA3 = variants[range(np.size(variants, axis=0)), np.argmin(np.array([ptsToMinTimes[A3Mask], timesA3]), axis=0)]
                ptsToMinTimes[A3Mask] = np.min(np.array([ptsToMinTimes[A3Mask], timesA3]), axis=0)

                # если точка в A4, то траектория через gate1 (gate = 1)
                distToGate1 = np.sqrt(np.sum(((ptFrom - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distsA4 = np.sqrt(np.sum(((divA4 - gate1cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate1
                timesA4 = distsA4 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[A4Mask], timesA4]), axis=0)
                TracesA4[t12 == 1] = np.array([i, 1])
                ptsToMinTimes[A4Mask] = np.min(np.array([ptsToMinTimes[A4Mask], timesA4]), axis=0)

                TracesNorth[A1NorthMask] = TracesA1
                TracesNorth[A2NorthMask] = TracesA2
                TracesSouth[A3SouthMask] = TracesA3
                TracesSouth[A4SouthMask] = TracesA4

            elif pathEspawn.contains_points([ptFrom]):
                TracesE1 = TracesNorth[E1NorthMask]
                TracesE2 = TracesSouth[E2SouthMask]
                TracesE3 = TracesSouth[E3SouthMask]
                TracesE4 = TracesNorth[E4NorthMask]

                # если точка в E1, то траектория прямая (gate = 0)
                distsE1 = np.sqrt(np.sum(((divE1 - ptFrom) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))
                timesE1 = distsE1 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[E1Mask], timesE1]), axis=0)
                TracesE1[t12 == 1] = np.array([i, 0])
                ptsToMinTimes[E1Mask] = np.min(np.array([ptsToMinTimes[E1Mask], timesE1]), axis=0)

                # если точка в E2, то траектория - минимальная между 1. траекторией через gate2 (gate = 2) и 2. траекторией через {bypassB2B3, gate1} (gate = 522)
                distToGate2 = np.sqrt(np.sum(((ptFrom - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists1E2 = np.sqrt(np.sum(((divE2 - gate2cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate2

                distToBypassB2B3 = np.sqrt(np.sum(((ptFrom - np.array([bypassB2B3cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassB2B3ToGate1 = np.sqrt(np.sum(((np.array([bypassB2B3cords]) - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists2E2 = np.sqrt(np.sum(((divE2 - gate1cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassB2B3 + distFromBypassB2B3ToGate1

                gateNumsE2[np.argmin(np.array([dists1E2, dists2E2]), axis=0) == 0] = 2
                gateNumsE2[np.argmin(np.array([dists1E2, dists2E2]), axis=0) == 1] = 522
                timesE2 = np.min(np.array([dists1E2, dists2E2]), axis=0) / vel

                variantsPart = np.append([np.array([i] * np.size(divE2, axis=0))], [gateNumsE2], axis=0).T
                variants = np.stack((TracesE2, variantsPart), axis=1)

                TracesE2 = variants[range(np.size(variants, axis=0)), np.argmin(np.array([ptsToMinTimes[E2Mask], timesE2]), axis=0)]
                ptsToMinTimes[E2Mask] = np.min(np.array([ptsToMinTimes[E2Mask], timesE2]), axis=0)

                # если точка в E3, то траектория - минимальная между 1. траекторией через {gate2, bypassE2E3} (gate = 531) и 2. траекторией через {bypassB2B3, gate1} (gate = 522)
                distToGate2 = np.sqrt(np.sum(((ptFrom - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromGate2ToBypassE2E3 = np.sqrt(np.sum(((np.array([bypassE2E3cords]) - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists1E3 = np.sqrt(np.sum(((divE3 - bypassE2E3cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate2 + distFromGate2ToBypassE2E3

                distToBypassB2B3 = np.sqrt(np.sum(((ptFrom - np.array([bypassB2B3cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassB2B3ToGate1 = np.sqrt(np.sum(((np.array([bypassB2B3cords]) - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists2E3 = np.sqrt(np.sum(((divE3 - gate1cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassB2B3 + distFromBypassB2B3ToGate1

                gateNumsE3[np.argmin(np.array([dists1E3, dists2E3]), axis=0) == 0] = 531
                gateNumsE3[np.argmin(np.array([dists1E3, dists2E3]), axis=0) == 1] = 522
                timesE3 = np.min(np.array([dists1E3, dists2E3]), axis=0) / vel

                variantsPart = np.append([np.array([i] * np.size(divE3, axis=0))], [gateNumsE3], axis=0).T
                variants = np.stack((TracesE3, variantsPart), axis=1)

                TracesE3 = variants[range(np.size(variants, axis=0)), np.argmin(np.array([ptsToMinTimes[E3Mask], timesE3]), axis=0)]
                ptsToMinTimes[E3Mask] = np.min(np.array([ptsToMinTimes[E3Mask], timesE3]), axis=0)

                # если точка в E4, то траектория через bypassB2B3 (gate = 541)
                distToBypassB2B3 = np.sqrt(np.sum(((ptFrom - np.array([bypassB2B3cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distsE4 = np.sqrt(np.sum(((divE4 - bypassB2B3cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassB2B3
                timesE4 = distsE4 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[E4Mask], timesE4]), axis=0)
                TracesE4[t12 == 1] = np.array([i, 541])
                ptsToMinTimes[E4Mask] = np.min(np.array([ptsToMinTimes[E4Mask], timesE4]), axis=0)

                TracesNorth[E1NorthMask] = TracesE1
                TracesSouth[E2SouthMask] = TracesE2
                TracesSouth[E3SouthMask] = TracesE3
                TracesNorth[E4NorthMask] = TracesE4

            else:
                #расстояния внутри North сектора меряются по прямым, если не оговорено иначе
                distsNorth = np.sqrt(np.sum(((divNorth - ptFrom) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))
                timesNorth = distsNorth / vel

                t11 = np.array([ptsToMinTimes[northMask], timesNorth])
                t12 = np.argmin(t11, axis=0)
                TracesNorth[t12 == 1] = np.array([i, 0])
                ptsToMinTimes[northMask] = np.min(np.array([ptsToMinTimes[northMask], timesNorth]), axis=0)

                TracesToSouth1 = TracesSouth[ToSouth1SouthMask]
                TracesToSouth2 = TracesSouth[ToSouth2SouthMask]

                # если точка в ToSouth1, то траектория - минимальная между 1. траекторией через {gate2, bypassE2E3} (gate = 531) и 2. траекторией через {bypassB2B3, gate1} (gate = 522)
                distToGate2 = np.sqrt(np.sum(((ptFrom - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromGate2ToBypassE2E3 = np.sqrt(np.sum(((np.array([bypassE2E3cords]) - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists1ToSouth1 = np.sqrt(np.sum(((divToSouth1 - bypassE2E3cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate2 + distFromGate2ToBypassE2E3

                distToBypassB2B3 = np.sqrt(np.sum(((ptFrom - np.array([bypassB2B3cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassB2B3ToGate1 = np.sqrt(np.sum(((np.array([bypassB2B3cords]) - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists2ToSouth1 = np.sqrt(np.sum(((divToSouth1 - gate1cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassB2B3 + distFromBypassB2B3ToGate1

                gateNumsToSouth1[np.argmin(np.array([dists1ToSouth1, dists2ToSouth1]), axis=0) == 0] = 531
                gateNumsToSouth1[np.argmin(np.array([dists1ToSouth1, dists2ToSouth1]), axis=0) == 1] = 522
                timesToSouth1 = np.min(np.array([dists1ToSouth1, dists2ToSouth1]), axis=0) / vel

                variantsPart = np.append([np.array([i] * np.size(divToSouth1, axis=0))], [gateNumsToSouth1], axis=0).T
                variants = np.stack((TracesToSouth1, variantsPart), axis=1)

                TracesToSouth1 = variants[range(np.size(variants, axis=0)), np.argmin(np.array([ptsToMinTimes[ToSouth1Mask], timesToSouth1]), axis=0)]
                ptsToMinTimes[ToSouth1Mask] = np.min(np.array([ptsToMinTimes[ToSouth1Mask], timesToSouth1]), axis=0)

                # если точка в ToSouth2, то траектория - минимальная между 1. траекторией через gate2 (gate = 2) и 2. траекторией через {bypassB2B3, gate1} (gate = 522)
                distToGate2 = np.sqrt(np.sum(((ptFrom - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists1ToSouth2 = np.sqrt(np.sum(((divToSouth2 - gate2cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate2

                distToBypassB2B3 = np.sqrt(np.sum(((ptFrom - np.array([bypassB2B3cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassB2B3ToGate1 = np.sqrt(np.sum(((np.array([bypassB2B3cords]) - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists2ToSouth2 = np.sqrt(np.sum(((divToSouth2 - gate1cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassB2B3 + distFromBypassB2B3ToGate1

                gateNumsToSouth2[np.argmin(np.array([dists1ToSouth2, dists2ToSouth2]), axis=0) == 0] = 2
                gateNumsToSouth2[np.argmin(np.array([dists1ToSouth2, dists2ToSouth2]), axis=0) == 1] = 522
                timesToSouth2 = np.min(np.array([dists1ToSouth2, dists2ToSouth2]), axis=0) / vel

                variantsPart = np.append([np.array([i] * np.size(divToSouth2, axis=0))], [gateNumsToSouth2], axis=0).T
                variants = np.stack((TracesToSouth2, variantsPart), axis=1)

                TracesToSouth2 = variants[range(np.size(variants, axis=0)), np.argmin(np.array([ptsToMinTimes[ToSouth2Mask], timesToSouth2]), axis=0)]
                ptsToMinTimes[ToSouth2Mask] = np.min(np.array([ptsToMinTimes[ToSouth2Mask], timesToSouth2]), axis=0)

                TracesSouth[ToSouth1SouthMask] = TracesToSouth1
                TracesSouth[ToSouth2SouthMask] = TracesToSouth2


                #distToGate1 = np.sqrt(np.sum(((ptFrom - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                #distToGate2 = np.sqrt(np.sum(((ptFrom - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                #dists1South = np.sqrt(np.sum(((divSouth - gate1cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate1
                #dists2South = np.sqrt(np.sum(((divSouth - gate2cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate2
                #print('------12------')

                #gateNumsSouth[np.argmin(np.array([dists1South, dists2South]), axis=0) == 0] = 1
                #gateNumsSouth[np.argmin(np.array([dists1South, dists2South]), axis=0) == 1] = 2
                #timesSouth = np.min(np.array([dists1South, dists2South]), axis=0) / vel
                #print('------13------')

                #variantsPart = np.append([np.array([i] * np.size(divSouth, axis=0))], [gateNumsSouth], axis=0).T
                #variants = np.stack((TracesSouth, variantsPart), axis=1)
                #print('------14------')

                #TracesSouth = variants[range(np.size(variants, axis=0)), np.argmin(np.array([ptsToMinTimes[southMask], timesSouth]), axis=0)]
                #ptsToMinTimes[southMask] = np.min(np.array([ptsToMinTimes[southMask], timesSouth]), axis=0)
                #print('------15------')
        else:
            if pathBspawn.contains_points([ptFrom]):
                TracesB1 = TracesSouth[B1SouthMask]
                TracesB2 = TracesNorth[B2NorthMask]
                TracesB3 = TracesNorth[B3NorthMask]
                TracesB4 = TracesSouth[B4SouthMask]
                TracesB5 = TracesSouth[B5SouthMask]

                # если точка в B1, то траектория прямая (gate = 0)
                distsB1 = np.sqrt(np.sum(((divB1 - ptFrom) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))
                timesB1 = distsB1 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[B1Mask], timesB1]), axis=0)
                TracesB1[t12 == 1] = np.array([i, 0])
                ptsToMinTimes[B1Mask] = np.min(np.array([ptsToMinTimes[B1Mask], timesB1]), axis=0)

                # если точка в B2, то траектория через gate1 (gate = 1)
                distToGate1 = np.sqrt(np.sum(((ptFrom - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distsB2 = np.sqrt(np.sum(((divB2 - gate1cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate1
                timesB2 = distsB2 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[B2Mask], timesB2]), axis=0)
                TracesB2[t12 == 1] = np.array([i, 1])
                ptsToMinTimes[B2Mask] = np.min(np.array([ptsToMinTimes[B2Mask], timesB2]), axis=0)

                # если точка в B3, то траектория - минимальная между 1. траекторией через {gate1, bypassB2B3} (gate = 231) и 2. траекторией через {bypassB1B5, bypassB5B4, gate2} (gate = 232)
                distToGate1 = np.sqrt(np.sum(((ptFrom - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromGate1ToBypassB2B3 = np.sqrt(np.sum(((np.array([bypassB2B3cords]) - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists1B3 = np.sqrt(np.sum(((divB3 - bypassB2B3cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate1 + distFromGate1ToBypassB2B3

                distToBypassB1B5 = np.sqrt(np.sum(((ptFrom - np.array([bypassB1B5cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassB1B5ToBypassB5B4 = np.sqrt(np.sum(((np.array([bypassB1B5cords]) - np.array([bypassB5B4cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassB5B4ToGate2 = np.sqrt(np.sum(((np.array([bypassB5B4cords]) - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists2B3 = np.sqrt(np.sum(((divB3 - gate2cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassB1B5 + distFromBypassB1B5ToBypassB5B4 + distFromBypassB5B4ToGate2

                gateNumsB3[np.argmin(np.array([dists1B3, dists2B3]), axis=0) == 0] = 231
                gateNumsB3[np.argmin(np.array([dists1B3, dists2B3]), axis=0) == 1] = 232
                timesB3 = np.min(np.array([dists1B3, dists2B3]), axis=0) / vel

                variantsPart = np.append([np.array([i] * np.size(divB3, axis=0))], [gateNumsB3], axis=0).T
                variants = np.stack((TracesB3, variantsPart), axis=1)

                TracesB3 = variants[range(np.size(variants, axis=0)), np.argmin(np.array([ptsToMinTimes[B3Mask], timesB3]), axis=0)]
                ptsToMinTimes[B3Mask] = np.min(np.array([ptsToMinTimes[B3Mask], timesB3]), axis=0)

                # если точка в B4, то траектория через {bypassB1B5, bypassB5B4} (gate = 241)
                distToBypassB1B5 = np.sqrt(np.sum(((ptFrom - np.array([bypassB1B5cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassB1B5ToBypassB5B4 = np.sqrt(np.sum(((np.array([bypassB1B5cords]) - np.array([bypassB5B4cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distsB4 = np.sqrt(np.sum(((divB4 - bypassB5B4cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassB1B5 + distFromBypassB1B5ToBypassB5B4
                timesB4 = distsB4 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[B4Mask], timesB4]), axis=0)
                TracesB4[t12 == 1] = np.array([i, 241])
                ptsToMinTimes[B4Mask] = np.min(np.array([ptsToMinTimes[B4Mask], timesB4]), axis=0)

                # если точка в B5, то траектория через bypassB1B5 (gate = 251)
                distToBypassB1B5 = np.sqrt(np.sum(((ptFrom - np.array([bypassB1B5cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distsB5 = np.sqrt(np.sum(((divB5 - bypassB1B5cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassB1B5
                timesB5 = distsB5 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[B5Mask], timesB5]), axis=0)
                TracesB5[t12 == 1] = np.array([i, 251])
                ptsToMinTimes[B5Mask] = np.min(np.array([ptsToMinTimes[B5Mask], timesB5]), axis=0)

                TracesSouth[B1SouthMask] = TracesB1
                TracesNorth[B2NorthMask] = TracesB2
                TracesNorth[B3NorthMask] = TracesB3
                TracesSouth[B4SouthMask] = TracesB4
                TracesSouth[B5SouthMask] = TracesB5

            elif pathCspawn.contains_points([ptFrom]):
                TracesC1 = TracesSouth[C1SouthMask]
                TracesC2 = TracesNorth[C2NorthMask]
                TracesC3 = TracesNorth[C3NorthMask]
                TracesC4 = TracesSouth[C4SouthMask]

                # если точка в C1, то траектория прямая (gate = 0)
                distsC1 = np.sqrt(np.sum(((divC1 - ptFrom) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))
                timesC1 = distsC1 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[C1Mask], timesC1]), axis=0)
                TracesC1[t12 == 1] = np.array([i, 0])
                ptsToMinTimes[C1Mask] = np.min(np.array([ptsToMinTimes[C1Mask], timesC1]), axis=0)

                # если точка в C2, то траектория через gate1 (gate = 1)
                distToGate1 = np.sqrt(np.sum(((ptFrom - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distsC2 = np.sqrt(np.sum(((divC2 - gate1cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate1
                timesC2 = distsC2 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[C2Mask], timesC2]), axis=0)
                TracesC2[t12 == 1] = np.array([i, 1])
                ptsToMinTimes[C2Mask] = np.min(np.array([ptsToMinTimes[C2Mask], timesC2]), axis=0)

                # если точка в C3, то траектория - минимальная между 1. траекторией через {gate1, bypassB2B3} (gate = 331) и 2. траекторией через {bypassC, bypassB5B4, gate2} (gate = 332)
                distToGate1 = np.sqrt(np.sum(((ptFrom - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromGate1ToBypassB2B3 = np.sqrt(np.sum(((np.array([bypassB2B3cords]) - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists1C3 = np.sqrt(np.sum(((divC3 - bypassB2B3cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate1 + distFromGate1ToBypassB2B3

                distToBypassC = np.sqrt(np.sum(((ptFrom - np.array([bypassCcords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassCToBypassB5B4 = np.sqrt(np.sum(((np.array([bypassCcords]) - np.array([bypassB5B4cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassB5B4ToGate2 = np.sqrt(np.sum(((np.array([bypassB5B4cords]) - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists2C3 = np.sqrt(np.sum(((divC3 - gate2cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassC + distFromBypassCToBypassB5B4 + distFromBypassB5B4ToGate2

                gateNumsC3[np.argmin(np.array([dists1C3, dists2C3]), axis=0) == 0] = 331
                gateNumsC3[np.argmin(np.array([dists1C3, dists2C3]), axis=0) == 1] = 332
                timesC3 = np.min(np.array([dists1C3, dists2C3]), axis=0) / vel

                variantsPart = np.append([np.array([i] * np.size(divC3, axis=0))], [gateNumsC3], axis=0).T
                variants = np.stack((TracesC3, variantsPart), axis=1)

                TracesC3 = variants[range(np.size(variants, axis=0)), np.argmin(np.array([ptsToMinTimes[C3Mask], timesC3]), axis=0)]
                ptsToMinTimes[C3Mask] = np.min(np.array([ptsToMinTimes[C3Mask], timesC3]), axis=0)

                # если точка в C4, то траектория через {bypassC, bypassB5B4} (gate = 341)
                distToBypassC = np.sqrt(np.sum(((ptFrom - np.array([bypassCcords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassCToBypassB5B4 = np.sqrt(np.sum(((np.array([bypassCcords]) - np.array([bypassB5B4cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distsC4 = np.sqrt(np.sum(((divC4 - bypassB5B4cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassC + distFromBypassCToBypassB5B4
                timesC4 = distsC4 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[C4Mask], timesC4]), axis=0)
                TracesC4[t12 == 1] = np.array([i, 341])
                ptsToMinTimes[C4Mask] = np.min(np.array([ptsToMinTimes[C4Mask], timesC4]), axis=0)

                TracesSouth[C1SouthMask] = TracesC1
                TracesNorth[C2NorthMask] = TracesC2
                TracesNorth[C3NorthMask] = TracesC3
                TracesSouth[C4SouthMask] = TracesC4

            elif pathDspawn.contains_points([ptFrom]):
                TracesD1 = TracesSouth[D1SouthMask]
                TracesD2 = TracesSouth[D2SouthMask]
                TracesD3 = TracesSouth[D3SouthMask]
                TracesD4 = TracesNorth[D4NorthMask]
                TracesD5 = TracesNorth[D5NorthMask]

                # если точка в D1, то траектория прямая (gate = 0)
                distsD1 = np.sqrt(np.sum(((divD1 - ptFrom) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))
                timesD1 = distsD1 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[D1Mask], timesD1]), axis=0)
                TracesD1[t12 == 1] = np.array([i, 0])
                ptsToMinTimes[D1Mask] = np.min(np.array([ptsToMinTimes[D1Mask], timesD1]), axis=0)

                # если точка в D2, то траектория через bypassD1D2 (gate = 421)
                distToBypassD1D2 = np.sqrt(np.sum(((ptFrom - np.array([bypassD1D2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distsD2 = np.sqrt(np.sum(((divD2 - bypassD1D2cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassD1D2
                timesD2 = distsD2 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[D2Mask], timesD2]), axis=0)
                TracesD2[t12 == 1] = np.array([i, 421])
                ptsToMinTimes[D2Mask] = np.min(np.array([ptsToMinTimes[D2Mask], timesD2]), axis=0)

                # если точка в D3, то траектория через {bypassD1D2, bypassD2D3} (gate = 431)
                distToBypassD1D2 = np.sqrt(np.sum(((ptFrom - np.array([bypassD1D2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassD1D2ToBypassD2D3 = np.sqrt(np.sum(((np.array([bypassD1D2cords]) - np.array([bypassD2D3cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distsD3 = np.sqrt(np.sum(((divD3 - bypassD2D3cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassD1D2 + distFromBypassD1D2ToBypassD2D3
                timesD3 = distsD3 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[D3Mask], timesD3]), axis=0)
                TracesD3[t12 == 1] = np.array([i, 431])
                ptsToMinTimes[D3Mask] = np.min(np.array([ptsToMinTimes[D3Mask], timesD3]), axis=0)

                # если точка в D4, то траектория - минимальная между 1. траекторией через {gate2, bypassB2B3} (gate = 441) и 2. траекторией через  {bypassD1D2, bypassD2D3, gate1} (gate = 442)
                distToGate2 = np.sqrt(np.sum(((ptFrom - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromGate2ToBypassB2B3 = np.sqrt(np.sum(((np.array([bypassB2B3cords]) - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists1D4 = np.sqrt(np.sum(((divD4 - bypassB2B3cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate2 + distFromGate2ToBypassB2B3

                distToBypassD1D2 = np.sqrt(np.sum(((ptFrom - np.array([bypassD1D2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassD1D2ToBypassD2D3 = np.sqrt(np.sum(((np.array([bypassD1D2cords]) - np.array([bypassD2D3cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromBypassD2D3ToGate1 = np.sqrt(np.sum(((np.array([bypassD2D3cords]) - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists2D4 = np.sqrt(np.sum(((divD4 - gate1cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToBypassD1D2 + distFromBypassD1D2ToBypassD2D3 + distFromBypassD2D3ToGate1

                gateNumsD4[np.argmin(np.array([dists1D4, dists2D4]), axis=0) == 0] = 441
                gateNumsD4[np.argmin(np.array([dists1D4, dists2D4]), axis=0) == 1] = 442
                timesD4 = np.min(np.array([dists1D4, dists2D4]), axis=0) / vel

                variantsPart = np.append([np.array([i] * np.size(divD4, axis=0))], [gateNumsD4], axis=0).T
                variants = np.stack((TracesD4, variantsPart), axis=1)

                TracesD4 = variants[range(np.size(variants, axis=0)), np.argmin(np.array([ptsToMinTimes[D4Mask], timesD4]), axis=0)]
                ptsToMinTimes[D4Mask] = np.min(np.array([ptsToMinTimes[D4Mask], timesD4]), axis=0)

                # если точка в D5, то траектория через gate2 (gate = 2)
                distToGate2 = np.sqrt(np.sum(((ptFrom - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distsD5 = np.sqrt(np.sum(((divD5 - gate2cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate2
                timesD5 = distsD5 / vel

                t12 = np.argmin(np.array([ptsToMinTimes[D5Mask], timesD5]), axis=0)
                TracesD5[t12 == 1] = np.array([i, 2])
                ptsToMinTimes[D5Mask] = np.min(np.array([ptsToMinTimes[D5Mask], timesD5]), axis=0)

                TracesSouth[D1SouthMask] = TracesD1
                TracesSouth[D2SouthMask] = TracesD2
                TracesSouth[D3SouthMask] = TracesD3
                TracesNorth[D4NorthMask] = TracesD4
                TracesNorth[D5NorthMask] = TracesD5

            else:
                # траектории внутри South сектора считаются по прямой, если не оговорено инчаче
                distsSouth = np.sqrt(np.sum(((divSouth - ptFrom) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))
                timesSouth = distsSouth / vel

                t21 = np.array([ptsToMinTimes[southMask], timesSouth])
                t22 = np.argmin(t21, axis=0)

                TracesSouth[t22 == 1] = np.array([i, 0])
                ptsToMinTimes[southMask] = np.min(np.array([ptsToMinTimes[southMask], timesSouth]), axis=0)



                TracesToNorth1 = TracesNorth[ToNorth1NorthMask]
                TracesToNorth2 = TracesNorth[ToNorth2NorthMask]

                # если точка в ToNorth1, то траектория - минимальная между 1. траекторией через gate1 (gate = 1) и 2. траекторией через {gate2, bypassB2B3} (gate = 531)
                distToGate1 = np.sqrt(np.sum(((ptFrom - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists1ToNorth1 = np.sqrt(np.sum(((divToNorth1 - gate1cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate1

                distToGate2 = np.sqrt(np.sum(((ptFrom - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromGate2ToBypassE2E3 = np.sqrt(np.sum(((np.array([bypassE2E3cords]) - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists2ToNorth1 = np.sqrt(np.sum(((divToNorth1 - bypassE2E3cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate2 + distFromGate2ToBypassE2E3

                gateNumsToNorth1[np.argmin(np.array([dists1ToNorth1, dists2ToNorth1]), axis=0) == 0] = 1
                gateNumsToNorth1[np.argmin(np.array([dists1ToNorth1, dists2ToNorth1]), axis=0) == 1] = 531
                timesToNorth1 = np.min(np.array([dists1ToNorth1, dists2ToNorth1]), axis=0) / vel

                variantsPart = np.append([np.array([i] * np.size(divToNorth1, axis=0))], [gateNumsToNorth1], axis=0).T
                variants = np.stack((TracesToNorth1, variantsPart), axis=1)


                TracesToNorth1 = variants[range(np.size(variants, axis=0)), np.argmin(np.array([ptsToMinTimes[ToNorth1Mask], timesToNorth1]), axis=0)]
                ptsToMinTimes[ToNorth1Mask] = np.min(np.array([ptsToMinTimes[ToNorth1Mask], timesToNorth1]), axis=0)

                # если точка в ToNorth2, то траектория - минимальная между 1. траекторией через {gate1, bypassB2B3} (gate = 331) и 2. траекторией через gate2 (gate = 2)
                distToGate1 = np.sqrt(np.sum(((ptFrom - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                distFromGate1ToBypassB2B3 = np.sqrt(np.sum(((np.array([bypassB2B3cords]) - np.array([gate1cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists1ToNorth2 = np.sqrt(np.sum(((divToNorth2 - bypassB2B3cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate1 + distFromGate1ToBypassB2B3

                distToGate2 = np.sqrt(np.sum(((ptFrom - np.array([gate2cords])) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1))[0]
                dists2ToNorth2 = np.sqrt(np.sum(((divToNorth2 - gate2cords) * np.array([horzMetersInPix, vertMetersInPix])) ** 2, axis=1)) + distToGate2

                gateNumsToNorth2[np.argmin(np.array([dists1ToNorth2, dists2ToNorth2]), axis=0) == 0] = 331
                gateNumsToNorth2[np.argmin(np.array([dists1ToNorth2, dists2ToNorth2]), axis=0) == 1] = 2
                timesToNorth2 = np.min(np.array([dists1ToNorth2, dists2ToNorth2]), axis=0) / vel

                variantsPart = np.append([np.array([i] * np.size(divToNorth2, axis=0))], [gateNumsToNorth2], axis=0).T
                variants = np.stack((TracesToNorth2, variantsPart), axis=1)

                TracesToNorth2 = variants[range(np.size(variants, axis=0)), np.argmin(np.array([ptsToMinTimes[ToNorth2Mask], timesToNorth2]), axis=0)]
                ptsToMinTimes[ToNorth2Mask] = np.min(np.array([ptsToMinTimes[ToNorth2Mask], timesToNorth2]), axis=0)

                TracesNorth[ToNorth1NorthMask] = TracesToNorth1
                TracesNorth[ToNorth2NorthMask] = TracesToNorth2

    Traces[northMask] = TracesNorth
    Traces[southMask] = TracesSouth
    # print(Traces)

    gate1cordsrev = gate1cords
    gate1cordsrev[1] = -gate1cordsrev[1] + height
    gate2cordsrev = gate2cords
    gate2cordsrev[1] = -gate2cordsrev[1] + height
    bypassA1A2cordsrev = bypassA1A2cords
    bypassA1A2cordsrev[1] = -bypassA1A2cordsrev[1] + height
    bypassA1A4A3cordsrev = bypassA1A4A3cords
    bypassA1A4A3cordsrev[1] = -bypassA1A4A3cordsrev[1] + height
    bypassB2B3cordsrev = bypassB2B3cords
    bypassB2B3cordsrev[1] = -bypassB2B3cordsrev[1] + height
    bypassB1B5cordsrev = bypassB1B5cords
    bypassB1B5cordsrev[1] = -bypassB1B5cordsrev[1] + height
    bypassB5B4cordsrev = bypassB5B4cords
    bypassB5B4cordsrev[1] = -bypassB5B4cordsrev[1] + height
    bypassCcordsrev = bypassCcords
    bypassCcordsrev[1] = -bypassCcordsrev[1] + height
    bypassD1D2cordsrev = bypassD1D2cords
    bypassD1D2cordsrev[1] = -bypassD1D2cordsrev[1] + height
    bypassD2D3cordsrev = bypassD2D3cords
    bypassD2D3cordsrev[1] = -bypassD2D3cordsrev[1] + height
    bypassE2E3cordsrev = bypassE2E3cords
    bypassE2E3cordsrev[1] = -bypassE2E3cordsrev[1] + height

    plotData = np.array
    for i in range(np.size(ptsTo, axis=0)):
        trace = Traces[i]
        pt1 = np.array(ptsFrom[trace[0]])
        pt2 = ptsTo[i]
        pt1[1] = -pt1[1] + height
        pt2[1] = -pt2[1] + height
        if trace[1] == 0:
            x, y = np.vstack((pt1, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 1:
            x, y = np.vstack((pt1, gate1cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 2:
            x, y = np.vstack((pt1, gate2cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 121:
            x, y = np.vstack((pt1, bypassA1A2cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 122:
            x, y = np.vstack((pt1, gate1cordsrev, bypassA1A4A3cordsrev, gate2cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 131:
            x, y = np.vstack((pt1, bypassA1A2cordsrev, gate2cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 132:
            x, y = np.vstack((pt1, gate1cordsrev, bypassA1A4A3cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 231:
            x, y = np.vstack((pt1, gate1cordsrev, bypassB2B3cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 232:
            x, y = np.vstack((pt1, bypassB1B5cordsrev, bypassB5B4cordsrev, gate2cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 241:
            x, y = np.vstack((pt1, bypassB1B5cordsrev, bypassB5B4cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 251:
            x, y = np.vstack((pt1, bypassB1B5cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 331:
            x, y = np.vstack((pt1, gate1cordsrev, bypassB2B3cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 332:
            x, y = np.vstack((pt1, bypassCcordsrev, bypassB5B4cordsrev, gate2cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 341:
            x, y = np.vstack((pt1, bypassCcordsrev, bypassB5B4cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 421:
            x, y = np.vstack((pt1, bypassD1D2cordsrev, pt2)).T
           #plt.plot(x, y, 'b')
        elif trace[1] == 431:
            x, y = np.vstack((pt1, bypassD1D2cordsrev, bypassD2D3cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 441:
            x, y = np.vstack((pt1, gate2cordsrev, bypassB2B3cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 442:
            x, y = np.vstack((pt1, bypassD1D2cordsrev, bypassD2D3cordsrev, gate1cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 522:
            x, y = np.vstack((pt1, bypassB2B3cordsrev, gate1cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 531:
            x, y = np.vstack((pt1, gate2cordsrev, bypassE2E3cordsrev, pt2)).T
            #plt.plot(x, y, 'b')
        elif trace[1] == 541:
            x, y = np.vstack((pt1, bypassB2B3cordsrev, pt2)).T
            #plt.plot(x, y, 'b')

        if i == 0:
            plotData = [[x, y, ptsToMinTimes[i], trace[1], trace[0]]]
        else:
            plotData.append([x, y, ptsToMinTimes[i], trace[1], trace[0]])

    ptsTo.T[1] = -ptsTo.T[1] + height

    preciseMask = pathZonePrec.contains_points(ptsTo)


    precPlotData = []
    for i in range(np.size(preciseMask)):
        if preciseMask[i] == True:
            precPlotData.append(plotData[i])
    return ptsTo[preciseMask], ptsToMinTimes[preciseMask], precPlotData


def PlotMap(ptsFromPix, ptsToPix, plotData, linewidth=0.75, viewFrom=True, viewTo=True, nameinsert='', stations=None):
    """
    Generate a plot showing optimal paths on a map.
    
    Parameters:
        ptsFromPix (numpy.array): Array of starting point coordinates
        ptsToPix (numpy.array): Array of destination point coordinates
        plotData (list): List of path data for plotting
        linewidth (float, optional): Width of path lines. Defaults to 0.75.
        viewFrom (bool, optional): Whether to show starting points. Defaults to True.
        viewTo (bool, optional): Whether to show destination points. Defaults to True.
        nameinsert (str, optional): String to insert in the output filename. Defaults to ''.
        stations (list, optional): List of station information. Defaults to None.
    """
    ptsFromPix = np.array(ptsFromPix)
    ptsToPix = np.array(ptsToPix)
    img = plt.imread("data/canvas_new_fish_gray.png")
    width = 4113
    height = 3145

    plt.figure(dpi=300)
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, width, 0, height])
    ax.axis('equal')
    plotData = sorted(plotData, key=lambda x : x[2])
    maxTime = plotData[-1][2]
    for plot in plotData:
        x = plot[0]
        y = plot[1]
        time = plot[2]
        #plt.plot(x, y, color = cm.Oranges(time/maxTime))
        plt.plot(x, y, color = cm.Purples(time/maxTime), linewidth=linewidth, zorder=5)

    if viewTo:
        x = ptsToPix.T[0]
        y = -ptsToPix.T[1] + height
        plt.scatter(x, y, s=2, zorder=10)

    if viewFrom:
        x = ptsFromPix.T[0]
        y = -ptsFromPix.T[1] + height
        plt.scatter(x, y, s=16, marker='s', color='r', edgecolor='black', linewidth=0.6, zorder=15)
        
        # Add station names if provided
        if stations and len(stations) == len(ptsFromPix):
            for i, (station_x, station_y) in enumerate(zip(x, y)):
                # Use actual station name, not a generated name
                station_name = stations[i].name if hasattr(stations[i], 'name') else f"Станция {i+1}"
                plt.annotate(
                    station_name,
                    (station_x, station_y),
                    xytext=(5, 5),
                    textcoords='offset points',
                    fontsize=6,  # Smaller font size
                    fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="black", alpha=0.8),
                    zorder=20
                )

    ax.set_ylim([0, height])
    ax.set_xlim([0, width])
    plt.savefig(f'output/plot_example{nameinsert}.png')
    #plt.savefig(f'output/plot_example{nameinsert}_hires.png', dpi=450, bbox_inches='tight')
    #plt.show()

def PlotMapReachability(ptsFromPix, ptsToPix, plotData, linewidth=0.75, viewFrom=True, viewTo=True, nameinsert='', stations=None):
    """
    Generate a reachability map showing travel times as a color gradient.
    
    Parameters:
        ptsFromPix (numpy.array): Array of starting point coordinates
        ptsToPix (numpy.array): Array of destination point coordinates
        plotData (list): List of path data for plotting
        linewidth (float, optional): Width of path lines. Defaults to 0.75.
        viewFrom (bool, optional): Whether to show starting points. Defaults to True.
        viewTo (bool, optional): Whether to show destination points. Defaults to True.
        nameinsert (str, optional): String to insert in the output filename. Defaults to ''.
        stations (list, optional): List of station information. Defaults to None.
    """
    ptsFromPix = np.array(ptsFromPix)
    ptsToPix = np.array(ptsToPix)
    img = plt.imread("data/canvas_new_fish_gray.png")
    width = 4113
    height = 3145

    plt.figure(dpi=300)
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, width, 0, height])
    ax.axis('equal')
    plotData = sorted(plotData, key=lambda x : x[2])
    maxTime = plotData[-1][2]
    scatterX = []
    scatterY = []
    scatterColor = []
    for plot in plotData:
        x = plot[0]
        y = plot[1]
        time = plot[2]
        #plt.plot(x, y, color = cm.Oranges(time/maxTime))
        scatterX.append(x[-1])
        scatterY.append(y[-1])
        scatterColor.append(cm.Purples(time/maxTime))
    plt.scatter(scatterX, scatterY, s=0.3, marker='o', c=scatterColor)

    if viewFrom:
        x = ptsFromPix.T[0]
        y = -ptsFromPix.T[1] + height
        plt.scatter(x, y, s=16, marker='s', color='r', edgecolor='black', linewidth=0.6, zorder=15)
        
        # Add station names if provided
        if stations and len(stations) == len(ptsFromPix):
            for i, (station_x, station_y) in enumerate(zip(x, y)):
                # Use actual station name, not a generated name
                station_name = stations[i].name if hasattr(stations[i], 'name') else f"Станция {i+1}"
                plt.annotate(
                    station_name,
                    (station_x, station_y),
                    xytext=(5, 5),
                    textcoords='offset points',
                    fontsize=6,  # Smaller font size
                    fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="black", alpha=0.8),
                    zorder=20
                )

    ax.set_ylim([0, height])
    ax.set_xlim([0, width])
    plt.savefig(f'output/plot_reachability_example{nameinsert}.png')
    #plt.savefig(f'output/plot_reachability_example{nameinsert}_hires.png', dpi=450, bbox_inches='tight')

def PlotMapDifStReachability(ptsFromPix, ptsToPix, plotData, linewidth=0.75, viewFrom=True, viewTo=True, nameinsert='', stations=None):
    """
    Generate a differential station reachability map showing which station is optimal for each point.
    
    Parameters:
        ptsFromPix (numpy.array): Array of starting point coordinates
        ptsToPix (numpy.array): Array of destination point coordinates
        plotData (list): List of path data for plotting
        linewidth (float, optional): Width of path lines. Defaults to 0.75.
        viewFrom (bool, optional): Whether to show starting points. Defaults to True.
        viewTo (bool, optional): Whether to show destination points. Defaults to True.
        nameinsert (str, optional): String to insert in the output filename. Defaults to ''.
        stations (list, optional): List of station information. Defaults to None.
    """
    ptsFromPix = np.array(ptsFromPix)
    ptsToPix = np.array(ptsToPix)
    img = plt.imread("data/canvas_new_fish_gray.png")
    width = 4113
    height = 3145

    num_pts = np.size(ptsFromPix, axis=0)
    colors = cm.rainbow(np.linspace(0, 1, np.size(ptsFromPix, axis=0)))
    #colors = cm.tab20b(np.linspace(0, 1, np.size(ptsFromPix, axis=0)))
    plt.figure(dpi=300)
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, width, 0, height])
    ax.axis('equal')
    plotData = sorted(plotData, key=lambda x : x[2])
    maxTime = plotData[-1][2]

    scatterX = []
    scatterY = []
    scatterColor = []
    for plot in plotData:
        x = plot[0]
        y = plot[1]
        time = plot[2]
        #plt.plot(x, y, color = cm.Oranges(time/maxTime))
        #plt.plot(x, y, color = colors[plot[4]], linewidth=linewidth, zorder=5)
        scatterX.append(x[-1])
        scatterY.append(y[-1])
        #scatterColor.append(colors[plot[4]])
        scatterColor.append(cm.rainbow(plot[4]/num_pts))
    plt.scatter(scatterX, scatterY, s=0.3, marker='o', c=scatterColor)

    if viewFrom:
        x = ptsFromPix.T[0]
        y = -ptsFromPix.T[1] + height
        plt.scatter(x, y, s=16, marker='s', color='r', edgecolor='black', linewidth=0.6, zorder=15)
        
        # Add station names if provided
        if stations and len(stations) == len(ptsFromPix):
            for i, (station_x, station_y) in enumerate(zip(x, y)):
                # Use actual station name, not a generated name
                station_name = stations[i].name if hasattr(stations[i], 'name') else f"Станция {i+1}"
                plt.annotate(
                    station_name,
                    (station_x, station_y),
                    xytext=(5, 5),
                    textcoords='offset points',
                    fontsize=6,  # Smaller font size
                    fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="black", alpha=0.8),
                    zorder=20
                )
                
    plt.savefig(f'output/plot_reachability_difSt_example{nameinsert}.png')
    #plt.savefig(f'output/plot_reachability_difSt_example{nameinsert}_hires.png', dpi=450, bbox_inches='tight')
#PlotMap(ptsFromPix, ptsToPix, answ3)
#PlotMapDifSt(ptsFromPix, ptsToPix, answ3)


def ClosestPathWithTraceDijkstra(ptsFrom, ptsTo, velocities, G, mesh, mask):
    """
    Calculate optimal paths from multiple starting points to multiple destination points
    using Dijkstra's algorithm for path finding.
    
    Parameters:
        ptsFrom (numpy.array): Array of starting point coordinates
        ptsTo (numpy.array): Array of destination point coordinates
        velocities (numpy.array): Array of velocities for each starting point
        G (networkx.Graph): Navigation graph
        mesh (numpy.array): Array of node coordinates
        mask (numpy.array): Boolean mask indicating valid nodes
    
    Returns:
        tuple: (filtered_destinations, minimum_times, plot_data) - Filtered destination points,
               minimum travel times, and data for plotting
    """
    width = 4113
    height = 3145
    
    maskNorth = np.logical_and(pathNorthPrec.contains_points(mesh), np.logical_not(pathKron.contains_points(mesh)))
    maskSouth = np.logical_and(pathSouthPrec.contains_points(mesh), np.logical_not(pathKron.contains_points(mesh)))
    
    ptsTo = ptsTo[pathZonePrec.contains_points(ptsTo)]
    ptsTo = ptsTo[np.logical_not(pathKron.contains_points(ptsTo))]
    
    times = np.empty((0,np.shape(ptsTo)[0]))
    ptFromNodes = []
    ptToNodes = []
    ptFromInds = []
    ptToInds = []
    distsFrom = [] #dists from point to closest mesh node
    distsTo = [] #same but at the other side
    traces = {}
    for i in range(np.shape(ptsFrom)[0]):
        ptFrom = np.array(ptsFrom[i])
        ptFrom[1] = -ptFrom[1] + height
        ptFromNode, ptFromInd = closestNodeInMesh(mesh, mask, ptFrom)
        ptFromNodes.append(ptFromNode)
        ptFromInds.append(ptFromInd)
        distsFrom.append(distPointToPoint(np.array([ptFrom[0], -ptFrom[1] + height]), ptFromNode))
    distsFrom = np.array(distsFrom)
    ptFromNodes = np.array(ptFromNodes)

    for j in range(np.shape(ptsTo)[0]):
        ptTo = np.array(ptsTo[j])
        if pathNorthPrec.contains_point(ptTo):
            ptTo[1] = -ptTo[1] + height
            ptToNode, ptToInd = closestNodeInMesh(mesh, maskNorth, ptTo)
        else:
            ptTo[1] = -ptTo[1] + height
            ptToNode, ptToInd = closestNodeInMesh(mesh, maskSouth, ptTo)
        ptToNodes.append(ptToNode)
        ptToInds.append(ptToInd)
        distsTo.append(distPointToPoint(np.array([ptTo[0], -ptTo[1] + height]), ptToNode))
    distsTo = np.array(distsTo)
    ptToNodes = np.array(ptToNodes)
        
    traces = {}
    for i in range(np.shape(ptsFrom)[0]):
        traces[ptFromInds[i]] = {}
    for i in range(np.shape(ptsFrom)[0]):
        dists = []
        ptFromInd = ptFromInds[i]
        distsTmp, tracesTmp = nx.single_source_dijkstra(G, ptFromInd)
        for j in range(np.shape(ptsTo)[0]):
            ptToInd = ptToInds[j]
            dists.append(distsTmp[ptToInd])
            traces[ptFromInds[i]][ptToInds[j]] = tracesTmp[ptToInd]
        dists = np.array(dists) + distsFrom[i] + distsTo
        times = np.append(times, np.array([dists / velocities[i]]), axis=0)
    i_args = np.argmin(times, axis=0)
    
    ptsToTimes = []
    for i in range(np.shape(ptsTo)[0]):
        ptsToTimes.append(times[i_args[i]][i])
    ptsToTimes = np.array(ptsToTimes)
    
    plotData = []     
    for i in range(np.shape(ptsTo)[0]):
        optimalStationNumber = i_args[i]
        ptFrom = ptsFrom[optimalStationNumber]
        ptTo = ptsTo[i]
        trace = traces[ptFromInds[optimalStationNumber]][ptToInds[i]]
        x = [ptFrom[0]]
        y = [-ptFrom[1] + height]
        for j in range(len(trace)-1):
            ind = trace[j]
            x.append(mesh[ind][0])
            y.append(-mesh[ind][1] + height)
        x.append(ptTo[0])
        y.append(-ptTo[1] + height)
        x = np.array(x)
        y = np.array(y)
        plotData.append([x, y, ptsToTimes[i], 0, optimalStationNumber])
    
    
    # x, y, time, skip, frompt
    return ptsTo, ptsToTimes, plotData


def expMakeLine(stationCoords, velocities, N):
    """
    Run an experiment using direct line path calculations.
    
    Parameters:
        stationCoords (list): List of station coordinates
        velocities (numpy.array): Array of velocities for each station
        N (int): Number of destination points to generate
    
    Returns:
        tuple: (starting_points, destinations, minimum_times, plot_data) - Starting points,
               destination points, minimum travel times, and data for plotting
    """
    ptsFromPix = []
    for i in stationCoords:
        tmp = (DegreesToDecimalVec(i[0]), DegreesToDecimalVec(i[1]))
        ptsFromPix.append(DecimalToPixelVec(tmp))

    x, y = GenWinterPts(N)
    yrev = -(y - height)

    ptsToPix = np.append(np.array([x]), np.array([yrev]), axis=0).T
    ptsTo, ptsToMinTimes, plotData = ClosestPathWithTraceNew(ptsFromPix, ptsToPix, velocities)


    return ptsFromPix, ptsTo, ptsToMinTimes, plotData

def expMakeGraph(stationCoords, velocities, N, G, Gmesh, Gmask):
    """
    Run an experiment using graph-based path calculations.
    
    Parameters:
        stationCoords (list): List of station coordinates
        velocities (numpy.array): Array of velocities for each station
        N (int): Number of destination points to generate
        G (networkx.Graph): Navigation graph
        Gmesh (numpy.array): Array of node coordinates
        Gmask (numpy.array): Boolean mask indicating valid nodes
    
    Returns:
        tuple: (starting_points, destinations, minimum_times, plot_data) - Starting points,
               destination points, minimum travel times, and data for plotting
    """
    ptsFromPix = []
    for i in stationCoords:
        tmp = (DegreesToDecimalVec(i[0]), DegreesToDecimalVec(i[1]))
        ptsFromPix.append(DecimalToPixelVec(tmp))

    x, y = GenWinterPts(N)
    yrev = -(y - height)

    ptsToPix = np.append(np.array([x]), np.array([yrev]), axis=0).T
    ptsTo, ptsToMinTimes, plotData = ClosestPathWithTraceDijkstra(ptsFromPix, ptsToPix, velocities, G, Gmesh, Gmask)


    return ptsFromPix, ptsTo, ptsToMinTimes, plotData


def probsFromTimes(times, m=10, theta=25):
    """
    Calculate probabilities from travel times using an exponential decay function.
    
    Parameters:
        times (numpy.array): Array of travel times
        m (int, optional): Minimum time parameter. Defaults to 10.
        theta (int, optional): Decay parameter. Defaults to 25.
    
    Returns:
        numpy.array: Array of probabilities
    """
    lmd = np.log(2) * theta * (theta - m) / m
    inner = (1 / np.float128(theta) - 1 / (theta - times.astype(np.float128)))
    return np.exp(inner * lmd)

 