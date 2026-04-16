'''
Prerequisites: 
  1) https://github.com/pierreaubert/spinorama repository is cloned and required module dependencies are installed. 
  2) PYTHONPATH is set to spinorama directories, e.g. if respository is cloned to home folder: 
     export PYTHONPATH=$HOME/spinorama/src:$HOME/spinorama/src/website:$HOME/spinorama

Example installation on Ubuntu 24.04:
  cd
  sudo apt-get update
  sudo apt install git
  git clone https://github.com/pierreaubert/spinorama
  sudo apt install imagemagick npm
  sudo apt install python3-pip
  sudo apt install python3.12-venv
  python3 -m venv $HOME/venv
  cd spinorama
  $HOME/venv/bin/pip install -r requirements.txt
  $HOME/venv/bin/pip install jupyterlab
  $HOME/venv/bin/pip install altair
  locale -a
  sudo locale-gen en_US.UTF-8
  cd
  git clone https://github.com/rwhomeaudio/ExportSpinoramaData

Test run:
  export PYTHONPATH=$HOME/spinorama/src:$HOME/spinorama/src/website:$HOME/spinorama
  cd ExportSpinoramaData
  $HOME/venv/bin/python ExportSpinoramaData.py -h
'''
 
import numpy as np
import pandas as pd
import plotly as plt
import os
import argparse
import math
import inspect

from spinorama.load_spl_hv_txt import parse_graphs_speaker_spl_hv_txt
from spinorama.load_klippel import parse_graphs_speaker_klippel
from spinorama.load_princeton import parse_graphs_speaker_princeton
from spinorama.load_gll_hv_txt import parse_graphs_speaker_gll_hv_txt
from spinorama.load import filter_graphs
from spinorama.constant_paths import MEAN_MIN, MEAN_MAX, DEFAULT_FREQ_RANGE
from datas import Measurement
from datas.metadata import speakers_info
from src.metaedit.api import get_speakers, get_speaker_metadata

# To find the measurmenrs directroy of the spinorama repository we retrive the spinorama model path which gets loaded via PYTHONPATH environment variable
m = inspect.getmodule(Measurement)
measurement_path = os.path.dirname(m.__file__) + '/measurements'

def export_measurement(speaker, version, absSPL):
    # Get measurment meta data
    measurement: Measurement = speakers_info[speaker]["measurements"][version]
    mformat = measurement['format']
    brand=speakers_info[speaker]["brand"]
    shape=speakers_info[speaker]["shape"]

    # Load measurement data
    if mformat in ("klippel", "princeton", "spl_hv_txt", "gll_hv_txt"):
        if mformat == "klippel":
            status, (h_spl, v_spl) = parse_graphs_speaker_klippel(
                measurement_path, brand, speaker, version, shape
            )
        elif mformat == "princeton":
            symmetry = measurement['symmetry']
            status, (h_spl, v_spl) = parse_graphs_speaker_princeton(
                measurement_path, brand, speaker, version, symmetry
            )
        elif mformat == "spl_hv_txt":
            status, (h_spl, v_spl) = parse_graphs_speaker_spl_hv_txt(
                measurement_path, brand, speaker, version
            )
        elif mformat == "gll_hv_txt":
            status, (h_spl, v_spl) = parse_graphs_speaker_gll_hv_txt(
                measurement_path, speaker, version
            )
    else:
        raise Exception(f"Unsupported measurement format '{mformat}'")

    # Get dataframe
    df = filter_graphs(speaker, h_spl, v_spl, MEAN_MIN, MEAN_MAX, mformat=mformat, mdistance=1)

    # Convert to absolute SPL
    if absSPL:
        df['CEA2034_unmelted'][['On Axis', 'Early Reflections', 'Listening Window', 'Sound Power']] = df['CEA2034_unmelted'][['On Axis', 'Early Reflections', 'Listening Window', 'Sound Power']] + df['sensitivity']
        df['Early Reflections_unmelted'][['Floor Bounce', 'Ceiling Bounce', 'Front Wall Bounce', 'Side Wall Bounce', 'Rear Wall Bounce', 'Total Early Reflection']] = df['Early Reflections_unmelted'][['Floor Bounce', 'Ceiling Bounce', 'Front Wall Bounce', 'Side Wall Bounce', 'Rear Wall Bounce', 'Total Early Reflection']] + df['sensitivity']
        df['Estimated In-Room Response_unmelted'][['Estimated In-Room Response']] = df['Estimated In-Room Response_unmelted'][['Estimated In-Room Response']] + df['sensitivity']
        diOffset = math.floor((df['sensitivity'] - 40)/10)*10
        df['CEA2034_unmelted'][['DI offset', 'Early Reflections DI', 'Sound Power DI']] = df['CEA2034_unmelted'][['DI offset', 'Early Reflections DI', 'Sound Power DI']] + diOffset

    # Export files
    path=f"export/{speaker}/{version}/CEA2034/"
    path = path.replace('|',' ').replace(':',' ')
    os.makedirs(path, exist_ok = True)
    filename = path + 'All.csv'
    df['CEA2034_unmelted'].to_csv(filename,index=False)
    for idx in df['CEA2034_unmelted'].columns:
        if idx != "Freq":
            filename = path + idx + '.txt'
            df['CEA2034_unmelted'][['Freq',idx]].to_csv(filename,index=False,sep=' ')

    path=f"export/{speaker}/{version}/Early Reflections/"
    path = path.replace('|',' ').replace(':',' ')
    os.makedirs(path, exist_ok = True)
    filename = path + 'All.csv'
    df['Early Reflections_unmelted'].to_csv(filename,index=False)
    for idx in df['Early Reflections_unmelted'].columns:
        if idx != "Freq":
            filename = path + idx + '.txt'
            df['Early Reflections_unmelted'][['Freq',idx]].to_csv(filename,index=False,sep=' ')

    path=f"export/{speaker}/{version}/"
    path = path.replace('|',' ').replace(':',' ')
    os.makedirs(path, exist_ok = True)
    filename = path + 'Estimated In-Room Response.txt'
    df['Estimated In-Room Response_unmelted'].to_csv(filename,index=False,sep=' ')

