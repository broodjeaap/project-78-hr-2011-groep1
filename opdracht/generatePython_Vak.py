filename = "DKC_vakken_final.txt"
file = open(filename,'r')
lines = []
for line in file:
	lines.append(line)
file.close()
outputLines = []
	
for line in lines:
	values = line.split(" ; ")
	str = "vak = entities.Vak(vakCode='"+values[0]+"', "
	str += "vakNaam='"+values[1][:-1]+"')"
	outputLines.append(str)
	
output = open("vakOutput.txt","w")
for line in outputLines:
	output.write(line+"\n")
	output.write("vak.put()\n")
output.close()	

"""
docent = entities.Docent(docentID='BAARR',aanhef='mw.',naam='drs. R.Baart',postvaknummer=41, email = 'BAARR@DKC.NL', wachtwoord='a')
docent.put()
BAARR ; mw. ; drs. R.Baart ; 41 ; BAARR@DKC.NL
"""
