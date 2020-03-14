#-*- coding: iso-8859-1 -*-
import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt,sin,cos,log,exp,asarray,loadtxt
from scipy.optimize import curve_fit
from scipy.odr import *
import Praktikum as prak

#Helium
data = loadtxt('../Messungen/Getrennt/helium1.txt')
h1 = np.mean(data,axis=0)
eh1 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/helium2.txt')
h2 = np.mean(data,axis=0)
eh2 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/helium3.txt')
h3 = np.mean(data,axis=0)
eh3 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/helium4.txt')
h4 = np.mean(data,axis=0)
eh4 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/helium5.txt')
h5 = np.mean(data,axis=0)
eh5 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/helium6.txt')
h6 = np.mean(data,axis=0)
eh6 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/helium7.txt')
h7 = np.mean(data,axis=0)
eh7 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/helium8.txt')
h8 = np.mean(data,axis=0)
eh8 = np.std(data,axis=0)

dataH9 = loadtxt('../Messungen/Getrennt/helium9.txt')
dataH10 = loadtxt('../Messungen/Getrennt/helium10.txt')

h9 = np.mean(dataH9[0:2,:],axis=0)
eh9 = np.std(dataH9[0:2,:],axis=0)
h10 = np.mean(dataH9[2:4,:],axis=0)
eh10 = np.std(dataH9[2:4,:],axis=0)
h11 = np.mean(dataH9[4:6,:],axis=0)
eh11 = np.std(dataH9[4:6,:],axis=0)
h12 = np.mean(dataH9[6:8,:],axis=0)
eh12 = np.std(dataH9[6:8,:],axis=0)
h13 = np.mean(dataH9[8:10,:],axis=0)
eh13 = np.std(dataH9[8:10,:],axis=0)
h14 = np.mean(dataH9[10:12,:],axis=0)
eh14 = np.std(dataH9[10:12,:],axis=0)
h15 = np.mean(dataH9[12:14,:],axis=0)
eh15 = np.std(dataH9[12:14,:],axis=0)
h16 = np.mean(dataH9[14:16,:],axis=0)
eh16 = np.std(dataH9[14:16,:],axis=0)
h17 = np.mean(dataH9[16:18,:],axis=0)
eh17 = np.std(dataH9[16:18,:],axis=0)
h18 = np.mean(dataH9[18:20,:],axis=0)
eh18 = np.std(dataH9[18:20,:],axis=0)
h19 = np.mean(dataH9[20:22,:],axis=0)
eh19 = np.std(dataH9[20:22,:],axis=0)
h20 = np.mean(dataH9[22:24,:],axis=0)
eh20 = np.std(dataH9[22:24,:],axis=0)
h21 = np.mean(dataH10[0:2,:],axis=0)
eh21 = np.std(dataH10[0:2,:],axis=0)
h22 = np.mean(dataH10[2:4,:],axis=0)
eh22 = np.std(dataH10[2:4,:],axis=0)
h23 = np.mean(dataH10[4:6,:],axis=0)
eh23 = np.std(dataH10[4:6,:],axis=0)
h24 = np.mean(dataH10[6:8,:],axis=0)
eh24 = np.std(dataH10[6:8,:],axis=0)
h25 = np.mean(dataH10[8:10,:],axis=0)
eh25 = np.std(dataH10[8:10,:],axis=0)
h26 = np.mean(dataH10[10:12,:],axis=0)
eh26 = np.std(dataH10[10:12,:],axis=0)


#Stickstoff
data = loadtxt('../Messungen/Getrennt/Nitrogen1.txt')
n1 = np.mean(data,axis=0)
en1 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen2.txt')
n2 = np.mean(data,axis=0)
en2 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen3.txt')
n3 = np.mean(data,axis=0)
en3 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen4.txt')
n4 = np.mean(data,axis=0)
en4 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen5.txt')
n5 = np.mean(data,axis=0)
en5 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen6.txt')
n6 = np.mean(data,axis=0)
en6 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen7.txt')
n7 = np.mean(data,axis=0)
en7 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen8.txt')
n8 = np.mean(data,axis=0)
en8 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen9.txt')
n9 = np.mean(data,axis=0)
en9 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen10.txt')
n10 = np.mean(data,axis=0)
en10 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen11.txt')
n11 = np.mean(data,axis=0)
en11 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen12.txt')
n12 = np.mean(data,axis=0)
en12 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen13.txt')
n13 = np.mean(data,axis=0)
en13 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen14.txt')
n14 = np.mean(data,axis=0)
en14 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen15.txt')
n15 = np.mean(data,axis=0)
en15 = np.std(data,axis=0)
data = loadtxt('../Messungen/Getrennt/Nitrogen16.txt')
n16 = np.mean(data,axis=0)
en16 = np.std(data,axis=0)

