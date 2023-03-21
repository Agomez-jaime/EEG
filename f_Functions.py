
import numpy as np
import struct as st
import matplotlib.pyplot as plt
import scipy.io as sciio
import pandas as pd
from scipy import signal

def f_GetIIRFilter(p_FsHz, p_PassFreqHz, p_StopFreqsHz):
    s_AMaxPassDb = 0.5
    s_AMinstopDb = 120
    s_NyFreqHz = p_FsHz / 2
    p_PassFreqHz = np.array(p_PassFreqHz) / s_NyFreqHz
    p_StopFreqsHz = np.array(p_StopFreqsHz) / s_NyFreqHz
    s_N, v_Wn = signal.cheb2ord(p_PassFreqHz, p_StopFreqsHz, s_AMaxPassDb, s_AMinstopDb)
    print('f_GetIIRFilter - Filter order: ' + str(s_N))
    filt_FiltSOS = signal.cheby2(s_N, s_AMinstopDb, v_Wn, btype='bandpass', output='sos')

    return filt_FiltSOS

def f_GaborTFTransform(p_XIn, p_FsHz, p_F1Hz, p_F2Hz, p_FreqResHz, p_NumCycles):
    # Creamos un vector de tiempo en segundos
    v_TimeArray = np.arange(0, np.size(p_XIn))
    v_TimeArray = v_TimeArray - v_TimeArray[np.int(np.floor(np.size(v_TimeArray) / 2))]
    v_TimeArray = v_TimeArray / p_FsHz

    # Definimos un rango de frecuencias
    # las cuales usaremos para crear nuestros
    # patrones oscilatorios de prueba
    # En este caso generaremos patrones para
    # frecuencias entre 1 y 50 Hz con pasos
    # de 0.25 Hz
    v_FreqTestHz = np.arange(p_F1Hz, p_F2Hz + p_FreqResHz, p_FreqResHz)

    # Creamos una matriz que usaremos para
    # almacenar el resultado de las
    # convoluciones sucesivas. En esta matriz,
    # cada fila corresponde al resultado de
    # una convolución y cada columna a todos
    # los desplazamientos de tiempo.
    m_ConvMat = np.zeros([np.size(v_FreqTestHz), np.size(p_XIn)], dtype=complex)

    # Se obtiene la transformada de Fourier
    # de la señal p_XIn para usarla en cada iteración
    p_XInfft = np.fft.fft(p_XIn)

    # Ahora creamos un procedimiento iterativo
    # que recorra todas las frecuencias de prueba
    # definidas en el arreglo v_FreqTestHz
    for s_FreqIter in range(np.size(v_FreqTestHz)):
        # Generamos una señal sinusoidal de prueba
        # que oscile a la frecuencia de la iteración
        # s_FreqIter (v_FreqTestHz[s_FreqIter]) y que tenga
        # la misma longitud que la señal p_XIn.
        # En este caso usamos una exponencial compleja.
        xtest = np.exp(1j * 2.0 * np.pi * v_FreqTestHz[s_FreqIter] * v_TimeArray)

        # Creamos una ventana gaussina para
        # limitar nuestro patrón en el tiempo
        # Definimos la desviación estándar de
        # acuerdo al número de ciclos definidos
        # Dividimos entre 2 porque para un ventana
        # gaussiana, una desviación estándar
        # corresponde a la mitad del ancho de la ventana
        xtestwinstd = ((1.0 / v_FreqTestHz[s_FreqIter]) * p_NumCycles) / 2.0
        # Definimos nuestra ventana gaussiana
        xtestwin = np.exp(-0.5 * (v_TimeArray / xtestwinstd) ** 2.0)
        # Multiplicamos la señal patrón por
        # la ventana gaussiana
        xtest = xtest * xtestwin

        # Para cada sinusoidal de prueba obtenemos
        # el resultado de la convolución con la señal p_XIn
        # En este caso nos toca calcular la convolución
        # separadamente para la parte real e imaginaria
        # m_ConvMat[s_FreqIter, :] = np.convolve(p_XIn, np.real(xtest), 'same') + \
        #                        1j * np.convolve(p_XIn, np.imag(xtest), 'same')

        # Se obtine la transformada de Fourier del patrón
        fftxtest = np.fft.fft(xtest)
        # Se toma únicamente la parte real para evitar
        # corrimientos de fase
        fftxtest = abs(fftxtest)
        # Se obtine el resultado de la convolución realizando
        # la multiplicación de las transformadas de Fourier de
        # la señal p_XIn por la del patrón
        m_ConvMat[s_FreqIter, :] = np.fft.ifft(p_XInfft * fftxtest)

    v_TimeArray = v_TimeArray - v_TimeArray[0]
    return m_ConvMat, v_TimeArray, v_FreqTestHz