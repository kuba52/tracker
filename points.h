#ifndef Point_H
#define Point_H

#include "structs.h"

struct Point{
    CordValue x;
    CordValue y;

    Point(){};
    Point(const CordValue x, const CordValue y) :
    x(x),
    y(y)
  {}
};

#endif