rPH =np.array([h1[0],h2[0],h3[0],h4[0],h5[0],h6[0],h7[0],h8[0],h9[0],h10[0],h11[0],h12[0],h13[0],h14[0],h15[0],h16[0],h17[0],h18[0],h19[0],h20[0],h21[0],h22[0],h23[0],h24[0],h25[0],h26[0]])
erPH =np.array([eh1[0],eh2[0],eh3[0],eh4[0],eh5[0],eh6[0],eh7[0],eh8[0],eh9[0],eh10[0],eh11[0],eh12[0],eh13[0],eh14[0],eh15[0],eh16[0],eh17[0],eh18[0],eh19[0],eh20[0],eh21[0],eh22[0],eh23[0],eh24[0],eh25[0],eh26[0]])
rPN =np.array([n1[0],n2[0],n3[0],n4[0],n5[0],n6[0],n7[0],n8[0],n9[0],n10[0],n11[0],n12[0],n13[0],n14[0],n15[0],n16[0]])
erPN =np.array([en1[0],en2[0],en3[0],en4[0],en5[0],en6[0],en7[0],en8[0],en9[0],en10[0],en11[0],en12[0],en13[0],en14[0],en15[0],en16[0]])

rKoH =np.array([h1[1],h2[1],h3[1],h4[1],h5[1],h6[1],h7[1],h8[1],h9[1],h11[1],h11[1],h12[1],h13[1],h14[1],h15[1],h16[1],h17[1],h18[1],h19[1],h21[1],h21[1],h22[1],h23[1],h24[1],h25[1],h26[1]])
erKoH =np.array([eh1[1],eh2[1],eh3[1],eh4[1],eh5[1],eh6[1],eh7[1],eh8[1],eh9[1],eh11[1],eh11[1],eh12[1],eh13[1],eh14[1],eh15[1],eh16[1],eh17[1],eh18[1],eh19[1],eh21[1],eh21[1],eh22[1],eh23[1],eh24[1],eh25[1],eh26[1]])
rKoN =np.array([n1[1],n2[1],n3[1],n4[1],n5[1],n6[1],n7[1],n8[1],n9[1],n11[1],n11[1],n12[1],n13[1],n14[1],n15[1],n16[1]])
erKoN =np.array([en1[1],en2[1],en3[1],en4[1],en5[1],en6[1],en7[1],en8[1],en9[1],en11[1],en11[1],en12[1],en13[1],en14[1],en15[1],en16[1]])

rKuH =np.array([h1[2],h2[2],h3[2],h4[2],h5[2],h6[2],h7[2],h8[2],h9[2],h12[2],h11[2],h12[2],h13[2],h14[2],h15[2],h16[2],h17[2],h18[2],h19[2],h22[2],h21[2],h22[2],h23[2],h24[2],h25[2],h26[2]])
erKuH =np.array([eh1[2],eh2[2],eh3[2],eh4[2],eh5[2],eh6[2],eh7[2],eh8[2],eh9[2],eh12[2],eh11[2],eh12[2],eh13[2],eh14[2],eh15[2],eh16[2],eh17[2],eh18[2],eh19[2],eh22[2],eh21[2],eh22[2],eh23[2],eh24[2],eh25[2],eh26[2]])
rKuN =np.array([n1[2],n2[2],n3[2],n4[2],n5[2],n6[2],n7[2],n8[2],n9[2],n12[2],n11[2],n12[2],n13[2],n14[2],n15[2],n16[2]])
erKuN =np.array([en1[2],en2[2],en3[2],en4[2],en5[2],en6[2],en7[2],en8[2],en9[2],en12[2],en11[2],en12[2],en13[2],en14[2],en15[2],en16[2]])

