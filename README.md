# DULoc-images
It's a deep-learning-based pattern unmixing pipeline for protein subcellular localization (DULoc) to quantitatively estimate the fractions of proteins localizing in different subcellular compartments from immunofluorescence images. The publication about this source code is 'DULoc: quantitatively unmixing protein subcel-lular location patterns in immunofluorescence images based on deep learning features'
## 1 part1 Dataset
Real_dataset can be accessed by 'http://murphylab.cbd.cmu.edu/software/2010_PNAS_Unmixing/'.
The samples of synthetic dataset are shown in .\Synthetic_dataset\data, and the synthetic processing is in .\Synthetic_dataset\code.
## 2 part2 Bestfitting
The deep learning model, Bestfitting, can be obtained by ‘https://github.com/CellProfiling/HPA-competition-solutions/tree/master/bestfitting’.
## 3 part3 Unmixing methods
Before running, replace '.\functions\RNNMF' in .\functions\do_RNNMF.mat with full path of 'RNNMF'.
Run MasterSamples.m.
