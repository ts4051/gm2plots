#Plot the standard model values for a_mu and the associated errors
#Tom Stuttard (29th Nov 2016)

#TODO Add deviation
#TODO Compare theory and experiment uncertainties

import matplotlib.pyplot as plt

#Define a_mu values and errors for the various contributions
#Using TDR table 2.3 for values
labels = list()
amuValues = list()
amuErrors = list()

#QED
labels.append("QED")
amuValues.append(116584718.951e-11)
amuErrors.append( ( 0.009 + 0.019 + 0.007 +  0.077 ) * 1.e-11 )

#EW
labels.append("EW")
amuValues.append(153.6e-11)
amuErrors.append( 1.0 * 1.e-11 )

#Hadronic
labels.append("Hadronic LO")
amuValues.append( 6923.e-11 )
amuErrors.append( 42. * 1.e-11 )

labels.append("Hadronic HO")
amuValues.append( 98.4e-11 )
amuErrors.append( 0.7 * 1.e-11 )

labels.append("Hadronic LbL")
amuValues.append( 105.e-11 )
amuErrors.append( 26. * 1.e-11 )

#Re-calculate amu values in absoliute terms (plotting -ve a bit tricky on a pie chart)
amuAbsValues = [ abs(v) for v in amuValues ]

#Re-calculate as percentages
amuAbsValuesSum = sum(amuAbsValues)
amuAbsValuesPercentages = [ 100. * v / amuAbsValuesSum for v in amuAbsValues]

amuErrorsSum = sum(amuErrors)
amuErrorsPercentages = [ 100. * e / amuErrorsSum for e in amuErrors]

#Draw pie chart of values
plt.figure(facecolor='white') #White background
plt.pie(amuAbsValuesPercentages, explode=([0]*len(labels)), labels=[labels[0],'Others','','',''] )#, autopct='%1.1f%%')
plt.axis('equal') #Make pie a circle
plt.show()

#Draw pie chart of errors
plt.figure(facecolor='white') #White background
plt.pie(amuErrorsPercentages, explode=([0]*len(labels)), labels=labels )#, autopct='%1.1f%%')
plt.axis('equal') #Make pie a circle
plt.show()

