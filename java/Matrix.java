import java.util.*;

public class Matrix {

  public static int POINT_SIZE = 4;
  public static int TRANSLATE = 0;
  public static int SCALE = 1;
  public static int ROTATE = 2;
  public static int HERMITE = 3;
  public static int BEZIER = 4;

  protected ArrayList<double []>m;

  Matrix() {
    m = new ArrayList<double []>();
  }//constructor

  Matrix(int transformType, double x, double y, double z) {
    ident();
    if (transformType == TRANSLATE)
      makeTranslate(x, y, z);
    else if (transformType == SCALE)
      makeScale(x, y, z);
  }//translate/scale constructor

  Matrix(int transformType, double theta, char axis) {
    ident();
    if (transformType == ROTATE) {
      if (axis == 'X' || axis == 'x')
        makeRotX(theta);
      else if (axis == 'Y' || axis == 'y')
        makeRotY(theta);
      else if (axis == 'Z' || axis == 'z')
        makeRotZ(theta);
    }
  }//roate constrcutor

  Matrix(int curveType, double p0, double p1, double p2, double p3) {
    this();
    Matrix curveMat = new Matrix(curveType);
    double[] col = {p0, p1, p2, p3};
    m.add(col);

    mult(curveMat);
  }//coefiecient constructor

  Matrix(int curveType) {
    this();
    if (curveType == HERMITE) {
      double[] col0 = {2, -3, 0, 1};
      double[] col1 = {-2, 3, 0, 0};
      double[] col2 = {1, -2, 1, 0};
      double[] col3 = {1, -1, 0, 0};
      m.add(col0);
      m.add(col1);
      m.add(col2);
      m.add(col3);
    }
    else if (curveType == BEZIER) {
      double[] col0 = {-1, 3, -3, 1};
      double[] col1 = {3, -6, 3, 0};
      double[] col2 = {-3, 3, 0, 0};
      double[] col3 = {1, 0, 0, 0};
      m.add(col0);
      m.add(col1);
      m.add(col2);
      m.add(col3);
    }
  }//curve generator constructor

  private void makeTranslate(double x, double y, double z){
    double[] lastCol = m.get(3);
    lastCol[0] = x;
    lastCol[1] = y;
    lastCol[2] = z;
  }//makeTranslate

  private void makeScale(double x, double y, double z) {
    m.get(0)[0] = x;
    m.get(1)[1] = y;
    m.get(2)[2] = z;
  }//makeScale

  private void makeRotX(double theta) {
    m.get(1)[1] = Math.cos(theta);
    m.get(2)[1] = -1*Math.sin(theta);
    m.get(1)[2] = Math.sin(theta);
    m.get(2)[2] = Math.cos(theta);
  }//makeRotX

  private void makeRotY(double theta) {
    m.get(0)[0] = Math.cos(theta);
    m.get(0)[2] = -1*Math.sin(theta);
    m.get(2)[0] = Math.sin(theta);
    m.get(2)[2] = Math.cos(theta);
  }//makeRotX

  private void makeRotZ(double theta) {
    m.get(0)[0] = Math.cos(theta);
    m.get(1)[0] = -1*Math.sin(theta);
    m.get(0)[1] = Math.sin(theta);
    m.get(1)[1] = Math.cos(theta);
  }//makeRotX

  public void addColumn(double x, double y, double z) {
    double[] col = {x, y, z, 1};
    m.add(col);
  }//addColumn

  public void ident() {
    m = new ArrayList<double []>();
    for (int i=0; i<POINT_SIZE; i++) {
      double[] point = new double[POINT_SIZE];
      point[i] = 1;
      m.add(point);
    }
  }//ident



  public void mult(Matrix a) {
    double[] tmp = new double[POINT_SIZE];
    for (int c=0; c<m.size(); c++) {
      double[] point = m.get(c);
      //copy values from m over
      for (int r=0; r < point.length; r++)
        tmp[r] = point[r];

      for (int r=0; r < point.length; r++) {
        m.get(c)[r] = a.m.get(0)[r] * tmp[0] +
          a.m.get(1)[r] * tmp[1] +
          a.m.get(2)[r] * tmp[2] +
          a.m.get(3)[r] * tmp[3];
      }
    }
  }//mult

  public void clear() {
    m = new ArrayList<double[] >();
  }//clear

  public double[] get(int i) {
    return m.get(i);
  }

  public Matrix copy() {
    Matrix nm = new Matrix();
    for (int c=0; c<m.size(); c++) {
      nm.m.add( Arrays.copyOf(m.get(c), POINT_SIZE));
    }
    return nm;
  }

  public String toString() {

    String s = "";
    if (m.size() == 0) {
      return s;
    }

    for (int i=0; i<POINT_SIZE; i++) {
      for (double[] p : m) {
        s+= p[i] + " ";
      }
      s+= "\n";
    }
    return s;
  }
}//Matrix
