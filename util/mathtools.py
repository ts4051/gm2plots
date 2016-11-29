import numpy as np
import math

#
# Calculate distance of closest approach of a line to a point
#

def dca(lineStart,lineEnd,point):

    #d = | ( r0 - r1 ) x ( r0 - r2 ) | / | r2 - r1 |
    #where r0 is point, r1 is line start and r2 is line end
    #http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html

    numerator = np.cross( (point-lineStart), (point-lineEnd) )
    numerator = math.sqrt( np.dot(numerator,numerator) )

    denominator = lineEnd - lineStart
    denominator = math.sqrt( np.dot(denominator,denominator) )

    d = numerator / denominator

    return d