rTH =np.array([h1[3],h2[3],h3[3],h4[3],h5[3],h6[3],h7[3],h8[3],h9[3],h13[3],h11[3],h12[3],h13[3],h14[3],h15[3],h16[3],h17[3],h18[3],h19[3],h23[3],h21[3],h22[3],h23[3],h24[3],h25[3],h26[3]])
erTH =np.array([eh1[3],eh2[3],eh3[3],eh4[3],eh5[3],eh6[3],eh7[3],eh8[3],eh9[3],eh13[3],eh11[3],eh12[3],eh13[3],eh14[3],eh15[3],eh16[3],eh17[3],eh18[3],eh19[3],eh23[3],eh21[3],eh22[3],eh23[3],eh24[3],eh25[3],eh26[3]])
rTN =np.array([n1[3],n2[3],n3[3],n4[3],n5[3],n6[3],n7[3],n8[3],n9[3],n13[3],n11[3],n12[3],n13[3],n14[3],n15[3],n16[3]])
erTN =np.array([en1[3],en2[3],en3[3],en4[3],en5[3],en6[3],en7[3],en8[3],en9[3],en13[3],en11[3],en12[3],en13[3],en14[3],en15[3],en16[3]])

rSH =np.array([h1[4],h2[4],h3[4],h4[4],h5[4],h6[4],h7[4],h8[4],h9[4],h14[4],h11[4],h12[4],h13[4],h14[4],h15[4],h16[4],h17[4],h18[4],h19[4],h24[4],h21[4],h22[4],h23[4],h24[4],h25[4],h26[4]])
erSH =np.array([eh1[4],eh2[4],eh3[4],eh4[4],eh5[4],eh6[4],eh7[4],eh8[4],eh9[4],eh14[4],eh11[4],eh12[4],eh13[4],eh14[4],eh15[4],eh16[4],eh17[4],eh18[4],eh19[4],eh24[4],eh21[4],eh22[4],eh23[4],eh24[4],eh25[4],eh26[4]])
rSN =np.array([n1[4],n2[4],n3[4],n4[4],n5[4],n6[4],n7[4],n8[4],n9[4],n14[4],n11[4],n12[4],n13[4],n14[4],n15[4],n16[4]])
erSN =np.array([en1[4],en2[4],en3[4],en4[4],en5[4],en6[4],en7[4],en8[4],en9[4],en14[4],en11[4],en12[4],en13[4],en14[4],en15[4],en16[4]])


#Temperaturkalibrierung
roomPlatin = rPH[0]
eroomP = erPH[0]
nitrogenPlatin = rPN[15]
enitrogenP = erPN[15]
heliumPlatin = rPH[24]
eheliumP = erPH[24]

roomK = rKoH[0]
eroomK = erKoH[0]
nitrogenK = rKoN[15]
enitrogenK = erKoN[15]
heliumK = rKoH[24]
eheliumK = erKoH[24]

T = np.array([4.2,77.15,290.05])
eT = np.array([0.01,0.01,1.])

R_Platin = np.array([heliumPlatin,nitrogenPlatin,roomPlatin])
eR_Platin = np.array([eheliumP,enitrogenP,eroomP])
R_Kohle = np.array([heliumK,nitrogenK,roomK])
eR_Kohle = np.array([eheliumK,enitrogenK,eroomK])
#expfit
def exp_func(p, x):
    a,b,c= p
    return a+b*exp(-c/x)
# Create a model for fitting.
exp_model = Model(exp_func)
# Create a RealData object using our initiated data from above.
data = RealData(T,R_Kohle, sx=eT, sy=eR_Kohle)
# Set up ODR with the model and data.
odr = ODR(data, exp_model, beta0=[28.432,-1471.3,2369.24],maxit=2000)
# Run the regression.
out = odr.run()
# Generate fitted data.
x_fit = np.linspace(T[0], T[-1], 1000)
y_fit = exp_func(out.beta, x_fit)
#linear fitt
def lin_func(p, x):
    m,b = p
    return m*x+b
# Create a model for fitting.
lin_model = Model(lin_func)
# Create a RealData object using our initiated data from above.
data1 = RealData(T[1:],R_Platin[1:], sx=eT[1:], sy=eR_Platin[1:])
# Set up ODR with the model and data.
odr1 = ODR(data1, lin_model, beta0=[0.4,-8.],maxit=2000)
# Run the regression.
out1 = odr1.run()
# Generate fitted data.
x_fit1 = np.linspace(T[0], T[-1], 1000)
y_fit1 = lin_func(out1.beta, x_fit1)


