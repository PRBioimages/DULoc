import shutil,os
import pandas as pd 
import numpy as np
import cv2
label_list = ['actin filaments', 'cell junctions', 'centriolar satellite', 'centrosome',
					'cytoplasmic bodies', 'cytosol', 'endoplasmic reticulum', 'focal adhesion sites',
					'golgi apparatus', 'intermediate filaments','lipid droplets', 'lysosomes',
					'microtubules', 'mitochondria', 'nuclear bodies', 'nuclear membrane',
					'nuclear speckles', 'nucleoli', 'nucleoli fibrillar center', 'nucleoplasm',
					'peroxisomes', 'plasma membrane', 'rods & rings', 'vesicles']
# label_list = ['cytosol', 'mitochondria', 'nucleoli', 'nucleoplasm','plasma membrane', 'vesicles']

def mkdir(dirName):
	if not os.path.exists(dirName):
		os.makedirs(dirName)
		print('---the '+dirName+' is created!---')
	else:
		print('---The dir is there!---')

def cal_gray_level(img_dir, img_csv):
	img_list = pd.read_csv(img_csv)
	mean_value_dist = {}
	mean_value_list = []
	lab_list = []
	img_ids = img_list['sample_id'].values
	img_labels = img_list['label'].values
	for label in label_list:
		lab_values = []
		for i in range(len(img_ids)):
			if img_labels[i]==label:
				imgpath = os.path.join(img_dir, str(img_ids[i])+'_green.jpg')
				green_arr = cv2.split(cv2.imread(imgpath))[1]
				arr_mean = np.mean(green_arr)
				lab_values.append(arr_mean)
			else:
				continue
		lab_values_mean = np.mean(lab_values)
		print(label, lab_values_mean)
		mean_value_dist[label] = lab_values_mean
		lab_list.append(label)
		mean_value_list.append(lab_values_mean)
	dist = {'label_id': lab_list, 'mean_value': mean_value_list}
	print(dist)
	df = pd.DataFrame(data=dist, index=None, columns=['label_id', 'mean_value'])
	df.to_csv('label_gray_mean.csv', index=False)
	return mean_value_dist

def high_intensity_img(img_dir, new_img_dir, img_csv, new_img_csv, mean_value_dist):
	img_list = pd.read_csv(img_csv)	
	img_ids = img_list['sample_id'].values
	img_labels = img_list['label'].values
	new_sample_id = []
	new_label_id = []
	mkdir(new_img_dir)
	for i in range(len(img_ids)):
		imgpath = os.path.join(img_dir, str(img_ids[i])+'_green.jpg')
		newpath = os.path.join(new_img_dir, str(img_ids[i])+'_green.jpg')
		green_arr = cv2.split(cv2.imread(imgpath))[1]
		arr_mean = np.mean(green_arr)
		img_label = img_labels[i]
		mean_value = mean_value_dist[img_label]
		if arr_mean >= mean_value:
			print(imgpath)
			shutil.copy(imgpath, newpath)
			shutil.copy(imgpath.replace('green.jpg', 'blue.jpg'), newpath.replace('green.jpg', 'blue.jpg'))
			shutil.copy(imgpath.replace('green.jpg', 'yellow.jpg'), newpath.replace('green.jpg', 'yellow.jpg'))
			shutil.copy(imgpath.replace('green.jpg', 'red.jpg'), newpath.replace('green.jpg', 'red.jpg'))
			shutil.copy(imgpath.replace('green.jpg', 'mask.png'), newpath.replace('green.jpg', 'mask.png'))
			new_sample_id.append(img_ids[i])
			new_label_id.append(img_labels[i])
		else:
			continue

	dist = {'sample_id':new_sample_id, 'label':new_label_id}			
	df = pd.DataFrame(data=dist, index=None, columns=['sample_id','label'])
	df.to_csv(new_img_csv, index= False)


if __name__ == '__main__':
	# add raw path
	img_dir = 'new_samples'
	img_csv = 'new_samples.csv'
	new_img_dir = 'hgray_samples'
	new_img_csv = 'hgray_samples.csv'
	mean_value_dist = cal_gray_level(img_dir, img_csv)
	print(mean_value_dist)
	high_intensity_img(img_dir, new_img_dir, img_csv, new_img_csv, mean_value_dist)
