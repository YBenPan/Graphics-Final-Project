import java.util.*;
import java.io.*;

import parser.*;
import parseTables.*;

public class MDL {
  public static void main(String args[]) throws ParseException {
	ArrayList<opCode> a;
	SymTab s;
	MdlParser parser;
	String file;
	if ( args.length == 1 )
	    file = args[0];
	else
	    file = "test.mdl";
	try {
	    parser = new MdlParser(new FileReader( file ));
	}
	catch ( IOException e ) {
	    parser = new MdlParser(System.in);
	}
	
	parser.start();
	a = parser.getOps();
	s = parser.getSymTab();

	MDLReader mr = new MDLReader(a, s);
	mr.process();
  }//main
}//class mdl
