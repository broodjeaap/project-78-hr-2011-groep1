leerlingenFile = "DKC_leerlingen_final.txt"
leerlingenFile = open(leerlingenFile,'r')
leerlingArray = []

for line in leerlingenFile:
        leerlingArray.append(line.split(" ; "))
leerlingenFile.close()

voogdFile = "DKC_voogdouder_final.txt"
voogdFile = open(voogdFile,'r')
voogdArray = []

for line in voogdFile:
        voogdArray.append(line.split(" ; "))
voogdFile.close()

output = []
for leerling in leerlingArray:
        for voogd in voogdArray:
                if(leerling[6][:-1] == voogd[0]):
                        tmp = []
                        tmp.append(leerling[0])
                        tmp.append(leerling[1])
                        tmp.append(leerling[2])
                        tmp.append(leerling[3])
                        tmp.append(leerling[4])
                        tmp.append(leerling[5])
                        tmp.append(voogd[1])
                        tmp.append(voogd[2])
                        tmp.append(voogd[3])
                        tmp.append(voogd[4])
                        tmp.append(voogd[5])
                        tmp.append(voogd[6])
                        tmp.append(voogd[7])
                        tmp.append(voogd[8])
                        tmp.append(voogd[9])
                        tmp.append(voogd[10])
                        tmp.append(voogd[11])
                        tmp.append(voogd[12][:-1])
                        
                        output.append(tmp)
        
outputFile = open("leerlingOutput.txt","w")
for line in output:
        outputFile.write("leerling = entities.Leerling( leerlingID='"+line[0]+"', wachtwoord='a', voornaam=unicode('"+line[1]+"','latin-1'), tussenvoegsel='"+line[2]+"', achternaam=unicode('"+line[3]+"','latin-1'), geslacht='"+line[4]+"', klas='"+line[5]+"', aanhefVerzorger='"+line[6]+"', initialenVerzorger='"+line[7]+"', voorvoegselsVerzorger='"+line[8]+"', achternaamVerzorger=unicode('"+line[9]+"','latin-1'), rolVerzorger='"+line[10]+"', adres='"+line[11]+"', huisnummer='"+line[12]+"',  woonplaats='"+line[13]+"',  postcode='"+line[14]+"',  mobielnummer='"+line[15]+"',  vastnummer='"+line[16]+"',  email='"+line[17]+"', )\n")

        outputFile.write("leerling.put()\n")
outputFile.close()      


"""
for line in lines:
        values = line.split(" ; ")
        str = "vak = entities.Vak(vakCode='"+values[0]+"', "
        str += "vakNaam='"+values[1][:-1]+"')"
        outputLines.append(str)
"""