# Generate a plot to show the data, errors, and fit.
fig, (ax,ax1) = plt.subplots(1,2,figsize=(10,5))
fig.subplots_adjust(wspace=0.3)
ax.errorbar(T,R_Kohle, xerr=eT, yerr=eR_Kohle, linestyle='None', marker='x',label='known temperature data')
ax.plot(x_fit, y_fit,label='fit')
ax.set_xlabel(r'$T$')
ax.set_ylabel(r'$R(T) = A+B \cdot e^{-C/T}$')
ax.set_title('coal calibration')
ax.legend(loc='center right',fontsize=9)
textstr = '\n'.join((
    r'$A=%.f \pm %.1f \cdot 10^{-26}$' % (out.beta[0],out.sd_beta[0]*10**26 ),
    r'$B=%.f \pm %.1f \cdot 10^{-26}$' % (out.beta[1],out.sd_beta[1]*10**26 ),
    r'$C=%.f \pm %.1f \cdot 10^{-26}$' % (out.beta[2],out.sd_beta[2]*10**26 )))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.3, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

ax1.errorbar(T[1:],R_Platin[1:], xerr=eT[1:], yerr=eR_Platin[1:], linestyle='None', marker='x',label='known temperature data')
ax1.plot(x_fit1, y_fit1,label='fit')
ax1.set_xlabel(r'$T$')
ax1.set_ylabel(r'$R(T) = m \cdot T + b$',labelpad=1)
ax1.set_title('platin calibration')
ax1.legend(loc='lower right',fontsize=9)
textstr1 = '\n'.join((
    r'$m=%.1f \pm %.1f \cdot 10^{-31}$' % (out1.beta[0],out1.sd_beta[0]*10**31 ),
    r'$b=%.1f \pm %.1f \cdot 10^{-31}$' % (out1.beta[1],out1.sd_beta[1]*10**31 )))
props1 = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax1.text(0.15, 0.95, textstr1, transform=ax1.transAxes, fontsize=14,
        verticalalignment='top', bbox=props1)
plt.close(fig)
fig.savefig('Plots/calibration.png')

nT = (rPN-out1.beta[1])/out1.beta[0]
nT_error = 0.

hT = out.beta[2]/(-log((rKoH-out.beta[0])/out.beta[1]))
ehT = np.ones(len(hT))*1
#hT_error=(out.beta[1]*out.beta[2])/((rKoH-out.beta[0])*(log(rKoH-out.beta[0]))**2)*erKoH
nT = (rPN-out1.beta[1])/out1.beta[0]
enT = np.ones(len(nT))*1


#R-T Plots

fig1, ax = plt.subplots()
x1,x2,y1,y2 = [],[],[],[]
ex1,ex2,ey1,ey2 = [],[],[],[]
for i in range(len(hT)):
    if(hT[i]<=77.15):
        x1.append(hT[i])
        y1.append(rKuH[i])
        x2.append(hT[i])
        y2.append(rTH[i])
        ex1.append(ehT[i])
        ey1.append(erKuH[i])
        ex2.append(ehT[i])
        ey2.append(erTH[i])
for i in range(len(nT)):
    if(nT[i]>=77.15):
        x1.append(nT[i])
        y1.append(rKuN[i])
        x2.append(nT[i])
        y2.append(rTN[i])
        ex1.append(enT[i])
        ey1.append(erKuN[i])
        ex2.append(enT[i])
        ey2.append(erTN[i])
ax.errorbar(x1,y1, xerr=ex1, yerr=ey1, linestyle='None', marker='x',label='tantalum')
ax.errorbar(x2,y2, xerr=ex2, yerr=ey2, linestyle='None', marker='x',label='copper')
ax.axvline(25., linestyle='--',color='red')
ax.axvline(110., linestyle='--',color='red')
ax.legend(loc='best',frameon=False,fontsize=9)
ax.set_title('R(T) curve')
ax.set_xlabel('temperature T [K]')
ax.set_ylabel(r'resistance R [$\Omega$]')
props = dict(boxstyle='square', facecolor='grey', alpha=0.5)

ax.text(0.03,0.95,'residual resistance',transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props,rotation=90)
ax.text(.15,0.95,'non-linear regime',transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props,rotation=90)
ax.text(0.4,0.95,'linear regime',transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props,rotation=90)
#ax.set_ylim(0.,0.3)
plt.close(fig1)
fig1.savefig('Plots/R_T_Kupfer_Tantal.png')


