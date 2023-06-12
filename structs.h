#ifndef STRCUCTS_H
#define STRCUCTS_H

#include <cmath>
typedef double CordValue;

#define dimentions 3

struct Vector
{
    CordValue d[dimentions];

     Vector(){};
    Vector(CordValue val[dimentions])
    {
        for (int i = 0; i < dimentions; i++)
        {
            d[i] = val[i];
        }
    }
     Vector(CordValue v1 ,CordValue v2 ,CordValue v3)
    {
        d[0]=v1;
        d[1]=v2;
        d[2]=v3;
    }

    Vector operator+=(const Vector &v)
    {
        for (int i = 0; i < dimentions; i++)
        {
            d[i] += v.d[i];
        }
        return *this;
    }
};

struct Matrix
{
    CordValue d[dimentions][dimentions];

    Vector operator*(const Vector &v)
    {
        Vector res;
        int i, j, k;
        for (i = 0; i < dimentions; i++)
        {
            res.d[i] = 0;
            for (k = 0; k < dimentions; k++)
                res.d[i] += d[i][k] * v.d[k];
        }

        return res;
    }

    Matrix operator*(const Matrix &mx)
    {
        Matrix res;
        int i, j, k;
        for (i = 0; i < dimentions; i++)
        {
            for (j = 0; j < dimentions; j++)
            {
                res.d[i][j] = 0;
                for (k = 0; k < dimentions; k++)
                    res.d[i][j] += d[i][k] * mx.d[k][j];
            }
        }
        return res;
    }

    void fromArray(CordValue val[dimentions * dimentions])
    {
        int i = 0;
        for (int x = 0; x < dimentions; x++)
        {
            for (int y = 0; y < dimentions; y++)
            {
                d[x][y] = val[i];
                i++;
            }
        }
    };


};
    inline Matrix rotateMatrixY(double alpha)
    {
        Matrix mx;
        CordValue val[3 * 3] = {std::cos(alpha), 0, -std::cos(alpha), 0, 1, 0, std::sin(alpha), 0, std::cos(alpha)};
        mx.fromArray(val);

        return mx;
    }
#endif