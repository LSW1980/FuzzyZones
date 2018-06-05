import matplotlib.pyplot as plt
import numpy as np, skfuzzy as fuzz
from skfuzzy import control as ctrl

# define domain interval and resolution of fuzzy sets inputs-output
x_err      = np.arange(-4,4, 0.1)
x_errRate  = np.arange(-10,10, 0.1)
x_outPower = np.arange(-100,100, 0.1)

# define fuzzy set shapes or membership functions
err_N = fuzz.trapmf(x_err,[-4,-4,-2,0])
err_Z = fuzz.trimf(x_err,[-2,0,2])
err_P = fuzz.trapmf(x_err,[0,2,4,4])

errRate_N = fuzz.trapmf(x_errRate,[-10,-10,-5,0])
errRate_Z = fuzz.trimf(x_errRate,[-5,0,5])
errRate_P = fuzz.trapmf(x_errRate,[0,5,10,10])

outPower_C  = fuzz.trapmf(x_outPower, [-100,-100,-50,0])
outPower_NC = fuzz.trimf(x_outPower, [-50,0,50])
outPower_H  = fuzz.trapmf(x_outPower, [0,50,100,100])

# Visualize membership functions ---------------------------------

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize=(11, 7))
ax1.plot(x_err, err_N, 'b', lw=2, label='err_N')
ax1.plot(x_err, err_P, 'r', lw=2, label='err_P')
ax1.plot(x_err, err_Z, 'orange', lw=2, label='err_Z')
ax1.set_xlabel('err', fontsize=10)
ax1.set_ylabel('Membership', fontsize=10)
ax1.set_title('Temp Different Fuzzy Sets')
ax1.legend()

ax2.plot(x_errRate, errRate_N, 'b', lw=2, label='errRate_N')
ax2.plot(x_errRate, errRate_P, 'r', lw=2, label='errRate_P')
ax2.plot(x_errRate, errRate_Z, 'orange', lw=2, label='errRate_Z')
ax2.set_xlabel('errRate', fontsize=10)
ax2.set_ylabel('Membership', fontsize=10)
ax2.set_title('Rate of Temp Change Fuzzy Sets')
ax2.legend()

ax3.plot(x_outPower, outPower_C, 'b', lw=2, label='outPower_C')
ax3.plot(x_outPower, outPower_H, 'r', lw=2, label='outPower_H')
ax3.plot(x_outPower, outPower_NC, 'orange', lw=2, label='outPower_NC')
ax3.set_xlabel('outPower', fontsize=10)
ax3.set_ylabel('Membership', fontsize=10)
ax3.set_title("outPower Fuzzy Sets")
ax3.legend()

plt.tight_layout(pad=0.4, w_pad=2, h_pad=2)

#--------------------------------------------------------------------

# err, errRate = eval(input("Enter 'err, errRate' values: "))
# specifying crisp input values
err, errRate = -1, 2.5

# interpolate to get membership values
# of all fuzzy sets from above inputs
im_err_N = fuzz.interp_membership(x_err, err_N, err)
im_err_Z = fuzz.interp_membership(x_err, err_Z, err)
im_err_P = fuzz.interp_membership(x_err, err_P, err)

im_errRate_N = fuzz.interp_membership(x_errRate, errRate_N, errRate)
im_errRate_Z = fuzz.interp_membership(x_errRate, errRate_Z, errRate)
im_errRate_P = fuzz.interp_membership(x_errRate, errRate_P, errRate)

# activate Antecedent-input of all rules, use AND or 
# minimum operator to get Consequent-output membership values
R1 = min(im_err_N , im_errRate_N) # --> outPower_C 
R2 = min(im_err_Z , im_errRate_N) # --> outPower_H
R3 = min(im_err_P , im_errRate_N) # --> outPower_H
R4 = min(im_err_N , im_errRate_Z) # --> outPower_C
R5 = min(im_err_Z , im_errRate_Z) # --> outPower_NC
R6 = min(im_err_P , im_errRate_Z) # --> outPower_H
R7 = min(im_err_N , im_errRate_P) # --> outPower_C 
R8 = min(im_err_Z , im_errRate_P) # --> outPower_C
R9 = min(im_err_P , im_errRate_P) # --> outPower_H

# Root Sum Squared Method - bypass clipping each rule output
im_outPower_C  = (R1**2 + R4**2 + R7**2 + R8**2)**0.5
im_outPower_NC = (R5**2)**0.5
im_outPower_H  = (R2**2 + R3**2 + R6**2 + R9**2)**0.5

Cx_C  = (50**2 + 50*100 + 100**2)/(3*150)-100 #stationary centroid/singleton of Cool
Cx_NC = 0    #locked singleton at zero (symmetrical)
Cx_H  = 100-(50**2 + 50*100 + 100**2)/(3*150) #centroid Cx of Hot Fuzzy Set, from traperzoid formula

#Weighted Average using interpolate membership and
#original Cx centroid of fuzzy sets (original areas)
#can also use its max/min outer edges

powerLevel = (Cx_C*im_outPower_C + Cx_NC*im_outPower_NC
    + Cx_H*im_outPower_H)/(im_outPower_C + im_outPower_NC + im_outPower_H)

print 'Percent Power Output: '  , powerLevel

#clip each fuzzy set with Root Sum Squared Method value
#use for print out
clip_outPower_C = np.fmin(im_outPower_C, outPower_C)
clip_outPower_NC = np.fmin(im_outPower_NC, outPower_NC)
clip_outPower_H = np.fmin(im_outPower_H, outPower_H)

clip_aggregated = np.fmax(clip_outPower_C,
                     np.fmax(clip_outPower_NC, clip_outPower_H))

# graphical view of power output
x_outPower0 = np.zeros_like(x_outPower) # define baseline interval for plotting
ax4.plot(x_outPower, clip_aggregated, 'g', lw=2, label='Clipped Fuzzy Sets')
ax4.fill_between(x_outPower,x_outPower0, clip_aggregated,
                 facecolor='c', alpha=0.6) # fill centroid area with color

ax4.set_xlabel('outPower', fontsize=10)
ax4.set_ylabel('Membership', fontsize=10)
ax4.set_title(
    "Power output: {:.2f}% , err = {:.1f} , errRate = {:.1f}".format(
     powerLevel, err, errRate))

# plot vertical line at output value
ax4.plot([powerLevel, powerLevel],[0, 1], 'm--', lw=3, label='Power Level')

ax4.legend()
plt.show()
