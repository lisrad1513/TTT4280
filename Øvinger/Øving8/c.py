import numpy as np
unit = 1000 #µm

br = 11 #µm
hy = 11 #µm

activePixels = [1200, 512, 256, 128] #active pixels 1:1, 1:4, 1:16, 1:64

FOV = 100 #mm

for i in range(len(activePixels)):
    pixSize = br * hy #µm^2
    countPix = activePixels[i] * activePixels[i]
    
    sensOpp = (unit) / 2 * pixSize                              #1
    horizontalPixSize = br * (activePixels[i] / (unit))         #2
    verticalPixSize = hy * (activePixels[i] / (unit))           #3
    PMAG = (horizontalPixSize * verticalPixSize) / (FOV)        #4
    objOpp_lpmm = sensOpp * PMAG                                #5
    objOpp_um = unit / (2 * objOpp_lpmm)                        #6

    print(f"Sensor med piksel størrelser {activePixels[i]} x {activePixels[i]} µm:")
    # print(f"\t 1) Sensor oppløsning: {sensOpp:.2f} lp/mm")
    # print(f"\t 2) Horizontal pixel size i objektplan: {horizontalPixSize:.2f} µm")
    # print(f"\t 3) Vertical pixel size i objektplan: {verticalPixSize:.2f} µm")
    # print(f"\t 4) PMAG: {PMAG:.2f}")
    print(f"\t Objektoppløsning: {objOpp_lpmm:.2f} lp/mm")
    print(f"\t Objektoppløsning: {objOpp_um:.3f} µm\n")

    
