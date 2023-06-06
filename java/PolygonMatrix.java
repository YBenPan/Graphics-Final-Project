import java.util.*;
import java.awt.*;

import parseTables.*;

public class PolygonMatrix extends Matrix {

  public void addBox( double x, double y, double z,
                       double width, double height, double depth ) {
    double x0, y0, z0, x1, y1, z1;
    x0 = x;
    x1 = x+width;
    y0 = y;
    y1 = y-height;
    z0 = z;
    z1 = z-depth;

    //front
    addPolygon(x, y, z, x1, y1, z, x1, y, z);
    addPolygon(x, y, z, x, y1, z, x1, y1, z);
    //back
    addPolygon(x1, y, z1, x, y1, z1, x, y, z1);
    addPolygon(x1, y, z1, x1, y1, z1, x, y1, z1);

    //right side
    addPolygon(x1, y, z, x1, y1, z1, x1, y, z1);
    addPolygon(x1, y, z, x1, y1, z, x1, y1, z1);
    //left side
    addPolygon(x, y, z1, x, y1, z, x, y, z);
    addPolygon(x, y, z1, x, y1, z1, x, y1, z);

    //top
    addPolygon(x, y, z1, x1, y, z, x1, y, z1);
    addPolygon(x, y, z1, x, y, z, x1, y, z);
    //bottom
    addPolygon(x, y1, z, x1, y1, z1, x1, y1, z);
    addPolygon(x, y1, z, x, y1, z1, x1, y1, z1);
  }//addBox

  public void addSphere( double cx, double cy, double cz,
                         double r, int steps ) {

    Matrix points = generateSphere(cx, cy, cz, r, steps);
    int p0, p1, p2, p3, lat, longt;
    int latStop, longStop, latStart, longStart;
    latStart = 0;
    latStop = steps;
    longStart = 1;
    longStop = steps;

    for ( lat = latStart; lat < latStop; lat++ ) {
      for ( longt = longStart; longt < longStop; longt++ ) {

        p0 = lat * (steps+1) + longt;
        p1 = p0 + 1;
        p2 = (p1 + steps) % (steps * (steps+1));
        p3 = (p0 + steps) % (steps * (steps+1));
        double[] point0 = points.get(p0);
        double[] point1 = points.get(p1);
        double[] point2 = points.get(p2);
        double[] point3 = points.get(p3);

        addPolygon(point0[0], point0[1], point0[2],
                   point1[0], point1[1], point1[2],
                   point2[0], point2[1], point2[2]);
        addPolygon(point0[0], point0[1], point0[2],
                   point2[0], point2[1], point2[2],
                   point3[0], point3[1], point3[2]);

      }
    }
  }//addSphere

  private Matrix generateSphere(double cx, double cy, double cz,
                                double r, int steps ) {

    Matrix points = new Matrix();
    int circle, rotation, rot_start, rot_stop, circ_start, circ_stop;
    double x, y, z, rot, circ;

    rot_start = 0;
    rot_stop = steps;
    circ_start = 0;
    circ_stop = steps;

    for (rotation = rot_start; rotation < rot_stop; rotation++) {
      rot = (double)rotation / steps;

      for(circle = circ_start; circle <= circ_stop; circle++){
        circ = (double)circle / steps;

        x = r * Math.cos(Math.PI * circ) + cx;
        y = r * Math.sin(Math.PI * circ) *
          Math.cos(2*Math.PI * rot) + cy;
        z = r * Math.sin(Math.PI * circ) *
          Math.sin(2*Math.PI * rot) + cz;

        /* printf("rotation: %d\tcircle: %d\n", rotation, circle); */
        /* printf("rot: %lf\tcirc: %lf\n", rot, circ); */
        /* printf("sphere point: (%0.2f, %0.2f, %0.2f)\n\n", x, y, z); */
        points.addColumn(x, y, z);
      }
    }
    return points;
  }//generateSphere

