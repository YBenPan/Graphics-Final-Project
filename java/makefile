run: all
	java MDL face.mdl

all: subs MDL.class

subs:
	$(MAKE) -C parseTables
	$(MAKE) -C parser

MDL.class: MDL.java MDLReader.class
	javac -classpath "." MDL.java

MDLReader.class: MDLReader.java Screen.class Matrix.class EdgeMatrix.class PolygonMatrix.class GfxVector.class
	javac -cp "." MDLReader.java

Matrix.class: Matrix.java
	javac Matrix.java

PolygonMatrix.class: PolygonMatrix.java Polygon.class Matrix.java Screen.class GfxVector.class
	javac PolygonMatrix.java

Polygon.class: Polygon.java GfxVector.class
	javac Polygon.java

GfxVector.class: GfxVector.java
	javac GfxVector.java

EdgeMatrix.class: EdgeMatrix.java Matrix.java Screen.class
	javac EdgeMatrix.java

Screen.class: Screen.java
	javac Screen.java

clean:
	$(MAKE) -C parseTables clean
	$(MAKE) -C parser clean
	rm *.class
	rm *~
