import pandas as pd, numpy as np, matplotlib.pyplot as plt

# put excel file in a working relative folder data, import convert to DataFrame
# or an absolute path such as 'C:/user/data/Mold_DOE.xlsx'
moldExp = pd.read_excel('data/Mold_DOE.xlsx', sheet_name="Mold_DOE", index_col = 0)



# you can bring data in using Dictionary format
moldDict = {'Runs ': range(1,9),
 'moldTemp': [38, 38, 38, 38, 23, 23, 23, 23],
 'coolTime': [28, 28, 18, 18, 28, 28, 18, 18],
 'holdPress': [650, 400, 650, 400, 650, 400, 650, 400],
 'Length': [40.85, 40.42, 40.72, 40.42, 40.95, 40.62, 40.75, 40.46]}

# bring moldDict to pandas DataFrame, you can use moldExp or moldDF for calculation
moldDF = pd.DataFrame(moldDict, index=range(1,9))

# average all high and low main factor levels
aveTemp = moldExp.groupby(['moldTemp'])[['Length']].mean()
aveTime = moldExp.groupby(['coolTime'])[['Length']].mean()
avePress = moldExp.groupby(['holdPress'])[['Length']].mean()

# computation of interaction between factors
aveTempCool = moldExp.groupby(['moldTemp','coolTime'])[['Length']].mean()
aveCoolPress = moldExp.groupby(['coolTime','holdPress'])[['Length']].mean()
aveTempPress = moldExp.groupby(['moldTemp','holdPress'])[['Length']].mean()

Temp_Press = (aveTempPress.Length[0] + aveTempPress.Length[3]
              -  aveTempPress.Length[1] - aveTempPress.Length[2]) / 2
Cool_Press = (aveCoolPress.Length[0] + aveCoolPress.Length[3]
              -  aveCoolPress.Length[1] - aveCoolPress.Length[2]) / 2
Temp_Cool = (aveTempCool.Length[0] + aveTempCool.Length[3]
             -  aveTempCool.Length[1] - aveTempCool.Length[2]) / 2

# plot the response graph of three main factors at two levels
plt.figure(2)
plt.plot(['moldTemp1', 'moldTemp2'], aveTemp.Length, 'rs-' ,
         ['coolTime1', 'coolTime2'], aveTime.Length, 'co-' ,
         ['holdPress1', 'holdPress2'], avePress.Length, 'bD-' ,
         lw=3, markersize=10, markerfacecolor='m')

# stacking Length values for text position then plot
aveResp = np.vstack([aveTemp, aveTime, avePress]).ravel().round(3)
for n in range(6) :
    i = n
    plt.text(i + 0.1 , aveResp[i] , str(aveResp[i]) , color='g')

# axis labels
plt.title('Average effects at Low and High Levels')
plt.xlabel('Factor Levels (Input Variables)')
plt.ylabel('Responses (mm)')

# another way of looking at response by magnitudes - delta Length of level averages
plt.figure(3)
X_factor = ['moldTemp', 'coolTime', 'holdPress','Temp*Press', 'Cool*Press', 'Temp*Cool']
Y_delta  = [aveTemp.iloc[1] - aveTemp.iloc[0],
            aveTime.iloc[1] - aveTime.iloc[0],
            avePress.iloc[1] - avePress.iloc[0],
            Temp_Press, Cool_Press, Temp_Cool]

# color the bar and draw a horizontal line at (0, 0) level
plt.bar(X_factor, Y_delta, color=['m','b','c','y', 'g', 'r'])
plt.plot([-0.4, 5.4], [0, 0], 'k-', lw = 2)

# setup text position for magnitude values
# yText = [-0.0925, 0.1225, 0.3375, 0.0275, 0.0425, -0.0575]
# convert Y_delta to float, because plt.text() does not like mixed data type

yText = np.round((np.array(Y_delta, dtype=float)), 4)
for n in range(6) :
    i = n
    y = yText[n]
    if y < 0 :  y -= 0.015
    else     :  y += 0.006
    plt.text(i - 0.25, y, str(yText[i]))

# axis labels
plt.ylabel('Response Magnitudes (mm)')
plt.xlabel('Factors (Inputs & Interactions)')
plt.title('Magnitude of effects with +- sign')

# setup contour plot
#  L = 0.00135*Pressure + 39.94
#  L = 0.01225*Time+ 40.367
#2*L = 0.00135*Pressure + 0.01225*coolTime + 80.307
#Pressure = (2*L - (0.01225*coolTime + 80.307)) / 0.00135

plt.figure(4)
Length = np.arange(40.5, 40.81, 0.05)
coolTime = np.arange(17, 30, 1)

# plot multiple lines
for n in Length:
    Pressure = (2*n - (0.01225*coolTime + 80.307)) / 0.00135
    plt.plot(coolTime, Pressure)

# process window limits
plt.plot([18, 18], [400, 650], 'b-' ,   #   vertical at x=18
         [28, 28], [400, 650], 'b-' ,
         [18, 28], [400, 400], 'b-' , # horizontal at y=400
         [18, 28], [650, 650], 'b-', lw=3)

# setup text position for contour Length values
pressY = np.arange(260,751,75)
for i in range(7):
    plt.text(28.5, pressY[i], str(round(Length[i], 2)))

# axis labels
plt.ylabel('Hold Pressure (Psi)')
plt.xlabel('Cooling Time (seconds)')
plt.title('Contour Plot (Pressure-Time-Length) vs. Process Window')

# show the graphs
plt.show()