  public void addTorus( double cx, double cy, double cz,
                        double r0, double r1, int steps ) {

    Matrix points = generateTorus(cx, cy, cz, r0, r1, steps);
    int p0, p1, p2, p3, lat, longt;
    int latStop, longStop, latStart, longStart;
    latStart = 0;
    latStop = steps;
    longStart = 0;
    longStop = steps;

    for ( lat = latStart; lat < latStop; lat++ ) {
      for ( longt = longStart; longt < longStop; longt++ ) {

        p0 = lat * steps + longt;
        if (longt == steps - 1)
          p1 = p0 - longt;
        else
          p1 = p0 + 1;
        p2 = (p1 + steps) % (steps * steps);
        p3 = (p0 + steps) % (steps * steps);

        double[] point0 = points.get(p0);
        double[] point1 = points.get(p1);
        double[] point2 = points.get(p2);
        double[] point3 = points.get(p3);

        addPolygon(point0[0], point0[1], point0[2],
                   point3[0], point3[1], point3[2],
                   point2[0], point2[1], point2[2]);
        addPolygon(point0[0], point0[1], point0[2],
                   point2[0], point2[1], point2[2],
                   point1[0], point1[1], point1[2]);

      }
    }
  }//addTorus

  private Matrix generateTorus(double cx, double cy, double cz,
                               double r0, double r1, int steps ) {

    Matrix points = new Matrix();
    int circle, rotation, rot_start, rot_stop, circ_start, circ_stop;
    double x, y, z, rot, circ;

    rot_start = 0;
    rot_stop = steps;
    circ_start = 0;
    circ_stop = steps;

    for (rotation = rot_start; rotation < rot_stop; rotation++) {
      rot = (double)rotation / steps;

      for(circle = circ_start; circle < circ_stop; circle++){
        circ = (double)circle / steps;

        x = Math.cos(2*Math.PI * rot) *
          (r0 * Math.cos(2*Math.PI * circ) + r1) + cx;
        y = r0 * Math.sin(2*Math.PI * circ) + cy;
        z = -1*Math.sin(2*Math.PI * rot) *
          (r0 * Math.cos(2*Math.PI * circ) + r1) + cz;

        /* printf("rotation: %d\tcircle: %d\n", rotation, circle); */
        /* printf("rot: %lf\tcirc: %lf\n", rot, circ); */
        /* printf("sphere point: (%0.2f, %0.2f, %0.2f)\n\n", x, y, z); */
        points.addColumn(x, y, z);
      }
    }
    return points;
  }//generateTorus


  public void addPolygon(double x0, double y0, double z0,
                         double x1, double y1, double z1,
                         double x2, double y2, double z2) {
    double[] col0 = {x0, y0, z0, 1};
    double[] col1 = {x1, y1, z1, 1};
    double[] col2 = {x2, y2, z2, 1};
    m.add(col0);
    m.add(col1);
    m.add(col2);
  }//addColumn

  public void drawPolygons(Screen s, GfxVector view, Color amb, GfxVector lightPos, Color lightColor, opConstants reflect) {
    if ( m.size() < 3) {
      System.out.println("Need at least 3 points to draw a polygon");
      return;
    }//not enough points

    for(int point=0; point<m.size()-1; point+=3) {
      double[] p0 = m.get(point);
      double[] p1 = m.get(point+1);
      double[] p2 = m.get(point+2);

      int red = (23 * (point/3))%256;
      int green = (109 * (point/3))%256;
      int blue = (227 * (point/3))%256;
      Color c = new Color(red, green, blue);

      Polygon tri = new Polygon(p0, p1, p2, c);
      double dot = tri.getNormal().dotProduct(view, false);

      if (dot > 0) {

        tri.setReflection(reflect.getAmbient(), reflect.getDiffuse(), reflect.getSpecular() );
        tri.calculteLighting(view, amb, lightPos, lightColor);
        tri.scanlineConvert(s);
        // s.drawLine((int)p0[0], (int)p0[1], (int)p1[0], (int)p1[1], c);
        // s.drawLine((int)p2[0], (int)p2[1], (int)p1[0], (int)p1[1], c);
        // s.drawLine((int)p0[0], (int)p0[1], (int)p2[0], (int)p2[1], c);
      }
    }//draw lines
  }//drawPloygons

}//class PolygonMatrix
