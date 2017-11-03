import os
    
import numpy as N   

if __name__ == '__main__':
    pass
    
    
    os.system ('cls')
    j=0
    while (j==0):
        s = N.zeros([6,6])
        c = N.zeros([6,6])
        d = N.zeros([3,6])
        propiedad =str (input('Que propiedad deseas?\ne (elasticidad), p (piezoelectricidad)\n'))
        
        sc = str (input ('Que sistema cristalino deseas?\n tc (Triclinico), m (Monoclinico), o (Ortorrombico), c (Cubico), te (Tetragonal), tg (Trigonal O Romboedrico), h (Hexagonal), iso (Isotropico)\n'))
        if propiedad == 'e':
            tipo = str (input ('Deseas s (compliance) o c (stiffness)?\n'))
            if sc == 'iso':
                if tipo == 's':
                    s[0,0] = s[1,1] = s[2,2] = float (input ('s11 = '))
                    s[0,1] = s[0,2] = s[1,2] = s[1,0] = s[2,0] = s[2,1] = float (input ('s12 = '))
                    s[3,3] = s[4,4] = s[5,5] = 2*(s[0,0] - s[0,1])
                    print (s)
                elif tipo == 'c':
                    c[0,0] = c[1,1] = c[2,2] = float (input ('c11 = '))
                    c[0,1] = c[0,2] = c[1,2] = c[1,0] = c[2,0] = c[2,1] = float (input ('c12 = '))
                    c[3,3] = c[4,4] = c[5,5] = (c[0,0] - c[0,1])/2
                    print (c)
                else:
                    print ('Tipo inexistente')
            elif sc == 'c':
                print ('Todos los grupos puntuales de este sistema cristalino tienen la misma matriz\n')
                if tipo == 's':
                    s[0,0] = s[1,1] = s[2,2] = float (input ('s11 = '))
                    s[0,1] = s[0,2] = s[1,2] = s[1,0] = s[2,0] = s[2,1] = float (input ('s12 = '))
                    s[3,3] = s[4,4] = s[5,5] = float (input ('s44 = '))
                    print (s)
                elif tipo == 'c':
                    c[0][0] = c[1][1] = c[2][2] = float (input ('c11 = '))
                    c[0][1] = c[0][2] = c[1][2] = c[1][0] = c[2][0] = c[2][1] = float (input ('c12 = '))
                    c[3][3] = c[4][4] = c[5][5] = float (input ('c44 = '))
                    print (c)
                else:
                    print ('Tipo inexistente')
            elif sc == 'h':
                print ('Todos los grupos puntuales de este sistema cristalino tienen la misma matriz\n')
                if tipo == 's':
                    s[0,0] = s[1,1] = float (input ('s11 = '))
                    s[0,1] = s[1,0] = float (input ('s12 = '))
                    s[0,2] = s[1,2] = s[2,0] = s[2,1] = float (input ('s13 = '))
                    s[2,2] = float (input ('s33 = '))
                    s[3,3] = s[4,4] = float (input ('s44 = '))
                    s[5,5] = 2*(s[0,0] - s[0,1])
                    print (s)
                elif tipo == 'c':
                    c[0,0] = c[1,1] = float (input ('c11 = '))
                    c[0,1] = c[1,0] = float (input ('c12 = '))
                    c[0,2] = c[1,2] = c[2,0] = c[2,1] = float (input ('c13 = '))
                    c[2,2] = float (input ('c33 = '))
                    c[3,3] = c[4,4] = float (input ('c44 = '))
                    c[5,5] = (c[0,0] - c[0,1])/2
                    print (c)
                else:
                    print ('Tipo inexistente')
            elif sc == 'o':
                print ('Todos los grupos puntuales de este sistema cristalino tienen la misma matriz\n')
                if tipo == 's':
                    s[0,0] = float (input ('s11 = '))
                    s[0,1] = s[1,0] = float (input ('s12 = '))
                    s[0,2] = s[2,0] = float (input ('s13 = '))
                    s[1,1] = float (input ('s22 = '))
                    s[1,2] = s[2,1] = float (input ('s23 = '))
                    s[2,2] = float (input ('s33 = '))
                    s[3,3] = float (input ('s44 = '))
                    s[4,4] = float (input ('s55 = '))
                    s[5,5] = float (input ('s66 = '))
                    print (s)
                elif tipo == 'c':
                    c[0,0] = float (input ('c11 = '))
                    c[0,1] = c[1,0] = float (input ('c12 = '))
                    c[0,2] = c[2,0] = float (input ('c13 = '))
                    c[1,1] = float (input ('c22 = '))
                    c[1,2] = c[2,1] = float (input ('c23 = '))
                    c[2,2] = float (input ('c33 = '))
                    c[3,3] = float (input ('c44 = '))
                    c[4,4] = float (input ('c55 = '))
                    c[5,5] = float (input ('c66 = '))
                    print (c)
                else:
                    print ('Tipo inexistente')
            elif sc == 'tc':
                print ('Todos los grupos puntuales de este sistema cristalino tienen la misma matriz\n')
                if tipo == 's':
                    s[0,0] = float (input ('s11 = '))
                    s[0,1] = s[1,0] = float (input ('s12 = '))
                    s[0,2] = s[2,0] = float (input ('s13 = '))
                    s[0,3] = s[3,0] = float (input ('s14 = '))
                    s[0,4] = s[4,0] = float (input ('s15 = '))
                    s[0,5] = s[5,0] = float (input ('s16 = '))
                    s[1,1] = float (input ('s22 = '))
                    s[1,2] = s[2,1] = float (input ('s23 = '))
                    s[1,3] = s[3,1] = float (input ('s24 = '))
                    s[1,4] = s[4,1] = float (input ('s25 = '))
                    s[1,5] = s[5,1] = float (input ('s26 = '))
                    s[2,2] = float (input ('s33 = '))
                    s[2,3] = s[3,2] = float (input ('s34 = '))
                    s[2,4] = s[4,2] = float (input ('s35 = '))
                    s[2,5] = s[5,2] = float (input ('s36 = '))
                    s[3,3] = float (input ('s44 = '))
                    s[3,4] = s[4,3] = float (input ('s45 = '))
                    s[3,5] = s[5,3] = float (input ('s46 = '))
                    s[4,4] = float (input ('s55 = '))
                    s[4,5] = s[5,4] = float (input ('s56 = '))
                    s[5,5] = float (input ('s66 = '))
                    print (s)
                elif tipo == 'c':
                    c[0,0] = float (input ('c11 = '))
                    c[0,1] = c[1,0] = float (input ('c12 = '))
                    c[0,2] = c[2,0] = float (input ('c13 = '))
                    c[0,3] = c[3,0] = float (input ('c14 = '))
                    c[0,4] = c[4,0] = float (input ('c15 = '))
                    c[0,5] = c[5,0] = float (input ('c16 = '))
                    c[1,1] = float (input ('c22 = '))
                    c[1,2] = c[2,1] = float (input ('c23 = '))
                    c[1,3] = c[3,1] = float (input ('c24 = '))
                    c[1,4] = c[4,1] = float (input ('c25 = '))
                    c[1,5] = c[5,1] = float (input ('c26 = '))
                    c[2,2] = float (input ('c33 = '))
                    c[2,3] = c[3,2] = float (input ('c34 = '))
                    c[2,4] = c[4,2] = float (input ('c35 = '))
                    c[2,5] = c[5,2] = float (input ('c36 = '))
                    c[3,3] = float (input ('c44 = '))
                    c[3,4] = c[4,3] = float (input ('c45 = '))
                    c[3,5] = c[5,3] = float (input ('c46 = '))
                    c[4,4] = float (input ('c55 = '))
                    c[4,5] = c[5,4] = float (input ('c56 = '))
                    c[5,5] = float (input ('c66 = '))
                    print (c)
                else:
                    print ('Tipo inexistente')
            elif sc == 'te':
                gp = str (input ('Cual grupo puntual? (4, -4, 4/m, 422, 4mm, -42m, 4/mmm)\n'))
                if gp in ('4mm', '-42m', '422', '4/mmm'):
                    if tipo == 's':
                        s[0,0] = s[1,1] = float (input ('s11 = '))
                        s[0,1] = s[1,0] = float (input ('s12 = '))
                        s[0,2] = s[1,2] = s[2,0] = s[2,1] = float (input ('s13 = '))
                        s[2,2] = float (input ('s33 = '))
                        s[3,3] = s[4,4] = float (input ('s44 = '))
                        s[5,5] = float (input ('s66 = '))
                        print (s)
                    elif tipo == 'c':
                        c[0,0] = c[1,1] = float (input ('c11 = '))
                        c[0,1] = c[1,0] = float (input ('c12 = '))
                        c[0,2] = c[1,2] = c[2,0] = c[2,1] = float (input ('c13 = '))
                        c[2,2] = float (input ('c33 = '))
                        c[3,3] = c[4,4] = float (input ('c44 = '))
                        c[5,5] = float (input ('c66 = '))
                        print (c)
                    else:
                        print ('Tipo inexistente')
                elif gp in ('4', '-4', '4/m'):
                    if tipo == 's':
                        s[0,0] = s[1,1] = float (input ('s11 = '))
                        s[0,1] = s[1,0] = float (input ('s12 = '))
                        s[0,2] = s[1,2] = s[2,0] = s[2,1] = float (input ('s13 = '))
                        s[0,5] = s[5,0] = float (input ('s16 = '))
                        s[1,5] = s[5,1] = -s[0,5]
                        s[2,2] = float (input ('s33 = '))
                        s[3,3] = s[4,4] = float (input ('s44 = '))
                        s[5,5] = float (input ('s66 = '))
                        print (s)
                    elif tipo == 'c':
                        c[0,0] = c[1,1] = float (input ('c11 = '))
                        c[0,1] = c[1,0] = float (input ('c12 = '))
                        c[0,2] = c[1,2] = c[2,0] = c[2,1] = float (input ('c13 = '))
                        c[0,5] = c[5,0] = float (input ('c16 = '))
                        c[1,5] = c[5,1] = -c[0,5]
                        c[2,2] = float (input ('c33 = '))
                        c[3,3] = c[4,4] = float (input ('c44 = '))
                        c[5,5] = float (input ('c66 = '))
                        print (c)
                    else:
                        print ('Tipo inexistente')
                else:
                    print ('Grupo puntual inexistente')
            elif sc == 'm':
                eje = str (input ('Donde se ubica el eje especial?(x2 o x3)\n'))
                print ('Todos los grupos puntuales de este sistema cristalino tienen la misma matriz\n')
                if eje == 'x2':
                    if tipo == 's':
                        s[0,0] = float (input ('s11 = '))
                        s[0,1] = s[1,0] = float (input ('s12 = '))
                        s[0,2] = s[2,0] = float (input ('s13 = '))
                        s[0,4] = s[4,0] = float (input ('s15 = '))
                        s[1,1] = float (input ('s22 = '))
                        s[1,2] = s[2,1] = float (input ('s23 = '))
                        s[1,4] = s[4,1] = float (input ('s25 = '))
                        s[2,2] = float (input ('s33 = '))
                        s[2,4] = s[4,2] = float (input ('s35 = '))
                        s[3,3] = float (input ('s44 = '))
                        s[3,5] = s[5,3] = float (input ('s46 = '))
                        s[4,4] = float (input ('s55 = '))
                        s[5,5] = float (input ('s66 = '))
                        print (s)
                    elif tipo == 'c':
                        c[0,0] = float (input ('c11 = '))
                        c[0,1] = c[1,0] = float (input ('c12 = '))
                        c[0,2] = c[2,0] = float (input ('c13 = '))
                        c[0,4] = c[4,0] = float (input ('c15 = '))
                        c[1,1] = float (input ('c22 = '))
                        c[1,2] = c[2,1] = float (input ('c23 = '))
                        c[1,4] = c[4,1] = float (input ('c25 = '))
                        c[2,2] = float (input ('c33 = '))
                        c[2,4] = c[4,2] = float (input ('c35 = '))
                        c[3,3] = float (input ('c44 = '))
                        c[3,5] = c[5,3] = float (input ('c46 = '))
                        c[4,4] = float (input ('c55 = '))
                        c[5,5] = float (input ('c66 = '))
                        print (c)
                    else:
                        print ('Tipo inexistente')
                elif eje == 'x3':
                    if tipo == 's':
                        s[0,0] = float (input ('s11 = '))
                        s[0,1] = s[1,0] = float (input ('s12 = '))
                        s[0,2] = s[2,0] = float (input ('s13 = '))
                        s[0,5] = s[5,0] = float (input ('s16 = '))
                        s[1,1] = float (input ('s22 = '))
                        s[1,2] = s[2,1] = float (input ('s23 = '))
                        s[1,5] = s[5,1] = float (input ('s26 = '))
                        s[2,2] = float (input ('s33 = '))
                        s[2,5] = s[5,2] = float (input ('s36 = '))
                        s[3,3] = float (input ('s44 = '))
                        s[3,4] = s[4,3] = float (input ('s45 = '))
                        s[4,4] = float (input ('s55 = '))
                        s[5,5] = float (input ('s66 = '))
                        print (s)
                    elif tipo == 'c':
                        c[0,0] = float (input ('c11 = '))
                        c[0,1] = c[1,0] = float (input ('c12 = '))
                        c[0,2] = c[2,0] = float (input ('c13 = '))
                        c[0,5] = c[5,0] = float (input ('c16 = '))
                        c[1,1] = float (input ('c22 = '))
                        c[1,2] = c[2,1] = float (input ('c23 = '))
                        c[1,5] = c[5,1] = float (input ('c26 = '))
                        c[2,2] = float (input ('c33 = '))
                        c[2,5] = c[5,2] = float (input ('c36 = '))
                        c[3,3] = float (input ('c44 = '))
                        c[3,4] = c[4,3] = float (input ('c45 = '))
                        c[4,4] = float (input ('c55 = '))
                        c[5,5] = float (input ('c66 = '))
                        print (c)
                    else:
                        print ('Tipo inexistente')
                else:
                    print ('Ubicacion del eje especial inexistente')
            elif sc == 'tg':
                gp = str (input ('Cual grupo puntual? (3, -3, 32, 3m, -3m)\n'))
                if gp in ('32', '-3m', '3m'):
                    if tipo == 's':
                        s[0,0] = s[1,1] = float (input ('s11 = '))
                        s[0,1] = s[1,0] = float (input ('s12 = '))
                        s[0,2] = s[1,2] = s[2,0] = s[2,1] = float (input ('s13 = '))
                        s[0,3] = s[3,0] = float (input ('s14 = '))
                        s[1,3] = s[3,1] = -s[0,3]
                        s[4,5] = s[5,4] = 2*s[0,3]
                        s[2,2] = float (input ('s33 = '))
                        s[3,3] = s[4,4] = float (input ('s44 = '))
                        s[5,5] = 2*(s[0,0] - s[0,1])
                        print (s)
                    elif tipo == 'c':
                        c[0,0] = c[1,1] = float (input ('c11 = '))
                        c[0,1] = c[1,0] = float (input ('c12 = '))
                        c[0,2] = c[1,2] = c[2,0] = c[2,1] = float (input ('c13 = '))
                        c[0,3] = c[3,0] = c[4,5] = c[5,4] = float (input ('c14 = '))
                        c[1,3] = c[3,1] = -c[0,3]
                        c[2,2] = float (input ('c33 = '))
                        c[3,3] = c[4,4] = float (input ('c44 = '))
                        c[5,5] = (c[0,0] - c[0,1])/2
                        print (c)
                    else:
                        print ('Tipo inexistente')
                elif gp in ('3', '-3'):
                    if tipo == 's':
                        s[0,0] = s[1,1] = float (input ('s11 = '))
                        s[0,1] = s[1,0] = float (input ('s12 = '))
                        s[0,2] = s[1,2] = s[2,0] = s[2,1] = float (input ('s13 = '))
                        s[0,3] = s[3,0] = float (input ('s14 = '))
                        s[1,3] = s[3,1] = -s[0,3]
                        s[4,5] = s[5,4] = 2*s[0,3]
                        s[1,4] = s[4,1] = float (input ('s25 = '))
                        s[0,4] = s[4,0] = -s[1,4]
                        s[3,5] = s[5,3] = 2*s[1,4]
                        s[2,2] = float (input ('s33 = '))
                        s[3,3] = s[4,4] = float (input ('s44 = '))
                        s[5,5] = 2*(s[0,0] - s[0,1])
                        print (s)
                    elif tipo == 'c':
                        c[0,0] = c[1,1] = float (input ('c11 = '))
                        c[0,1] = c[1,0] = float (input ('c12 = '))
                        c[0,2] = c[1,2] = c[2,0] = c[2,1] = float (input ('c13 = '))
                        c[0,3] = c[3,0] = c[4,5] = c[5,4] = float (input ('c14 = '))
                        c[1,3] = c[3,1] = -c[0,3]
                        c[1,4] = c[4,1] = c[3,5] = c[5,3] = float (input ('c25 = '))
                        c[0,4] = c[4,0] = -c[1,4]
                        c[2,2] = float (input ('c33 = '))
                        c[3,3] = c[4,4] = float (input ('c44 = '))
                        c[5,5] = (c[0,0] - c[0,1])/2
                        print (c)
                    else:
                        print ('Tipo inexistente')
                else:
                    print ('Grupo puntual inexistente')
            else:
                print ('Sistema Cristalino inexistente')
        elif propiedad == 'p':
            if sc == 'tc':
                gp = str (input ('Cual grupo puntual? (1, -1)\n'))
                if gp == 1:
                    d[0,0] = float (input ('d11 = '))
                    d[0,1] = float (input ('d12 = '))
                    d[0,2] = float (input ('d13 = '))
                    d[0,3] = float (input ('d14 = '))
                    d[0,4] = float (input ('d15 = '))
                    d[0,5] = float (input ('d16 = '))
                    d[1,0] = float (input ('d21 = '))
                    d[1,1] = float (input ('d22 = '))
                    d[1,2] = float (input ('d23 = '))
                    d[1,3] = float (input ('d24 = '))
                    d[1,4] = float (input ('d25 = '))
                    d[1,5] = float (input ('d26 = '))
                    d[2,0] = float (input ('d31 = '))
                    d[2,1] = float (input ('d32 = '))
                    d[2,2] = float (input ('d33 = '))
                    d[2,3] = float (input ('d34 = '))
                    d[2,4] = float (input ('d35 = '))
                    d[2,5] = float (input ('d36 = '))
                    print (d)
                elif gp == '-1':
                    print ('Este grupo puntual no tiene priezoelectricidad')
                else:
                    print ('Grupo puntual inexistente')
            elif sc == 'm':
                eje = str (input ('Donde se ubica el eje especial?(x2 o x3)\n'))
                gp = str (input ('Cual grupo puntual? (2, m, 2/m)\n'))
                if eje == 'x2':
                    if gp == '2':
                        d[0,3] = float (input ('d14 = '))
                        d[0,5] = float (input ('d16 = '))
                        d[1,0] = float (input ('d21 = '))
                        d[1,1] = float (input ('d22 = '))
                        d[1,2] = float (input ('d23 = '))
                        d[1,4] = float (input ('d25 = '))
                        d[2,3] = float (input ('d34 = '))
                        d[2,5] = float (input ('d36 = '))
                        print (d)
                    elif gp == 'm':
                        d[0,0] = float (input ('d11 = '))
                        d[0,1] = float (input ('d12 = '))
                        d[0,2] = float (input ('d13 = '))
                        d[0,4] = float (input ('d15 = '))
                        d[1,3] = float (input ('d24 = '))
                        d[1,5] = float (input ('d26 = '))
                        d[2,0] = float (input ('d31 = '))
                        d[2,1] = float (input ('d32 = '))
                        d[2,2] = float (input ('d33 = '))
                        d[2,4] = float (input ('d35 = '))
                        print (d)
                    elif gp == '2/m':
                        print ('Este grupo puntual no tiene priezoelectricidad')
                    else:
                        print ('Grupo puntual inexistente')
                elif eje == 'x3':
                    if gp == '2':
                        d[0,3] = float (input ('d14 = '))
                        d[0,4] = float (input ('d15 = '))
                        d[1,3] = float (input ('d24 = '))
                        d[1,4] = float (input ('d25 = '))
                        d[2,0] = float (input ('d31 = '))
                        d[2,1] = float (input ('d32 = '))
                        d[2,2] = float (input ('d33 = '))
                        d[2,5] = float (input ('d36 = '))
                        print (d)
                    elif gp == 'm':
                        d[0,0] = float (input ('d11 = '))
                        d[0,1] = float (input ('d12 = '))
                        d[0,2] = float (input ('d13 = '))
                        d[0,5] = float (input ('d16 = '))
                        d[1,0] = float (input ('d21 = '))
                        d[1,1] = float (input ('d22 = '))
                        d[1,2] = float (input ('d23 = '))
                        d[1,5] = float (input ('d26 = '))
                        d[2,3] = float (input ('d34 = '))
                        d[2,4] = float (input ('d35 = '))
                        print (d)
                    elif gp == '2/m':
                        print ('Este grupo puntual no tiene priezoelectricidad')
                    else:
                        print ('Grupo puntual inexistente')
                else:
                    print ('Ubicacion del eje especial inexistente')
            elif sc == 'o':
                gp = str (input ('Cual grupo puntual? (222, 2mm, mmm)\n'))
                if gp == '222':
                    d[0,3] = float (input ('d14 = '))
                    d[1,4] = float (input ('d25 = '))
                    d[2,5] = float (input ('d36 = '))
                    print (d)
                elif gp == '2mm':
                    d[0,4] = float (input ('d15 = '))
                    d[1,3] = float (input ('d24 = '))
                    d[2,0] = float (input ('d31 = '))
                    d[2,1] = float (input ('d32 = '))
                    d[2,2] = float (input ('d33 = '))
                    print (d)
                elif gp == 'mmm':
                    print ('Este grupo puntual no tiene priezoelectricidad')
                else:
                    print ('Grupo puntual inexistente')
            elif sc == 'te':
                gp = str (input ('Cual grupo puntual? (4, -4, 4/m, 422, 4mm, -42m, 4/mmm)\n'))
                if gp == '4':
                    d[0,3] = float (input ('d14 = '))
                    d[1,4] = -d[0,3]
                    d[0,4] = d[1,3] = float (input ('d15 = '))
                    d[2,0] = d[2,1] = float (input ('d31 = '))
                    d[2,2] = float (input ('d33 = '))
                    print (d)
                elif gp == '-4':
                    d[0,3] = d[1,4] = float (input ('d14 = '))
                    d[0,4] = float (input ('d15 = '))
                    d[1,3] = -d[0,4]
                    d[2,0] = float (input ('d31 = '))
                    d[2,1] = -d[2,0]
                    d[2,5] = float (input ('d36 = '))
                    print (d)
                elif gp in ('4/m', '4/mmm'):
                    print ('Este grupo puntual no tiene priezoelectricidad')
                elif gp == '422':
                    d[0,3] = float (input ('d14 = '))
                    d[1,4] = -d[0,3]
                    print (d)
                elif gp == '4mm':
                    d[0,4] = d[1,3] = float (input ('d15 = '))
                    d[2,0] = d[2,1] = float (input ('d31 = '))
                    d[2,2] = float (input ('d33 = '))
                    print (d)
                elif gp == '-42m':
                    d[0,3] = d[1,4] = float (input ('d14 = '))
                    d[2,5] = float (input ('d36 = '))
                    print (d)
                else:
                    print ('Grupo puntual inexistente')
            elif sc == 'c':
                gp = str (input ('Cual grupo puntual? (23, m3, 432, -43m, m3m)\n'))
                if gp in ('23', '-43m'):
                    d[0,3] = d[1,4] = d[2,5] = float (input ('d14 = '))
                    print (d)
                elif gp in ('m3', '432', 'm3m'):
                    print ('Este grupo puntual no tiene priezoelectricidad')
                else:
                    print ('Grupo puntual inexistente')
            elif sc == 'tg':
                gp = str (input ('Cual grupo puntual? (3, -3, 32, 3m, -3m)\n'))
                if gp == '3':
                    d[0,0] = float (input ('d11 = '))
                    d[0,1] = -d[0,0]
                    d[1,5] = -2*d[0,0]
                    d[0,3] = float (input ('d14 = '))
                    d[1,4] = -d[0,3]
                    d[0,4] = d[1][3] = float (input ('d15 = '))
                    d[1,1] = float (input ('d22 = '))
                    d[1,0] = -d[1,1]
                    d[0,5] = -2*d[1,1]
                    d[2,0] = d[2][1] = float (input ('d31 = '))
                    d[2,2] = float (input ('d33 = '))
                    print (d)
                elif gp == '32':
                    d[0,0] = float (input ('d11 = '))
                    d[0,1] = -d[0,0]
                    d[1,5] = -2*d[0,0]
                    d[0,3] = float (input ('d14 = '))
                    d[1,4] = -d[0,3]
                    print (d)
                elif gp == '3m':
                    eje = str (input ('Donde se ubica el eje especial?(x1 o x2)\n'))
                    if eje == 'x1':
                        d[0,3] = float (input ('d14 = '))
                        d[1,4] = -d[0,3]
                        d[0,4] = d[1,3] = float (input ('d15 = '))
                        d[1,1] = float (input ('d22 = '))
                        d[1,0] = -d[1,1]
                        d[0,5] = -2*d[1,1]
                        d[2,0] = d[2][1] = float (input ('d31 = '))
                        d[2,2] = float (input ('d33 = '))
                        print (d)
                    elif eje == 'x2':
                        d[0,0] = float (input ('d11 = '))
                        d[0,1] = -d[0,0]
                        d[1,5] = -2*d[0,0]
                        d[0,3] = float (input ('d14 = '))
                        d[1,4] = -d[0,3]
                        d[0,4] = d[1,3] = float (input ('d15 = '))
                        d[2,0] = d[2,1] = float (input ('d31 = '))
                        d[2,2] = float (input ('d33 = '))
                        print (d)
                    else:
                        print ('Ubicacion del eje especial inexistente')
                elif gp in ('-3', '-3m'):
                    print ('Este grupo puntual no tiene priezoelectricidad')
                else:
                    print ('Grupo puntual inexistente')
            elif sc == 'h':
                gp = str (input ('Cual grupo puntual? (6, -6, 6/m, 6mm, 622, -6m2, 6/mmm)\n'))
                if gp == '6':
                    d[0,3] = float (input ('d14 = '))
                    d[1,4] = -d[0,3]
                    d[0,4] = d[1,3] = float (input ('d15 = '))
                    d[2,0] = d[2,1] = float (input ('d31 = '))
                    d[2,2] = float (input ('d33 = '))
                    print (d)
                elif gp == '6mm':
                    d[0,4] = d[1,3] = float (input ('d15 = '))
                    d[2,0] = d[2,1] = float (input ('d31 = '))
                    d[2,2] = float (input ('d33 = '))
                    print (d)
                elif gp == '622':
                    d[0,3] = float (input ('d14 = '))
                    d[1,4] = -d[0,3]
                    print (d)
                elif gp == '-6':
                    d[0,0] = float (input ('d11 = '))
                    d[0,1] = -d[0,0]
                    d[1,5] = -2*d[0,0]
                    d[1,1] = float (input ('d22 = '))
                    d[1,0] = -d[1,1]
                    d[0,5] = -2*d[1,1]
                    print (d)
                elif gp == '-6m2':
                    eje = str (input ('Donde se ubica el eje especial?(x1 o x2)\n'))
                    if eje == 'x1':
                        d[1,1] = float (input ('d22 = '))
                        d[1,0] = -d[1,1]
                        d[0,5] = -2*d[1,1]
                        print (d)
                    elif eje == 'x2':
                        d[0,0] = float (input ('d11 = '))
                        d[0,1] = -d[0,0]
                        d[1,5] = -2*d[0,0]
                        print (d)
                    else:
                        print ('Ubicacion del eje especial inexistente')
                elif gp in ('6/m', '6/mmm'):
                    print ('Este grupo puntual no tiene priezoelectricidad')
                else:
                    print ('Grupo puntual inexistente')
            else:
                print ('Sistema Cristalino inexistente')
        else:
            print ('Propiedad inexistente')
        seguir = str (input ('Desea seguir?\n'))
        if seguir == 'no':
            j=1
            print ('Nos vemos luego')
        print ('\n')