# ============================
# ANOVA analysis process:
# ============================

# Total of all results:
T = sum(moldExp.Length)

# Correction Factor:
CF = T**2 / len(moldExp.Length)

# Total sum of squares:
SS_T = sum(moldExp.Length**2) - CF

# Factor sum of squares:
SS_Temp = (moldExp.groupby(['moldTemp'])[['Length']].sum()**2).sum()/4 - CF
SS_Time = (moldExp.groupby(['coolTime'])[['Length']].sum()**2).sum()/4 - CF
SS_Press = (moldExp.groupby(['holdPress'])[['Length']].sum()**2).sum()/4 - CF

# Interaction sum of squares:
SS_TempTime = (moldExp.groupby(['Temp*Time'])[['Length']].sum()**2).sum()/4 - CF
SS_TimePress = (moldExp.groupby(['Time*Press'])[['Length']].sum()**2).sum()/4 - CF
SS_TempPress = (moldExp.groupby(['Temp*Press'])[['Length']].sum()**2).sum()/4 - CF

# All other error sum of squares:
SS_e = SS_T - (SS_Temp + SS_Time + SS_Press
                + SS_TempTime + SS_TimePress + SS_TempPress)

# fT = (total number of trials * number of repetition) – 1 = (8 * 1) - 1
# f  = number of levels  – 1 =  2- 1 => Degrees of Freedom

fT = 8*1 - 1
fPress = 2-1
fTemp = 2-1
fTime = 2-1
fTempTime = fTemp * fTime
fTimePress = fTime * fPress
fTempPress = fTemp * fPress
fe = fT - (fTemp + fTime + fPress 
           + fTempTime + fTimePress + fTempPress)

# Mean square (variance):
MS_Temp = SS_Temp / fTemp
MS_Time = SS_Time / fTime
MS_Press = SS_Press / fPress
MS_TempTime = SS_TempTime / fTempTime
MS_TimePress = SS_TimePress / fTimePress
MS_TempPress = SS_TempPress / fTempPress

MS_e = SS_e / fe

# Factor F ratios (Variance Factor/ error variance)
F_Temp = MS_Temp / MS_e
F_Time = MS_Time / MS_e
F_Press = MS_Press / MS_e
F_TempTime = MS_TempTime / MS_e
F_TimePress = MS_TimePress / MS_e
F_TempPress = MS_TempPress / MS_e
F_e = MS_e / MS_e

# Pure sum of squares - PS :
PS_Temp = SS_Temp - (MS_e * fTemp)
PS_Time = SS_Time - (MS_e * fTime)
PS_Press = SS_Press - (MS_e * fPress)
PS_TempTime = SS_TempTime - (MS_e * fTempTime)
PS_TimePress = SS_TimePress - (MS_e * fTimePress)
PS_TempPress = SS_TempPress - (MS_e * fTempPress)
PS_e = SS_e + (fTemp + fTime + fPress + fTempTime + fTimePress + fTempPress) * MS_e

# Percentage contribution/Influence:
PI_Temp = PS_Temp / SS_T * 100
PI_Time = PS_Time / SS_T * 100
PI_Press = PS_Press / SS_T * 100
PI_TempTime = PS_TempTime / SS_T * 100
PI_TimePress = PS_TimePress / SS_T * 100
PI_TempPress = PS_TempPress / SS_T * 100
PI_e = PS_e / SS_T * 100

# Construct ANOVA table with pandas DataFrame
Source = ['moldTemp', 'coolTime', 'holdPress', 'Temp*Time', 'Time*Press', 'Temp*Press', 'Error', 'Total']
df = [fTemp, fTime, fPress, fTempTime, fTimePress, fTempPress, fe, fT]
SS = np.array([SS_Temp, SS_Time, SS_Press, SS_TempTime, SS_TimePress, SS_TempPress, SS_e, SS_T], dtype=float).round(4)
MS = np.array([MS_Temp, MS_Time, MS_Press, MS_TempTime, MS_TimePress, MS_TempPress, MS_e, 'nan'], dtype=float).round(4)
F  = np.array([F_Temp, F_Time, F_Press, F_TempTime, F_TimePress, F_TempPress, F_e, 'nan'], dtype=float).round(2)
PS = np.array([PS_Temp, PS_Time, PS_Press, PS_TempTime, PS_TimePress, PS_TempPress, PS_e, 'nan'], dtype=float).round(4)
totalPI = sum(np.array([PI_Temp, PI_Time, PI_Press, PI_TempTime, PI_TimePress, PI_TempPress, PI_e], dtype=float).round(2))
PI = np.array([PI_Temp, PI_Time, PI_Press, PI_TempTime, PI_TimePress, PI_TempPress, PI_e, totalPI.item()], dtype=float).round(2)

anovaDict = {'Source': Source,
             'df': df,
             'SS': SS,
             'MS': MS,
             'F' : F,
             'PS': PS,
             'PI': PI}

anovaMold = pd.DataFrame(anovaDict)

print(anovaMold)

'''
# -----------------------------------------

# Some other commands you may use. You can play with moldDF DataFrame
# moldDF.sort_values(['coolTime','holdPress','Length'])[['moldTemp','coolTime','holdPress','Length']]
# To rename columns -> moldDF.rename(columns={'Runs ': '# Order'}, inplace=True)
# To rename index -> moldDF.index.name = '# Trials' -> you can use this index instead of a column

interaction = moldDF.groupby(['holdPress','coolTime'])[['Length']].mean()
interaction.loc[400].sem()*2
plt.legend()

#--------------------------------
'''