#ln(R_Tantal/Kupfer) über lnT
RRest_Kupfer = 0.188
RRest_Tantal = 0.091
fig1, ax = plt.subplots(2,2,figsize=(12,8))
x1,x2,y1,y2 = [],[],[],[]
ex1,ex2,ey1,ey2 = [],[],[],[]

lXTan,lYTan,lXKu,lYKu = [],[],[],[]
e_lXTan,e_lYTan,e_lXKu,e_lYKu = [],[],[],[]
for i in range(len(hT)):
    if(hT[i]<=77.15 and hT[i]>=25):
        x1.append(hT[i])
        y1.append(rKuH[i])
        x2.append(hT[i])
        y2.append(rTH[i])
        ex1.append(ehT[i])
        ey1.append(erKuH[i])
        ex2.append(ehT[i])
        ey2.append(erTH[i])
    if(hT[i]>=110.):
        lXTan.append(hT[i])
        lYTan.append(rTH[i])
        lXKu.append(hT[i])
        lYKu.append(rKuH[i])
        e_lXTan.append(ehT[i])
        e_lYTan.append(erTH[i])
        e_lXKu.append(ehT[i])
        e_lYKu.append(erKuH[i])

for i in range(len(nT)):
    if(nT[i]>=77.15 and nT[i]<=110.):
        if(nT[i]>=90. or nT[i]<=80.):
            x1.append(nT[i])
            y1.append(rKuN[i])
            x2.append(nT[i])
            y2.append(rTN[i])
            ex1.append(enT[i])
            ey1.append(erKuN[i])
            ex2.append(enT[i])
            ey2.append(erTN[i])
        if(hT[i]>=110.):
            lXTan.append(nT[i])
            lYTan.append(rTN[i])
            lXKu.append(nT[i])
            lYKu.append(rKuN[i])
            e_lXTan.append(enT[i])
            e_lYTan.append(erTN[i])
            e_lXKu.append(enT[i])
            e_lYKu.append(erKuN[i])
y1=asarray(y1)-RRest_Kupfer
y2 = asarray(y2)- RRest_Tantal
ex1,ey1,ex2,ey2 = asarray(ex1)/asarray(x1),asarray(ey1)/asarray(y1),asarray(ex2)/asarray(x2),asarray(ey2)/asarray(y2)
x1,y1,x2,y2 = log(x1),log(y1),log(x2),log(y2)

a,ea,b,eb,chiq,cov = prak.lineare_regression_xy(x1,y1,ex1,ey1)
a1,ea1,b1,eb1,chiq1,cov1 = prak.lineare_regression_xy(x2,y2,ex2,ey2)

plt.subplots_adjust(hspace=0.1,wspace=0.2)
ax[0,0].errorbar(x1,y1, xerr=ex1, yerr=ey1, linestyle='None', marker='x',label='tantalum',color='red')
ax[0,0].plot(x1,a*x1+b,color='green',label=r'a$\cdot$ln(T)+b')
ax[0,0].legend(loc='upper left',frameon=False,fontsize=9)
ax[0,0].set_title('ln(R)-ln(T) curve tantalum')
ax[0,0].set_xlim(3.,5.)
#ax[0,0].set_ylim(-3.,3.)
ax[0,0].set_ylabel(r'loharithmic resistance R [$\Omega$]')

ax[0,1].errorbar(x2,y2, xerr=ex2, yerr=ey2, linestyle='None', marker='x',label='copper',color='red')
ax[0,1].plot(x2,a1*x2+b1,color='green',label=r'a$\cdot$ln(T)+b')
ax[0,1].legend(loc='upper left',frameon=False,fontsize=9)
ax[0,1].set_title('ln(R)-ln(T) curve copper')
ax[0,1].set_xlim(3.,5.)
#ax[0,1].set_ylim(-3.,3.)

eyy1 = sqrt(ey1**2+(a*ex1)**2)
eyy2 = sqrt(ey2**2+(a1*ex2)**2)

ax[1,0].set_xlabel('logarithmic temperature ln(T)')
ax[1,0].set_ylabel('residues')
ax[1,0].axhline(0.,color='black')
ax[1,0].errorbar(x1,(y1-(a*x1+b)),yerr=eyy1, linestyle='.')
ax[1,0].set_xlim(3.,5.)
textstr1 = '\n'.join((
    r'$a=%.1f \pm %.1f$' % (a,ea),
    r'$b=%.1f \pm %.1f$' % (b,eb),
    r'$\chi_{ndof}=%.1f$' % (chiq/2)))
