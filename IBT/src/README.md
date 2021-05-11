  client.py
  ---------
  TCP client is necessary to connect to TCP server and for communication with E4 wristband.
  
  Example:
  ```
  >>> import sys
  >>> import socket
  >>> import re
  >>> import threading as th
  >>> import time
  >>> from pathlib import Path

  >>> path = os.path.dirname(os.getcwd())

  >>> client = Client(path=path)
  >>> client.connect()
  ```
  ------------------------------------------------------------------------------------------------

  data_convertor.py
  -----------------
  Data from E4 wristband processing. Split raw data into 'csv' files by the type of signal.
  
  Example:
  ```
  >>> import os
  >>> import pandas as pd
  >>> import numpy as np
  >>> from pathlib import Path

  >>> from file_processing import load_files

  >>> path = os.path.dirname(os.getcwd())
  >>> path = '{}/data'.format(path)

  >>> files = load_files(path)
  >>> raw_data_to_csv(files, path)
  ```
  ------------------------------------------------------------------------------------------------

  data_time_processing.py
  -----------------------
  Daytime statistic (morning, noon, afternoon, evening, night) of sessions.
  
  Example: 
  ```
  python .\data_time_processing.py
  ```
  ------------------------------------------------------------------------------------------------

  file_processing.py
  ------------------
  Useful functions for loading data.
  
  ------------------------------------------------------------------------------------------------

  make_stat.py
  ------------
  Functions for creating statistics and plotting interesting information about the dataset.
  
  Example:
  ```
  >>> import os
  >>> import pandas as pd
  >>> import matplotlib.pyplot as plt
  >>> from matplotlib.ticker import MaxNLocator
  >>> import seaborn as sns
  >>> from file_processing import get_data
  >>> from scipy.stats import f_oneway

  >>> plt.rcParams['figure.figsize'] = [10, 6]
  >>> plt.rcParams['font.size']= 18

  >>> path = os.path.dirname(os.getcwd())
  >>> path = '{}/data'.format(path)

  >>> emotion_gender_df = pd.read_csv('{}/Emotion_Gender.csv'.format(path))
  >>> hr_eda_stat(path)
  >>> plot_stat(path, emotion_gender_df)
  >>> plot_heatmap_emotion_choice(path)
  >>> get_mean_hrv_indices(path)
  ```
  ------------------------------------------------------------------------------------------------

  processing_nk.py
  ----------------
  Main script for data processing and signal features extraction.

  Example:
  ```
  >>> from file_processing import get_all_data
  >>> from pathlib import Path, PurePath
  >>> import os
  >>> import numpy as np
  >>> import pandas as pd
  >>> import matplotlib.pyplot as plt
  >>> import seaborn as sns
  >>> import neurokit2 as nk
  >>> import make_stat as ms

  >>> path = os.path.dirname(os.getcwd())
  >>> path = '{}/data'.format(path)

  >>> processor = Processor(path=path)
  >>> processor.process_all()
  ```
  ------------------------------------------------------------------------------------------------

  session.py
  ----------
  Main script for data receiving and measuring physiological data during session.
  
  Example:
  ```
  >>> import argparse
  >>> import os

  >>> path = os.path.dirname(os.getcwd())
  >>> session(path=path, keep_raw_data=False, fig=False)
  ```

  ------------------------------------------------------------------------------------------------

  visualize.py
  ------------
  Plot all signals from E4 wristband received during sessions.
 
  Example:
  ```
  >>> import matplotlib.pyplot as plt
  >>> from pathlib import Path
  >>> import numpy as np

  >>> from file_processing import get_all_data

  >>> path = os.path.dirname(os.getcwd())
  >>> path = '{}/plots'.format(path)
  >>> p = Path(path)
  >>> p.mkdir(exist_ok=True)

  >>> plot_data()
  ```
  ------------------------------------------------------------------------------------------------
