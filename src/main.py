# #プロット関係のライブラリ
# from pyqtgraph.Qt import QtCore
# import pyqtgraph as pg
# import numpy as np
# import sys
# #音声関係のライブラリ
# import pyaudio
# class MainWindow():#(QtWidgets.QMainWindow):
#     def __init__(self):
#         # super(MainWindow, self).__init__()
#         # self.graphWidget = pg.PlotWidget()
#         # self.setCentralWidget(self.graphWidget)
        
#         #マイクインプット設定
#         self.CHUNK=1024         #1度に読み取る音声のデータ幅
#         self.RATE=16000             #サンプリング周波数
#         self.update_seconds=50      #更新時間[ms]
#         self.audio=pyaudio.PyAudio()
#         self.stream=self.audio.open(format=pyaudio.paInt16,
#                                     channels=1,
#                                     rate=self.RATE,
#                                     input=True,
#                                     frames_per_buffer=self.CHUNK)

#         #音声データの格納場所(プロットデータ)
#         self.data=np.zeros(self.CHUNK)
#         self.axis=np.fft.fftfreq(len(self.data), d=1.0/self.RATE)

#         #プロット初期設定
#         self.win=pg.GraphicsWindow()
#         self.win.setWindowTitle("SpectrumAnalyzer")
#         self.plt=self.win.addPlot() #プロットのビジュアル関係
#         self.plt.setYRange(0,100)    #y軸の制限

#         # self.graphWidget = PlotWidget()
#         # self.setCentralWidget(self.graphWidget)
#         # self.data_line =  self.graphWidget.plot()

#         #アップデート時間設定
#         self.timer=QtCore.QTimer()
#         self.timer.timeout.connect(self.update)
#         self.timer.start(self.update_seconds)    #10msごとにupdateを呼び出し

#     def update(self):
#         self.data=np.append(self.data,self.AudioInput())
#         if len(self.data)/1024 > 10:
#             self.data=self.data[1024:]
#         self.fft_data=self.FFT_AMP(self.data)
#         self.axis=np.fft.fftfreq(len(self.data), d=1.0/self.RATE)
#         self.plt.plot(x=self.axis, y=self.fft_data, clear=True, pen="y")  #symbol="o", symbolPen="y", symbolBrush="b")
#         # self.data_line.setData(x=self.axis, y=self.fft_data, clear=True, pen="y") 

#     def AudioInput(self):
#         ret=self.stream.read(self.CHUNK)    #音声の読み取り(バイナリ) CHUNKが大きいとここで時間かかる
#         #バイナリ → 数値(int16)に変換
#         #32768.0=2^16で割ってるのは正規化(絶対値を1以下にすること)
#         ret=np.frombuffer(ret, dtype="int16")/32768.0
#         return ret

#     def FFT_AMP(self, data):
#         data=np.hamming(len(data))*data
#         data=np.fft.fft(data)
#         data=np.abs(data)
#         return data

# if __name__=="__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     win=MainWindow()
#     # win.show()
#     # if (sys.flags.interactive!=1) or not hasattr(QtCore, 'PYQT_VERSION'):
#     #     QtGui.QApplication.instance().exec_()
#     sys.exit(app.exec())



"""
This example demonstrates many of the 2D plotting capabilities
in pyqtgraph. All of the plots may be panned/scaled by dragging with 
the left/right mouse buttons. Right click on any plot to show a context menu.
"""

import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, mkQApp, QtCore
import pyaudio

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        gr_wid = pg.GraphicsLayoutWidget(show=True)
        self.setCentralWidget(gr_wid)
        self.setWindowTitle('pyqtgraph example: Correlation matrix display')
        self.resize(600,500)
        self.show()
        
        #マイクインプット設定
        self.CHUNK=1024         #1度に読み取る音声のデータ幅
        self.RATE=16384             #サンプリング周波数
        self.update_seconds=50      #更新時間[ms]
        self.audio=pyaudio.PyAudio()
        self.stream=self.audio.open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=self.RATE,
                                    input=True,
                                    frames_per_buffer=self.CHUNK)

        #音声データの格納場所(プロットデータ)
        self.data=np.zeros(self.CHUNK)
        self.axis=np.fft.fftfreq(len(self.data), d=1.0/self.RATE)

        #プロット初期設定
        self.plt=gr_wid.addPlot() #プロットのビジュアル関係
        self.plt.setYRange(0,100)    #y軸の制限
        self.plt.setXRange(-1000,1000)    #y軸の制限

        # self.graphWidget = PlotWidget()
        # self.setCentralWidget(self.graphWidget)
        # self.data_line =  self.graphWidget.plot()

        #アップデート時間設定
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(self.update_seconds)    #10msごとにupdateを呼び出し

    def update(self):
        self.data=np.append(self.data,self.AudioInput())
        if len(self.data)/1024 > 10:
            self.data=self.data[1024:]
        self.fft_data=self.FFT_AMP(self.data)
        self.axis=np.fft.fftfreq(len(self.data), d=1.0/self.RATE)
        self.plt.plot(x=self.axis, y=self.fft_data, clear=True, pen="y")  #symbol="o", symbolPen="y", symbolBrush="b")
        # self.data_line.setData(x=self.axis, y=self.fft_data, clear=True, pen="y") 

    def AudioInput(self):
        ret=self.stream.read(self.CHUNK)    #音声の読み取り(バイナリ) CHUNKが大きいとここで時間かかる
        #バイナリ → 数値(int16)に変換
        #32768.0=2^16で割ってるのは正規化(絶対値を1以下にすること)
        ret=np.frombuffer(ret, dtype="int16")/32768.0
        return ret

    def FFT_AMP(self, data):
        data=np.hamming(len(data))*data
        data=np.fft.fft(data)
        data=np.abs(data)
        return data

# plot = win.addPlot(title="Updating plot")
# curve = plot.plot(pen='y')
# data = np.random.normal(size=(10,1000))
# ptr = 0
# def update():
#     global curve, data, ptr, plot
#     curve.setData(data[ptr%10])
#     if ptr == 0:
#         plot.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
#     ptr += 1
# timer = QtCore.QTimer()
# timer.timeout.connect(update)
# timer.start(50)

mkQApp("Correlation matrix display")
main_window = MainWindow()

## Start Qt event loop
if __name__ == '__main__':
    pg.exec()
