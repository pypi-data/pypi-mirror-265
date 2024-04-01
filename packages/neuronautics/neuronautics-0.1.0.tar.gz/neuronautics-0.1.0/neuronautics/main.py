from PyQt5 import QtWidgets
import sys
from datetime import datetime
from neuronautics import my_resources

from neuronautics.ui.neuronautics_ui import NeuronauticsUi

def main():
    app = QtWidgets.QApplication(sys.argv)

    window = NeuronauticsUi()

    app.exec_()

def extract_spikes(folder):
    green_text = "\033[32m"
    red_text = "\033[91m"
    reset_color = "\033[0m"

    import glob
    import os
    h5_files = glob.glob(os.path.join(folder, '*.h5'))
    file_errors = []
    for ix, file in enumerate(h5_files):
        if not os.path.exists(file.replace('h5', 'spike')):
            print(green_text+f'[{datetime.now()}] {ix+1}/{len(h5_files)} : {file}'+reset_color)
            from neuronautics.recordings.mcs_raw import McsRaw
            try:
                McsRaw(file).extract_all_spikes(5, 1000).to_csv(file.replace('h5', 'spike'), index=False)
            except:
                print(red_text+f'{ix+1}/{len(h5_files)} : {file}'+reset_color)
                file_errors.append(file)
    print('Failing spikes extraction: ')
    for file in file_errors:
        print(f'| {file}')


if __name__ == '__main__':
    main()
    #extract_spikes('/home/dani/OneDrive/MEA')