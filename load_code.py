# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 23:39:51 2020

@author: ASUS
"""


import os
import librosa
import numpy as np
import pandas as pd 
            
def extract_features(files):
    try:
        file_name =files.file
        X, sample_rate = librosa.load(file_name, res_type='kaiser_fast')  
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
        stft = np.abs(librosa.stft(X))
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
        mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X),
        sr=sample_rate).T,axis=0)
        label = files.label
        return mfccs, chroma, mel, contrast, tonnetz, label 
    except:
        errors.append(file_name)
        return []               

dirname = os.path.dirname(__file__) + '\Data_Uploads'
filelist = os.listdir(dirname)
errors = []

file_names = []
df_ = pd.DataFrame()
class_number = []
subject_number = []
label = []
birth = [] 
k = 0  
for i in range(2,len(filelist)+1):
    name = dirname + "\\" + filelist[i-1]
    each_class_dir = name + "\\" + 'Voices'
    d = pd.read_csv(str(name + "\\" + os.listdir(name)[0]),encoding = "ISO-8859-1")
    each_class_list = os.listdir(each_class_dir)
    each_class_list = list(map(int, each_class_list))
    each_class_list.sort()
    Y = d['Birth']
    subjects_Birth = Y.tolist()
    Y = d['Gender']
    gender_map = {'F':1, 'M':0}
    subjects_gender = Y.map(gender_map).tolist()
    for j in range(len(each_class_list)):
        subject_dir = each_class_dir + "\\" + str(each_class_list[j])
        each_subject = os.listdir(subject_dir)
        directory = [subject_dir] * len(each_subject)
        sum_list = []
        for (item1, item2) in zip(directory, each_subject):
            sum_list.append(item1+"\\"+item2)
        #if '.DS_Store' in sum_list: sum_list.remove('DS_Store')
        file_names.append(sum_list)
        k = k + 1
        for l in range(len(each_subject)):
            class_number.append(i)
            subject_number.append(k)
            label.append(subjects_gender[j])
            birth.append(subjects_Birth[j])
            
flat_list = [item for sublist in file_names for item in sublist]
data = {'file': flat_list,
        'birth': birth,
        'label': label,
        'class': class_number,
        'subject': subject_number
        }               
df = pd.DataFrame (data, columns =  ['file','label', 'birth', 'class', 'subject'])                
df.to_csv('info_true_subject_DS.csv')

features_label = df.apply(extract_features, axis=1)
np.save('features_label', features_label)