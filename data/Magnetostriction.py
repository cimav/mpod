# -*- coding: utf-8 -*-
# Magnetostriction
import numpy as np
from numpy import sin,cos,pi,abs # makes the code more readable
 
# Terfenol D 
#L100=90.0; L111=1640.0
# Galfenol 19 Altulasimha
L100=318*2/3; L111=-20*2/3
#L100=318*2/3; L111=0
# Galfenol 24 Altulasimha
# L100=310*2/3; L111=55*2/3
# Galfenol 29 Altulasimha
#L100=300*2/3; L111=55*2/3
#Prueba material hipotético isotrópico
#L111=1.0;L100=1.0   
phi, beta = np.mgrid[0:np.pi:180j,0:2*np.pi:360j]
x = sin(phi)*cos(beta)
y = sin(phi)*sin(beta)
z = cos(phi)
S0=L100
S1=3*(L111-L100)*((x**2)*(y**2) + (x**2)*(z**2) + (y**2)*(z**2))
S=S0+S1
x1 = S*sin(phi)*cos(beta)
y1 = S*sin(phi)*sin(beta)
z1 = S*cos(phi)
 
