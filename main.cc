#include <iostream>
#include <numbers>
#include <cmath>
#include "structs.h"
#include "points.h"
#include <fstream>

double fov;
double distanceToPlane;
double planeSize[2];
int resolution[2];
double dd = 1;

Point fromScreenToPlane(int x, int y)
{

    Vector v(x / resolution[0] * planeSize[1], y / resolution[1] * planeSize[0], 0);
    v += Vector(-planeSize[1] / 2, -planeSize[0] / 2, -distanceToPlane);
    // Matrix r  =

    rotateMatrixY(std::numbers::pi / 2) * v;

    return Point(dd * x * planeSize[0] / resolution[0], dd * y * planeSize[1] / resolution[1]);
}

int main(int argc, char *argv[])
{
    std::ifstream inF;
    std::ofstream outF;
    inF.open("data.txt", std::ios::in);
    outF.open("data2.txt", std::ios::out | std::ios::trunc);
    int x, y;
    Point p;

    if (argc < 4)
    {
        std::cout << "usage: " << argv[0] << " [rosolution Width In Pixels] [rosolution Hight In Pixels]  [distance to plane] (optional) [fov in Radians]\n";
        return 1;
    }

    resolution[0] = std::atoi(argv[1]);
    resolution[1] = std::atoi(argv[2]);
    distanceToPlane = std::stod(argv[3]);
    // resolution[0]= 1280;
    // resolution[1] = 720

    fov = 0.68080883 * 2;
    if (argc > 4)
        fov = std::stod(argv[4]);

    std::cerr << "width,hight: " << resolution[0] << "," << resolution[1] << "\n";
    std::cerr << "fov: " << fov << "\n";

    planeSize[0] = std::tan(fov / 2) * distanceToPlane * 2;
    planeSize[1] = planeSize[0] * (dd * resolution[1] / resolution[0]);
    std::cerr << "plane" << planeSize[0] << "\n";

    // std::cout<<planeSize[0]<<" "<<planeSize[1]<<"\n";
    double time;
    std::string str;
    while (1)
    {
        // if (!inF.eof())
        // {
        
        if (!inF.eof())
        {
            inF >> str;
            if (str == "dupa"){
                outF.close();
                inF.close();
                return 0;
            }
            x = std::atoi(str.c_str());
            inF >> y >> time;
            p = fromScreenToPlane(x, y);
            outF << p.x << " " << p.y << " " << time << "\n";
        }
        else{
            // inF.sync();
            outF.close();
            return 1;
        }
        // outF<<x<<" "<<y<<" "<<time<<"\n";
        // }
        // in
    }
}