props1 = dict(boxstyle='round', facecolor='lightgrey', alpha=1.)
ax[1,0].text(0.75, 1., textstr1, transform=ax[1,0].transAxes, fontsize=14,
        verticalalignment='top', bbox=props1)

ax[1,1].set_xlabel('logarithmic temperature ln(T)')
ax[1,1].axhline(0.,color='black')
ax[1,1].errorbar(x2,(y2-(a1*x2+b1)),yerr=eyy2, linestyle='.')
ax[1,1].set_xlim(3.,5.)
textstr1 = '\n'.join((
    r'$a=%.1f \pm %.1f$' % (a1,ea1),
    r'$b=%.1f \pm %.1f$' % (b1,eb1),
    r'$\chi_{ndof}=%.1f$' % (chiq1/2)))
props2 = dict(boxstyle='round', facecolor='lightgrey', alpha=1.)
ax[1,1].text(2., 1., textstr1, transform=ax[1,0].transAxes, fontsize=14,
        verticalalignment='top', bbox=props1)

#ax.set_ylim(0.,0.3)
plt.close(fig1)
fig1.savefig('Plots/lnR_lnT_Kupfer_Tantal.png')


#ln(1/R) über ln(1/T) für Silizium
fig2, (ax1,ax2) = plt.subplots(2,1)
x1,y1 = [],[]
ex1,ey1 = [],[]
for i in range(len(hT)):
    if(hT[i]<=77.15):
        x1.append(hT[i])
        y1.append(rSH[i])
        ex1.append(ehT[i])
        ey1.append(erSH[i])
for i in range(len(nT)):
    if(nT[i]>=77.15):
        x1.append(nT[i])
        y1.append(rSN[i])
        ex1.append(enT[i])
        ey1.append(erSN[i])
ex1,ey1= asarray(ex1)/asarray(x1),asarray(ey1)/asarray(y1)
x1,y1 = log(asarray(x1)),log(1./asarray(y1))

ax1.plot(x1,y1,'g.',label=('data with jump to R=9.9*10^38 Ohm'))
ax1.set_title('silicon data')
ax2.set_xlabel('logarithmic T')
ax1.set_ylabel('logarithmic reciprocal R')
x1,y1 = [],[]
ex1,ey1 = [],[]
for i in range(len(hT)):
    if(hT[i]<=77.15 and rSH[i]<=9.9*10**30):
        x1.append(hT[i])
        y1.append(rSH[i])
        ex1.append(ehT[i])
        ey1.append(erSH[i])
for i in range(len(nT)):
    if(nT[i]>=77.15 and rSN[i]<=9.9*10**30):
        x1.append(nT[i])
        y1.append(rSN[i])
        ex1.append(enT[i])
        ey1.append(erSN[i])
ex1,ey1= asarray(ex1)/asarray(x1),asarray(ey1)/asarray(y1)
x1,y1 = log(asarray(x1)),log(1./asarray(y1))

ax2.plot(x1,y1,'g.',label=('data without jump to R=9.9*10^38 Ohm'))
ax2.set_ylabel('logarithmic reciprocal R')
ax1.legend(loc='best',fontsize=10)
ax2.legend(loc='best',fontsize=10)
plt.close(fig2)

fig2.savefig('Plots/Silizium_Jump_lnT.png')

#the linear coefficient of resistance of Cu and Ta, following R(T) = R0 (1+ α T) where T in
#°C and R in Ω have to be used and R0 = R(T = 0°C) .

#in Celsius
lXTan = asarray(lXTan)-273.15
lXKu = asarray(lXKu)-273.15
lYTan = asarray(lYTan)
lYKu = asarray(lYKu)
e_lXTan = asarray(e_lXTan)
e_lXKu = asarray(e_lXKu)
e_lYTan = asarray(e_lYTan)
e_lYKu = asarray(e_lYKu)

aTa,eaTa,bTa,ebTa,chiqTa,covTa = prak.lineare_regression_xy(lXTan,lYTan,e_lXTan,e_lYTan)
aKu,eaKu,bKu,ebKu,chiqKu,covKu = prak.lineare_regression_xy(lXKu,lYKu,e_lXKu,e_lYKu)

