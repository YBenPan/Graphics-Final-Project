/*========== MDLReader.java ==========
  MDLReader objects minimally contain an ArrayList<opCode> containing
  the opCodes generated when an mdl file is run through the java created
  lexer/parser, as well as the associated SymTab (Symbol Table).

  The provided methods are a constructor, and methods to print out the
  entries in the symbol table and command ArrayList.

  Your job is to go through each entry in opCodes and perform
  the required action from the list below:

  push: push a new origin matrix onto the origin stack
  pop: remove the top matrix on the origin stack

  move/scale/rotate: create a transformation matrix 
                     based on the provided values, then 
		     multiply the current top of the
		     origins stack by it.

  box/sphere/torus: create a solid object based on the
                    provided values. Store that in a 
		    temporary matrix, multiply it by the
		    current top of the origins stack, then
		    call draw_polygons.

  line: create a line based on the provided values. Store 
        that in a temporary matrix, multiply it by the
	current top of the origins stack, then call draw_lines.

  save: save the current screen with the provided filename

  =========================*/

import java.util.*;
import java.io.*;
import java.awt.Color;

import parser.*;
import parseTables.*;

public class  MDLReader {

    ArrayList<opCode> opcodes;
    SymTab symbols;
    Set<String> symKeys;

    Color c;
    Screen s;
    EdgeMatrix edges;
    PolygonMatrix polys;

    GfxVector view;
    Color ambient;
    GfxVector lightPos;
    Color lightColor;

    Matrix transform;
    Stack<Matrix> csystems;

    public MDLReader(ArrayList<opCode> o, SymTab st) {

		opcodes = o;
		symbols = st;
		symKeys = st.keySet();
	
		c = Color.GREEN;
		s = new Screen();
		edges = new EdgeMatrix();
		polys = new PolygonMatrix();

		view = new GfxVector(0, 0, 1);
		ambient = new Color(50, 50, 50);
		lightPos = new GfxVector(0.5, 0.75, 1);
		lightColor = new Color(255, 255, 255);

		transform = new Matrix();
		transform.ident();
		csystems = new Stack<Matrix>();
		csystems.push(transform);
    }//constructor

    public void printCommands() {
	
		Iterator i = opcodes.iterator();

		while (i.hasNext()) {
			System.out.println(i.next());
	    }
    }//printCommands

    public void printSymbols() {

		Iterator i;

		i = symKeys.iterator();
		System.out.println("Symbol Table:");

		while (i.hasNext()) {
			String key = (String)i.next();
			Object value=symbols.get(key);
			System.out.println(""+key+"="+value);
		}
    }//printSymbols

    /*======== public void process()) ==========
      Inputs:   
      Returns: 

      Insert your interpreting code here

      you can use instanceof to check what kind of op
      you are looking at:
          if ( oc instanceof opPush ) ...
	  
      you will need to typecast in order to get the
      operation specific data values
      ====================*/
    public void process() {
	
	Iterator i = opcodes.iterator();
	opCode oc;
	double step2d = 0.01;
    int step3d = 100;


	opConstants white = new opConstants("_white",
										new double[]{0.2, 0.2, 0.2},
										new double[]{0.5, 0.5, 0.5},
										new double[]{0.5, 0.5, 0.5},
										null);
	opConstants reflect = white;

	while (i.hasNext()) {
	    
	    oc = (opCode)i.next();
	    String command = oc.getClass().getName();

	    if ( oc instanceof opPush ) {
			csystems.push( csystems.peek().copy() );
	    }//push
	    
	    else if ( oc instanceof opPop ) {
			csystems.pop();
	    }//pop
	    
	    else if ( oc instanceof opSphere ) {
		
			polys.addSphere( ((opSphere)oc).getCenter()[0],
							 ((opSphere)oc).getCenter()[1],
							 ((opSphere)oc).getCenter()[2],
							 ((opSphere)oc).getR(), step3d);
			polys.mult(csystems.peek());

			if ( ((opShape)oc).getConstants() != null ) {
				reflect = (opConstants)(symbols.get( ((opShape)oc).getConstants() ));
			}//retrieve constants
			polys.drawPolygons(s, view, ambient, lightPos, lightColor, reflect);
			polys.clear();
			reflect = white;
	    }//sphere

	    else if ( oc instanceof opTorus ) {
		
			polys.addTorus( ((opTorus)oc).getCenter()[0],
						  ((opTorus)oc).getCenter()[1],
						  ((opTorus)oc).getCenter()[2],
						  ((opTorus)oc).getr(),
						  ((opTorus)oc).getR(), step3d);
			polys.mult(csystems.peek());
			if ( ((opShape)oc).getConstants() != null ) {
				reflect = (opConstants)(symbols.get( ((opShape)oc).getConstants() ));
			}//retrieve constants
			polys.drawPolygons(s, view, ambient, lightPos, lightColor, reflect);
			polys.clear();
			reflect = white;
	    }//torus

	    else if ( oc instanceof opBox ) {
			polys.addBox( ((opBox)oc).getP1()[0],
						((opBox)oc).getP1()[1],
						((opBox)oc).getP1()[2],
						((opBox)oc).getP2()[0],
						((opBox)oc).getP2()[1],
						((opBox)oc).getP2()[2] );
			polys.mult(csystems.peek());
			if ( ((opShape)oc).getConstants() != null ) {
				reflect = (opConstants)(symbols.get( ((opShape)oc).getConstants() ));
			}//retrieve constants
			polys.drawPolygons(s, view, ambient, lightPos, lightColor, reflect);
			polys.clear();
			reflect = white;
	    }//box

		else if ( oc instanceof opLine ) {

			edges.addEdge( ((opLine)oc).getP1()[0],
						   ((opLine)oc).getP1()[1],
						   ((opLine)oc).getP1()[2],
						   ((opLine)oc).getP2()[0],
						   ((opLine)oc).getP2()[1],
						   ((opLine)oc).getP2()[2] );
			edges.mult(csystems.peek());
			edges.drawEdges(s, c);
			polys.clear();
	    }//line

	    else if ( oc instanceof opMove ) {

			Matrix tmp = new Matrix(Matrix.TRANSLATE,
								  ((opMove)oc).getValues()[0],
								  ((opMove)oc).getValues()[1],
								  ((opMove)oc).getValues()[2] );
			tmp.mult(csystems.pop());
			csystems.push(tmp);
	    }//move

	    else if ( oc instanceof opScale ) {

			Matrix tmp = new Matrix(Matrix.SCALE,
								  ((opScale)oc).getValues()[0],
								  ((opScale)oc).getValues()[1],
								  ((opScale)oc).getValues()[2] );
			tmp.mult(csystems.pop());
			csystems.push(tmp);
	    }//scale

	    else if ( oc instanceof opRotate ) {
			double angle = ((opRotate)oc).getDeg() * (Math.PI / 180);
			char axis = ((opRotate)oc).getAxis();
			Matrix tmp = new Matrix(Matrix.ROTATE, angle, axis);
			tmp.mult(csystems.pop());
			csystems.push(tmp);
	    }//rotate

	    else if ( oc instanceof opSave ) {
			s.saveExtension( ((opSave)oc).getName() );
	    }//save
		else if ( oc instanceof opDisplay ) {
			s.display();
	    }//save
		
	}//end loop
    }
}
