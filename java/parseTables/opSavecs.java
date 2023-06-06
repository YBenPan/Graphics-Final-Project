package parseTables;

import parseTables.*;

public class opSavecs extends opCode
{
    private String name;
    private Object csystem;

    public opSavecs(String name)
    {
	this.name = name;
    }
    public String getName()
    {
	return name;
    }
    public Object getCS() {
        return csystem;
    }
    public void setCS(Object cs) {
        csystem = cs;
    }
    public String toString()
    {
	return "SaveCS: "+name +"\n"+ csystem;
    }
}