fig3,ax = plt.subplots(2,2,figsize=(12,8))
ax[0,0].errorbar(lXTan,lYTan,xerr=e_lXTan,yerr=e_lYTan,linestyle='None',marker='x',label='tantalum')
ax[0,0].plot(lXTan,aTa*lXTan+bTa,label=r'fit $R(T)=R_0 \cdot (1+\alpha \cdot T)$')
ax[0,0].legend(loc='best',fontsize=9)
ax[0,0].set_ylabel(r'resistance R [$\Omega$]')
ax[0,0].set_title('tantalum')

ax[0,1].errorbar(lXKu,lYKu,xerr=e_lXKu,yerr=e_lYKu,linestyle='None',marker='x',label='copper')
ax[0,1].plot(lXKu,aKu*lXKu+bKu,label=r'fit $R(T)=R_0 \cdot (1+\alpha \cdot T)$')
ax[0,1].legend(loc='best',fontsize=9)
ax[0,1].set_title('copper')

yTaErr = sqrt(e_lYTan**2+(aTa*e_lXTan)**2)
ax[1,0].axhline(0.)
ax[1,0].set_ylabel('resdiues')
ax[1,0].set_xlabel(r'temperature T [C]')
ax[1,0].errorbar(lXTan,lYTan-(aTa*lXTan+bTa),yerr=yTaErr,linestyle='None',marker='x')
textstr1 = '\n'.join((
    r'$a=%.2f \pm %.3f$' % (aTa,eaTa),
    r'$b=%.1f \pm %.1f$' % (bTa,ebTa),
    r'$\chi_{ndof}=%.1f$' % (chiqTa/2)))
props1 = dict(boxstyle='round,pad=1', facecolor='lightgrey', alpha=1.)
ax[1,0].text(0.78, 1., textstr1, transform=ax[1,0].transAxes, fontsize=10,
        verticalalignment='top', bbox=props1)

yKuErr = sqrt(e_lYKu**2+(aKu*e_lXKu)**2)
ax[1,1].axhline(0.)
ax[1,1].set_xlabel(r'temperature T [C]')
ax[1,1].errorbar(lXKu,lYKu-(aKu*lXKu+bKu),yerr=yKuErr,linestyle='None',marker='x')
textstr2 = '\n'.join((
    r'$a=%.2f \pm %.3f$' % (aKu,eaKu),
    r'$b=%.1f \pm %.1f$' % (bKu,ebKu),
    r'$\chi_{ndof}=%.1f$' % (chiqKu/2)))
props2 = dict(boxstyle='round,pad=1', facecolor='lightgrey', alpha=1.)
ax[1,1].text(0.78,1, textstr2, transform=ax[1,1].transAxes, fontsize=10,
        verticalalignment='top', bbox=props2)
plt.close(fig3)
fig3.savefig('Plots/lineare_regression_Tantal_Kupfer_Rnull.png')



#Sprungstelle
data = loadtxt('../Messungen/helium2.txt')
data1 = loadtxt('../Messungen/helium3.txt')

RCoal = []
R_Tantal = []

for i in range(len(data)):
    RCoal.append(data[i][1])
    R_Tantal.append(data[i][3])
for i in range(len(data1)):
    RCoal.append(data1[i][1])
    R_Tantal.append(data1[i][3])
RCoal = asarray(RCoal)
R_Tantal = asarray(R_Tantal)

T = out.beta[2]/(-log((RCoal-out.beta[0])/out.beta[1]))
eT = np.ones(len(T))

print T
print R_Tantal

figu = plt.figure(figsize=(8,8))
plt.ylim(-0.05,0.5)
plt.axvline(5.34304278, color='red', linewidth=0.5,linestyle='--', label='boundaries')
plt.axvline(20.24707648 , color='red', linewidth=0.5,linestyle='--')
plt.axvline(20.24707648-(20.24707648-5.34304278)/2. , color='green', linewidth=0.5,linestyle='--')

#plt.xlim(3.,8.)
plt.title(r'critical temperature $T_C$ of Ta')
plt.plot(T,R_Tantal,'b.',label='data Ta')
plt.xlabel('temperature T [K]')
plt.ylabel(r'resistance R [$\Omega$]')
plt.legend(loc='best')
props2 = dict(boxstyle='round,pad=1', facecolor='lightgrey', alpha=1.)
plt.text(6,0.4, r'T$_C$ = (%.1f $\pm$ %.1f) K' % (20.24707648-(20.24707648-5.34304278)/2.,(20.24707648-5.34304278)/2), fontsize=10,
        verticalalignment='top', bbox=props2)
figu.savefig('Plots/Sprungtemp.jpg')
