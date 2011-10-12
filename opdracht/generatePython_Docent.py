filename = "DKC_docenten_final.txt"
file = open(filename,'r')
lines = []
for line in file:
	lines.append(line)
file.close()
outputLines = []
	
for line in lines:
	values = line.split(" ; ")
	str = "docent = entities.Docent(docentID='"+values[0]+"', "
	str += "aanhef='"+values[1]+"', "
	str += "naam='"+values[2]+"', "
	str += "postvaknummer="+values[3]+", " 
	str += "email='"+values[4][:-1]+"', "
	str += "wachtwoord='a')"
	outputLines.append(str)
	
output = open("docentenOutput.txt","w")
for line in outputLines:
	output.write(line+"\n")
	output.write("docent.put()\n")
output.close()	

"""
docent = entities.Docent(docentID='BAARR',aanhef='mw.',naam='drs. R.Baart',postvaknummer=41, email = 'BAARR@DKC.NL', wachtwoord='a')
docent.put()
BAARR ; mw. ; drs. R.Baart ; 41 ; BAARR@DKC.NL
"""