#main    
parser = argparse.ArgumentParser(prog='ExportSpinoramaData',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='''
ExportSpinoramaData exports spinorama data of a given speaker model and measurement version as text files in a sub directory "export".
The exported files can e.g. directly be imported in REW or spreadsheet programs.
''',
epilog='''
Example:

  ExportSpinoramaData.py --absSPL "KEF LS50 Meta" "asr"

  creates

    export/KEF LS50 Meta/asr/CEA2034/All.csv
    export/KEF LS50 Meta/asr/CEA2034/Early Reflections DI.txt
    export/KEF LS50 Meta/asr/CEA2034/On Axis.txt
    export/KEF LS50 Meta/asr/CEA2034/Early Reflections.txt
    export/KEF LS50 Meta/asr/CEA2034/Sound Power.txt
    export/KEF LS50 Meta/asr/CEA2034/DI offset.txt
    export/KEF LS50 Meta/asr/CEA2034/Listening Window.txt
    export/KEF LS50 Meta/asr/CEA2034/Sound Power DI.txt
    export/KEF LS50 Meta/asr/Estimated In-Room Response.txt
    export/KEF LS50 Meta/asr/Early Reflections/Front Wall Bounce.txt
    export/KEF LS50 Meta/asr/Early Reflections/All.csv
    export/KEF LS50 Meta/asr/Early Reflections/Total Early Reflection.txt
    export/KEF LS50 Meta/asr/Early Reflections/Floor Bounce.txt
    export/KEF LS50 Meta/asr/Early Reflections/Rear Wall Bounce.txt
    export/KEF LS50 Meta/asr/Early Reflections/Ceiling Bounce.txt
    export/KEF LS50 Meta/asr/Early Reflections/Side Wall Bounce.txt

  from the measurement of the KEF LS50 Meta provided by Audio Science Review with absolute SPL.
  
  Use

  ExportSpinoramaData.py --absSPL '*' '*'

  to export all availabile measurements.
'''
)
parser.add_argument('--absSPL', action='store_true', help='Export data with absolute SPL instead of 0dB normalized, default off')
parser.add_argument('speaker')
parser.add_argument('version')
args = parser.parse_args()
speaker = args.speaker
version = args.version
absSPL = args.absSPL

#measurement_path = './datas/measurements'

if speaker == '*' and version == '*':
    success = 0
    failure = 0
    for sp in get_speakers():
        for i, (key, value) in enumerate(get_speaker_metadata(sp)['measurements'].items()):
            print("Exporting ",sp, key)
            try:
                export_measurement(sp, key, absSPL)
                success = success + 1
            except Exception as e:
                print("Export of ",sp, key, " failed:", e)
                failure = failure +1
    print(success, "measurements successfull exported, ",failure," exports failed.")
else:
    export_measurement(speaker, version, absSPL)



