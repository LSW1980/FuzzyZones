import matplotlib.pyplot as plt
import numpy as np, skfuzzy as fuzz
from skfuzzy import control as ctrl

# define domain interval and resolution of fuzzy sets inputs-output
err      = ctrl.Antecedent(np.arange(-4,4, 0.1), 'err')
errRate  = ctrl.Antecedent(np.arange(-10,10, 0.1), 'errRate')
outPower = ctrl.Consequent(np.arange(-100,100, 0.1), 'outPower')

# define fuzzy set shapes or membership functions
err['N'] = fuzz.trapmf(err.universe,[-4,-4,-2,0])
err['Z'] = fuzz.trimf(err.universe,[-2,0,2])
err['P'] = fuzz.trapmf(err.universe,[0,2,4,4])

errRate['N'] = fuzz.trapmf(errRate.universe,[-10,-10,-5,0])
errRate['Z'] = fuzz.trimf(errRate.universe,[-5,0,5])
errRate['P'] = fuzz.trapmf(errRate.universe,[0,5,10,10])

outPower['C']  = fuzz.trapmf(outPower.universe, [-100,-100,-50,0])
outPower['NC'] = fuzz.trimf(outPower.universe, [-50,0,50])
outPower['H']  = fuzz.trapmf(outPower.universe, [0,50,100,100])

# sample view of membership functions
err['Z'].view()
errRate.view()
outPower.view()

# develop rule base for two inputs and one output
rule1 = ctrl.Rule(err['N'] & errRate['N'], outPower['C'])
rule2 = ctrl.Rule(err['Z'] & errRate['N'], outPower['H'])
rule3 = ctrl.Rule(err['P'] & errRate['N'], outPower['H'])
rule4 = ctrl.Rule(err['N'] & errRate['Z'], outPower['C'])
rule5 = ctrl.Rule(err['Z'] & errRate['Z'], outPower['NC'])
rule6 = ctrl.Rule(err['P'] & errRate['Z'], outPower['H'])
rule7 = ctrl.Rule(err['N'] & errRate['P'], outPower['C'])
rule8 = ctrl.Rule(err['Z'] & errRate['P'], outPower['C'])
rule9 = ctrl.Rule(err['P'] & errRate['P'], outPower['H'])

rule1.view()

# create a control system base on the rules
powerLevel_ctrl = ctrl.ControlSystem([rule1,rule2,rule3,
                rule4,rule5,rule6,rule7,rule8,rule9])

# simulate control system                
powerLevel = ctrl.ControlSystemSimulation(powerLevel_ctrl)

# specifying crisp input values
powerLevel.input['err'] = -1.5
powerLevel.input['errRate'] = 2.0

# behind the scene Mamdani computation of interpolation,
# clipping, aggregation and centroid calculation
powerLevel.compute()

print 'Power ouput percentage: ', powerLevel.output['outPower']
# graphical view of power output
outPower.view(sim=powerLevel)
plt.title('% Power output - vertical line')
plt.show()
