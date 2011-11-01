filename = "DKC_KVDcombinaties_final.txt"
file = open(filename,'r')
lines = []
for line in file:
	lines.append(line)
file.close()
output = open("vakPerKlasOutput.txt","w")
for line in lines:
	values = line.split(" ; ")
	output.write("vak = entities.VakPerKlas(jaargang='2010-2011', klas='"+values[0]+"', vakCode='"+values[1]+"', docentID='"+values[2][:-1]+"')\n")
	output.write("vak.put()\n")
	
output.close()


"""
    vak = entities.VakPerKlas(jaargang='2010-2011', klas='1B1', vakCode='NED', docentID='BAARR')
    vak.put()
1B1 ; NED ; BAARR
    
"""
