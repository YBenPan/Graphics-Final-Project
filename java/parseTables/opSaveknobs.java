package parseTables;

import parseTables.*;
import java.util.*;

public class opSaveknobs extends opCode
{
    private String name;
    private HashMap<String, Double> knobs;
    public opSaveknobs(String name)
    {
	this.name = name;
    knobs = new HashMap<String, Double>();
    }
    public String getName()
    {
	return name;
    }
    public void addKnob(String name, Double val) {
        knobs.put(name, val);
    }
    public Double getKnob(String name) {
        return knobs.get(name);
    }
    public String toString()
    {
	return "Saveknobs: "+name;
    }
}
