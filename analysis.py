# -*- coding: utf-8 -*-
"""analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z5dG5S7d0yDBJ5IQKPkKzACxppJ0-EsO

Set library and environment
"""

import numpy as np
import pandas as pd  
# import gdown # Enable this part to run on Colab
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(rc={'figure.figsize':(11.7,8.27)})
palette = sns.color_palette("bright", 2)

"""Import data"""
# # Enable this part to run on Colab ===================================================
# !gdown --id '1yqJGddilLG1t-LW2QGOc9yVyyGz57R5Q' # Attacked
# !gdown --id '1ZkG956KsDTOxUxMrDbTpVbBmAzXbOIiW' # Normal
# # ====================================================================================
# # Upload files yourself in case link does not work

attacked_path = 'attacked_feature_set.txt' 
normal_path = 'normal_feature_set.txt' 

attacked = open(attacked_path, 'r')
attacked_data = []
label = []
for line in attacked:
    attacked_data.append(line.split())
    label.append(1)
for i in range(len(attacked_data)):
    for j in range(len(attacked_data[i])):
        attacked_data[i][j] = float(attacked_data[i][j])
attacked.close()

normal = open(normal_path, 'r')
normal_data = []
for line in normal:
    normal_data.append(line.split())
    label.append(0)
for i in range(len(normal_data)):
    for j in range(len(normal_data[i])):
        normal_data[i][j] = float(normal_data[i][j])
normal.close()
data = attacked_data + normal_data
x = np.array(data)
y = np.array(label)
print(np.shape(x))
print(np.shape(y))


# # ======================= ADFA :Enable this part to run on Colab =============================
# !gdown --id '1xmxwjDm_7xyZfxoJRX2O1GcNdGKtJqf6' # Attacked
# !gdown --id '15JKsiVcPrTpn9b5hPekQH4-5ipuDZ8LE' # Training
# # ============================================================================================
# # Upload files yourself in case link does not work


ADFA_attacked = 'Attack_feature_set.txt'
ADFA_normal = 'Training_feature_set.txt'

attacked = open(ADFA_attacked, 'r')
attacked_data = []
label = []
for line in attacked:
    attacked_data.append(line.split())
    label.append(1)
for i in range(len(attacked_data)):
    for j in range(len(attacked_data[i])):
        attacked_data[i][j] = float(attacked_data[i][j])
attacked.close()

normal = open(ADFA_normal, 'r')
normal_data = []
for line in normal:
    normal_data.append(line.split())
    label.append(0)
for i in range(len(normal_data)):
    for j in range(len(normal_data[i])):
        normal_data[i][j] = float(normal_data[i][j])
normal.close()
ADFA_data = attacked_data + normal_data
ADFA_x = []
ADFA_y = []

# Remove uniform distribution
deletion = []
for i in range(len(ADFA_data)):
    for j in range(len(ADFA_data[i])):
        if np.isnan(ADFA_data[i][j]):
            deletion.append(i)
for i in range(len(ADFA_data)):
    if i not in deletion:
        ADFA_x.append(ADFA_data[i])
        ADFA_y.append(label[i])
    else:
        print('ADFA_data', i, 'deleted')
ADFA_x = np.array(ADFA_x)
ADFA_y = np.array(ADFA_y)
print(np.shape(ADFA_x))
print(np.shape(ADFA_y))

"""t-SNE"""

tsne = TSNE(n_components=2, perplexity=10.0, verbose=1, random_state=1000)
z = tsne.fit_transform(x) 
df = pd.DataFrame()
df["y"] = y
df["comp-1"] = z[:,0]
df["comp-2"] = z[:,1]

sns.scatterplot(x="comp-1", y="comp-2", hue=df.y.tolist(),
                palette=sns.color_palette("hls", 2),
                data=df).set(title="Iris data T-SNE projection")

tsne = TSNE(n_components=2, perplexity=30.0, verbose=1, random_state=1000)
z = tsne.fit_transform(ADFA_x) 
df = pd.DataFrame()
df["y"] = ADFA_y
df["comp-1"] = z[:,0]
df["comp-2"] = z[:,1]

sns.scatterplot(x="comp-1", y="comp-2", hue=df.y.tolist(),
                palette=sns.color_palette("hls", 2),
                data=df).set(title="Iris data T-SNE projection")

"""PCA"""

y = np.reshape(y, (50,1))
final_data = np.concatenate([x,y],axis=1)
gen_dataset = pd.DataFrame(final_data)
features = []
for i in range(42):
    features.append('f' + str(i))
features_labels = np.array(features)
features_labels = np.append(features_labels, 'label')
gen_dataset.columns = features_labels
gen_dataset['label'].replace(0, 'normal',inplace=True)
gen_dataset['label'].replace(1, 'attacked',inplace=True)

x = gen_dataset.loc[:, features].values
x = StandardScaler().fit_transform(x)
feat_cols = ['feature'+str(i) for i in range(x.shape[1])]
x = pd.DataFrame(x,columns=feat_cols)


pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])

plt.figure()
plt.figure(figsize=(10,10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=14)
plt.xlabel('Principal Component - 1',fontsize=20)
plt.ylabel('Principal Component - 2',fontsize=20)
plt.title("Principal Component Analysis of Generated Dataset",fontsize=20)
targets = ['normal', 'attacked']
colors = ['r', 'b']
for target, color in zip(targets,colors):
    indicesToKeep = gen_dataset['label'] == target
    plt.scatter(principalDf.loc[indicesToKeep, 'principal component 1']
               , principalDf.loc[indicesToKeep, 'principal component 2'], c = color, s = 50)

plt.legend(targets,prop={'size': 15})

ADFA_y = np.reshape(ADFA_y, (1576,1))
final_data = np.concatenate([ADFA_x,ADFA_y],axis=1)
ADFA_dataset = pd.DataFrame(final_data)
features = []
for i in range(42):
    features.append('f' + str(i))
features_labels = np.array(features)
features_labels = np.append(features_labels, 'label')
ADFA_dataset.columns = features_labels
ADFA_dataset['label'].replace(0, 'normal',inplace=True)
ADFA_dataset['label'].replace(1, 'attacked',inplace=True)

x = ADFA_dataset.loc[:, features].values
x = StandardScaler().fit_transform(x)
feat_cols = ['feature'+str(i) for i in range(x.shape[1])]
x = pd.DataFrame(x,columns=feat_cols)


pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])

plt.figure()
plt.figure(figsize=(10,10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=14)
plt.xlabel('Principal Component - 1',fontsize=20)
plt.ylabel('Principal Component - 2',fontsize=20)
plt.title("Principal Component Analysis of ADFA Dataset",fontsize=20)
targets = ['normal', 'attacked']
colors = ['r', 'b']
for target, color in zip(targets,colors):
    indicesToKeep = ADFA_dataset['label'] == target
    plt.scatter(principalDf.loc[indicesToKeep, 'principal component 1']
               , principalDf.loc[indicesToKeep, 'principal component 2'], c = color, s = 50)

plt.legend(targets,prop={'size': 15})