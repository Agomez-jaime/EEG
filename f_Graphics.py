
import matplotlib.pyplot as plt
def PlotFilteredEEG(m_Data,v_SigFilt,v_Time):
    fig, ax = plt.subplots(2, 1, sharex=True)
    fig.suptitle('EEG SIGNAL FILTERED')
    ax[0].plot(v_Time, m_Data, color = 'darkred',linewidth=1)
    ax[1].plot(v_Time, v_SigFilt, color = 'k', linewidth=1)

    ax[0].grid(linestyle = '--', linewidth = 0.5)
    ax[1].grid(linestyle = '--', linewidth = 0.5)

    ax[0].set_ylabel('Amplitud')
    ax[1].set_ylabel('Amplitud')

    ax[0].set_xlabel('')
    ax[1].set_xlabel('Tiempo (s)')