import numpy as np
unit = 1000 #µm

br = [3.45, 11] #µm
hy = [3.45, 11] #µm

H = [2448, 1200] #pixels
V = [2050, 1200] #pixels

FOV = 100 #mm

for i in range(len(br)):
    pixSize = br[i] * hy[i] #µm^2
    countPix = H[i] * V[i]
    
    sensOpp = (unit) / 2 * pixSize                              #1
    horizontalPixSize = br[i] * (H[i] / (unit))                 #2
    verticalPixSize = hy[i] * (V[i] / (unit))                   #3
    PMAG = (horizontalPixSize * verticalPixSize) / (FOV)        #4
    objOpp_lpmm = sensOpp * PMAG                                #5
    objOpp_um = unit / (2 * objOpp_lpmm)                        #6

    print(f"Sensor {i+1}, piksel størrelser {br[i]} x {hy[i]} µm:")
    print(f"\t 1) Sensor oppløsning: {sensOpp:.2f} lp/mm")
    print(f"\t 2) Horizontal pixel size i objektplan: {horizontalPixSize:.2f} µm")
    print(f"\t 3) Vertical pixel size i objektplan: {verticalPixSize:.2f} µm")
    print(f"\t 4) PMAG: {PMAG:.2f}")
    print(f"\t 5) Objektoppløsning: {objOpp_lpmm:.2f} lp/mm")
    print(f"\t 6) Objektoppløsning: {objOpp_um:.3f} µm\n")

    
