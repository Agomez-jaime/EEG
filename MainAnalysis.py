# -##################################
#             Imports
# -##################################

from f_Functions import *
from f_Graphics import *
import pandas as pd
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import scipy.signal as sig
import struct as st
import os
# -##################################
#       Lectura de datos
# -##################################
#TODO: Realice la lectura de datos, utilice los nombres proporcionados y la ruta del archivo debe ser generalizada.

str_FileName = 'C:/Users/andre/Documents/2023-1/Señales/Parcial 2/Esqueleto/Data/EEGEpilepsyData.mat'# Nombre y dirección del archivo

st_File = sio.loadmat(str_FileName) #dict_keys(['__header__', '__version__', '__globals__', 's_SRate', 'v_MicroData'])

m_Data = np.double(st_File['v_MicroData'])
s_FsHz = np.double(st_File['s_SRate'])

#TODO: Verifique cómo se almacenan sus variables y, si es necesario, modifíquelas.

# -##################################
#                Filtrado
# -##################################

#TODO: Aplique el filtro de respuesta infinita y grafique su señal resultante junto a la original.

v_Time =  m_Data  # Vector de tiempo de la señal
filt_FiltSOS = f_GetIIRFilter(s_FsHz, [Fq1, Fq2], [Fq1Rechazo, Fq2Rechazo]) #80-500
v_SigFilt = signal.sosfiltfilt(filt_FiltSOS, m_Data)
PlotFilteredEEG(m_Data,v_SigFilt,v_Time)

# -##################################
#                RMS
# -##################################

def window_rms(a, window_size=2): #tomado de https://stackoverflow.com/questions/8245687/numpy-root-mean-squared-rms-smoothing-of-a-signal
    return np.sqrt(sum([a[window_size-i-1:len(a)-i]**2 for i in range(window_size-1)])/window_size)
Sig_Proc = window_rms(v_SigFilt)

#TODO: Aplique un filtro RMS a su señal, esta no debe modificar la frecuencia de muestreo de la misma.

# -##################################
# Detección y selección de picos
# -##################################

v_PeaksInd = sig.find_peaks(Sig_Proc)

#TODO: Realice una detección de picos a su señal resultante de RMS y luego seleccione los picos correspondientes a eventos HFO

# threshold = # Umbral de selección de picos
# chanel_peaks, _ = # Función que detecta picos por encima de umbral

# selected_peaks = [] # Picos seleccionados

#TODO: Busque en los articulos que condicion se debe cumplir para seleccionar un pico, luego recorra cada uno de sus picos y dtermine si este debe ser seleccionado o es ruido.

# -##################################
#        Timepo frecuencia
# -##################################
#TODO: Realice un analisis de tiempo frecuencia solo a una ventana de Xs donde se haya detectado un HFO con una resolucion de 1Hz y 3 ciclos.

# -##################################
#           Visualización
# -##################################

#TODO: Grafique su señal original (Raw), Filtrada, Rms, FFT y Tiempo frecuencia solo en la ventana de tiempo escogida para los 3 HFOs y un artefacto.