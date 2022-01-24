# NMLAB Final Project - Anomaly Detction by System Call
- Author: B07901040 凌鼎皓 and B07901174 蔡瑋展

# Feature Generation
## Files
- container_runner.sh: Shell script to open, delete the container and run Mysqlslap, sqlmap on container repetitively. In this script, five different kinds of operations from Mysqlslap is choosen and combined to generate 25 different suystem call trace.
- gettrace.sh: Shell script to detect creation of containers and trace system calls of containers via Sysdig. The data will be stored in a directory "trace_data".
- system_call_to_number.py: Change system calls to numbers
- feature_extraction.py: Read a file of numeralized system call trace and yield a feature vector of length 42



## Reqiurements
- Sysdig
- Docker
- inotify-tools

## How to Run
- Set to root
```
sudo -s
```

- Run gettrace.sh to track container
```
./gettrace.sh
```

- Open another terminal and run container_runner.sh to start repetitively create and delete container
```
./container_runner.sh
```

- Change system calls into numbers
```
python3 system_call_to_number.py
```

- Extract features: Modify code for normal or attacked set
```
python3 feature_extraction.py
```

# ADFA Dataset Feature Extraction and Analysis
## Files
- training_feature_extraction.py: Feature extraction
- attack_feature_extraction.py: Feature extraction
- analysis.py: Data analysis

## Setup
- Install libraries
```
pip3 install numpy
pip3 install pandas
pip3 install scipy
pip3 install sklearn
pip3 install matplotlib
pip3 install seaborn
```

## How to Run
- Feature extraction
```
python3 training_feature_extraction.py
python3 attack_feature_extractio.py
```

### Data Analysis by Colab
- Upload analysis.py to Google Colab
- Modify code to enable gdown or upload data by yourself
- Run

### Run on Local Machine
```
python3 analysis.py
```