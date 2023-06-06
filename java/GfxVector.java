import java.util.*;
import java.io.*;


public class GfxVector {

  private double[] components;
  private double[] normalized;
  private double magnitude;

  public GfxVector() {
    components = new double[3];
    normalized = new double[3];
  }

  public GfxVector(double x, double y, double z) {

    this();

    components[0] = x;
    components[1] = y;
    components[2] = z;

    setMagnitude();
    setNormalized();
  }//constructor

  public GfxVector(GfxVector v) {
    components = Arrays.copyOf(v.components, 3);
    normalized = Arrays.copyOf(v.normalized, 3);
    magnitude = v.magnitude;
  }//copy constructor

  public GfxVector(double[] p0, double[] p1) {
    this();

    components[0] = p1[0] - p0[0];
    components[1] = p1[1] - p0[1];
    components[2] = p1[2] - p0[2];

    setNormalized();
    setMagnitude();
  }//point constructor

  private void setMagnitude() {
    magnitude = components[0] * components[0];
    magnitude+= components[1] * components[1];
    magnitude+= components[2] * components[2];

    magnitude = Math.sqrt(magnitude);
  }//setMagnitude

  private void setNormalized() {
    normalized[0] = components[0] / magnitude;
    normalized[1] = components[1] / magnitude;
    normalized[2] = components[2] / magnitude;
  }//setNormalized

  public void scalarMultiplty(double factor) {
    for (int i=0; i<3; i++) {
      components[i]*= factor;
      normalized[i]*= factor;
    }
  }//scalarMultiplty

  public void subtract(GfxVector v) {
    for (int i=0; i<3; i++) {
      components[i] -= v.components[i];
      normalized[i] -= v.normalized[i];
    }
  }//subtract

  public double dotProduct(GfxVector v, boolean useNormal) {
    double[] v0 = components;
    double[] v1 = v.components;
    if (useNormal) {
      v0 = normalized;
      v1 = v.normalized;
    }
    double dot = v0[0] * v1[0];
    dot+= v0[1]* v1[1];
    dot+= v0[2] * v1[2];
    return dot;
  }//dotProduct

  public GfxVector crossProduct(GfxVector v) {
    double x, y, z;

    x = components[1] * v.components[2] - components[2] * v.components[1];
    y = components[2] * v.components[0] - components[0] * v.components[2];
    z = components[0] * v.components[1] - components[1] * v.components[0];

    return new GfxVector(x, y, z);
  }//crossProduct

  public String toString() {
    String s = "";
    s+= "vector: <" + components[0] + ", " + components[1] + ", " + components[2] + ">\n";
    s+= "normal: <" + normalized[0] + ", " + normalized[1] + ", " + normalized[2] + ">\n";
    s+= "magnitude: " + magnitude;
    return s;
  }//toString

}//GfxVector
