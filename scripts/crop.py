import dicom
import matplotlib.pyplot as plt 
import pylab
import os
import numpy as np
import time
import scipy.misc
from matplotlib import pyplot, cm
from get_edge import get_map
import random

path = "/home/zlstg1/cding0622/project/data_lung/"

lstFileDCM = []
map_dict = {}
for root, subdirs, files in os.walk(path):
	files.sort()
	for filename in files:
		path = os.path.join(root, filename)
		if filename.endswith(".dcm"):
			lstFileDCM += [path]
		elif filename.endswith(".xml"):			
			tmp_dict = get_map(path)
			map_dict.update(tmp_dict)



print(str(len(lstFileDCM)))
print(str(len(map_dict.keys())))
# get SOPInstanceUID from dcm files
# check if UID in xml files
img_id = 0
for i in range(len(lstFileDCM)):
	ref = dicom.read_file(lstFileDCM[i])
	uid = getattr(ref, "SOPInstanceUID", '')
	#print(uid)
	if uid in map_dict:
		for i in map_dict[uid]:
			# getting malignancy score
			score_list = [int(x) for x in map_dict[uid]["score"]]
			if len(score_list) != 0:
				score = sum(score_list)/len(score_list)
			else:
				continue
			if 0 < score <= 3:
				file = "benign"
			if 3 < score <= 5:
				file = "malignant"

			x_ary = []
			y_ary = []
			for coord in map_dict[uid][i]:
				if len(coord) == 2:
					x_ary += [int(coord[0])]
					y_ary += [int(coord[1])]
			if x_ary != [] or y_ary != []:
				x_min = min(x_ary)
				x_max = max(x_ary)
				y_min = min(y_ary)
				y_max = max(y_ary)

			#spliting 3:7 train and valid
			pvalid = 0.3
			r = random.randrange(0, 11)/10.0

			if r < pvalid:
				p_class = "valid"
			else:
				p_class = "train"
			#cutting the square containing the nodule from edge maps
			if not (x_min == x_max):
				tmp = ref.pixel_array
				img_ary = tmp[x_min:x_max, y_min:y_max]
				
				if file is "benign":
					a = random.randrange(1,4)
					rot_list = [0,a]
				elif file is "malignant":
					rot_list = [0,1,2,3]
				#shaped_ary = scipy.misc.toimage(img_ary, cmin=0.0).resize((48, 48))
				a = np.random.uniform(0, 2**16 - 1, (500, 500)).astype('int32')
				shaped_ary = scipy.misc.toimage(img_ary, high=np.max(a), low=np.min(a), mode='I').resize((48, 48))
				for i in rot_list: #rotatting 0, 90, 180, 270
					final_ary = np.rot90(shaped_ary, i)
					scipy.misc.imsave("/home/zlstg1/cding0622/balanced_data/%s/%s/%d.jpg" % (p_class, file, img_id), final_ary)
					img_id += 1



"""
# cropping the new file
a = [['312', '355'], ['311', '356'], ['310', '357'], ['309', '357'], ['308', '358'], ['308', '359'], ['308', '360'], ['307', '360'], ['306', '361'], ['306', '362'], ['305', '363'], ['304', '364'], ['303', '365'], ['303', '366'], ['302', '367'], ['302', '368'], ['302', '369'], ['301', '370'], ['301', '371'], ['300', '371'], ['299', '372'], ['299', '373'], ['299', '374'], ['299', '375'], ['299', '376'], ['300', '377'], ['301', '378'], ['302', '379'], ['303', '379'], ['304', '379'], ['305', '379'], ['306', '379'], ['307', '378'], ['308', '377'], ['308', '376'], ['309', '375'], ['310', '375'], ['311', '375'], ['312', '375'], ['313', '375'], ['314', '375'], ['315', '375'], ['316', '375'], ['317', '375'], ['318', '375'], ['319', '375'], ['320', '374'], ['321', '373'], ['322', '372'], ['322', '371'], ['322', '370'], ['323', '369'], ['324', '368'], ['325', '367'], ['326', '366'], ['327', '365'], ['328', '364'], ['328', '363'], ['327', '362'], ['327', '361'], ['326', '360'], ['325', '359'], ['324', '359'], ['323', '358'], ['322', '358'], ['321', '357'], ['320', '358'], ['319', '358'], ['318', '358'], ['318', '357'], ['317', '356'], ['316', '355'], ['315', '355'], ['314', '355'], ['313', '355'], ['312', '355'], ['314', '346'], ['313', '347'], ['313', '348'], ['313', '349'], ['313', '350'], ['312', '351'], ['312', '352'], ['312', '353'], ['311', '353'], ['310', '352'], ['309', '353'], ['308', '354'], ['308', '355'], ['308', '356'], ['308', '357'], ['307', '357'], ['306', '358'], ['306', '359'], ['306', '360'], ['305', '360'], ['304', '360'], ['303', '360'], ['302', '360'], ['301', '361'], ['300', '362'], ['300', '363'], ['301', '364'], ['302', '365'], ['302', '366'], ['302', '367'], ['301', '367'], ['300', '367'], ['299', '368'], ['298', '369'], ['298', '370'], ['298', '371'], ['298', '372'], ['298', '373'], ['299', '374'], ['299', '375'], ['299', '376'], ['299', '377'], ['299', '378'], ['300', '379'], ['301', '379'], ['302', '379'], ['303', '379'], ['304', '379'], ['305', '378'], ['306', '378'], ['307', '378'], ['308', '379'], ['309', '379'], ['309', '380'], ['310', '381'], ['310', '382'], ['311', '383'], ['312', '384'], ['313', '385'], ['314', '385'], ['315', '386'], ['316', '386'], ['317', '385'], ['318', '384'], ['318', '383'], ['318', '382'], ['318', '381'], ['319', '381'], ['320', '381'], ['321', '381'], ['322', '381'], ['323', '381'], ['324', '381'], ['325', '381'], ['326', '381'], ['327', '381'], ['328', '381'], ['329', '381'], ['330', '380'], ['330', '379'], ['330', '378'], ['330', '377'], ['330', '376'], ['330', '375'], ['330', '374'], ['330', '373'], ['330', '372'], ['331', '371'], ['331', '370'], ['331', '369'], ['331', '368'], ['331', '367'], ['331', '366'], ['331', '365'], ['330', '364'], ['330', '363'], ['330', '362'], ['330', '361'], ['329', '360'], ['329', '359'], ['328', '358'], ['327', '358'], ['326', '357'], ['325', '356'], ['324', '355'], ['323', '354'], ['322', '354'], ['321', '353'], ['320', '353'], ['320', '352'], ['319', '351'], ['318', '350'], ['317', '350'], ['316', '349'], ['316', '348'], ['315', '347'], ['314', '346'], ['312', '346'], ['311', '347'], ['311', '348'], ['311', '349'], ['310', '349'], ['309', '349'], ['308', '350'], ['308', '351'], ['308', '352'], ['307', '353'], ['306', '354'], ['306', '355'], ['306', '356'], ['306', '357'], ['306', '358'], ['305', '358'], ['304', '359'], ['303', '360'], ['303', '361'], ['302', '361'], ['301', '361'], ['300', '362'], ['299', '363'], ['299', '364'], ['299', '365'], ['299', '366'], ['299', '367'], ['299', '368'], ['300', '369'], ['300', '370'], ['300', '371'], ['299', '372'], ['298', '372'], ['297', '373'], ['298', '374'], ['298', '375'], ['299', '376'], ['300', '376'], ['300', '377'], ['300', '378'], ['300', '379'], ['301', '380'], ['301', '381'], ['302', '382'], ['303', '383'], ['304', '383'], ['305', '383'], ['306', '382'], ['306', '381'], ['307', '381'], ['308', '381'], ['309', '381'], ['310', '381'], ['311', '381'], ['312', '381'], ['313', '381'], ['314', '382'], ['315', '382'], ['315', '383'], ['316', '384'], ['317', '385'], ['318', '386'], ['319', '386'], ['320', '387'], ['321', '386'], ['322', '385'], ['322', '384'], ['322', '383'], ['323', '382'], ['324', '382'], ['325', '381'], ['325', '380'], ['325', '379'], ['324', '378'], ['324', '377'], ['324', '376'], ['324', '375'], ['324', '376'], ['325', '377'], ['326', '378'], ['327', '379'], ['328', '379'], ['329', '378'], ['329', '377'], ['329', '376'], ['329', '375'], ['330', '374'], ['331', '374'], ['332', '374'], ['333', '373'], ['334', '372'], ['334', '371'], ['334', '370'], ['334', '369'], ['334', '368'], ['334', '367'], ['333', '366'], ['333', '365'], ['333', '364'], ['333', '363'], ['332', '362'], ['331', '362'], ['330', '362'], ['329', '362'], ['328', '362'], ['328', '361'], ['329', '360'], ['329', '359'], ['328', '358'], ['328', '357'], ['328', '356'], ['328', '355'], ['327', '354'], ['326', '353'], ['325', '353'], ['324', '353'], ['323', '353'], ['322', '353'], ['321', '353'], ['320', '353'], ['319', '352'], ['319', '351'], ['318', '350'], ['317', '350'], ['317', '349'], ['316', '348'], ['315', '347'], ['314', '347'], ['313', '347'], ['312', '346'], ['308', '340'], ['307', '341'], ['308', '342'], ['308', '343'], ['309', '344'], ['309', '345'], ['310', '346'], ['311', '347'], ['311', '348'], ['312', '349'], ['311', '349'], ['310', '348'], ['309', '347'], ['308', '347'], ['307', '347'], ['306', '348'], ['306', '349'], ['306', '350'], ['306', '351'], ['306', '352'], ['305', '352'], ['305', '351'], ['305', '350'], ['305', '349'], ['305', '348'], ['305', '347'], ['305', '346'], ['304', '345'], ['303', '345'], ['302', '344'], ['301', '344'], ['300', '343'], ['299', '344'], ['299', '345'], ['299', '346'], ['300', '347'], ['300', '348'], ['301', '349'], ['301', '350'], ['302', '351'], ['303', '352'], ['303', '353'], ['304', '354'], ['304', '355'], ['304', '356'], ['304', '357'], ['304', '358'], ['303', '359'], ['302', '360'], ['302', '361'], ['302', '362'], ['302', '363'], ['301', '362'], ['300', '362'], ['299', '362'], ['298', '363'], ['298', '364'], ['299', '365'], ['300', '366'], ['300', '367'], ['300', '368'], ['300', '369'], ['300', '370'], ['300', '371'], ['300', '372'], ['300', '373'], ['300', '374'], ['299', '375'], ['298', '376'], ['299', '377'], ['299', '378'], ['299', '379'], ['299', '380'], ['300', '381'], ['300', '382'], ['301', '383'], ['302', '383'], ['303', '383'], ['304', '383'], ['305', '383'], ['306', '382'], ['306', '383'], ['307', '384'], ['308', '384'], ['309', '385'], ['310', '384'], ['311', '383'], ['312', '382'], ['313', '382'], ['314', '382'], ['315', '382'], ['316', '382'], ['317', '382'], ['318', '382'], ['319', '383'], ['320', '383'], ['321', '383'], ['322', '382'], ['323', '381'], ['324', '380'], ['325', '380'], ['326', '380'], ['327', '380'], ['328', '379'], ['328', '378'], ['328', '377'], ['328', '376'], ['329', '375'], ['330', '374'], ['331', '373'], ['332', '373'], ['333', '373'], ['334', '373'], ['335', '372'], ['335', '371'], ['335', '370'], ['335', '369'], ['335', '368'], ['335', '367'], ['335', '366'], ['335', '365'], ['335', '364'], ['334', '363'], ['333', '363'], ['332', '363'], ['331', '363'], ['330', '363'], ['330', '362'], ['330', '361'], ['330', '360'], ['329', '359'], ['328', '358'], ['327', '358'], ['326', '358'], ['325', '358'], ['324', '358'], ['324', '357'], ['324', '356'], ['324', '355'], ['324', '354'], ['325', '353'], ['324', '352'], ['323', '351'], ['322', '350'], ['321', '350'], ['320', '350'], ['319', '350'], ['318', '350'], ['317', '350'], ['317', '349'], ['317', '348'], ['317', '347'], ['317', '346'], ['316', '345'], ['315', '345'], ['314', '346'], ['314', '347'], ['313', '346'], ['313', '345'], ['312', '344'], ['312', '343'], ['311', '342'], ['310', '342'], ['309', '341'], ['308', '340'], ['314', '347'], ['313', '346'], ['312', '347'], ['311', '348'], ['310', '349'], ['309', '350'], ['309', '351'], ['308', '352'], ['307', '352'], ['306', '352'], ['305', '352'], ['305', '351'], ['305', '350'], ['304', '349'], ['303', '348'], ['302', '349'], ['302', '350'], ['302', '351'], ['302', '352'], ['302', '353'], ['302', '354'], ['302', '355'], ['302', '356'], ['302', '357'], ['302', '358'], ['302', '359'], ['302', '360'], ['302', '361'], ['302', '362'], ['302', '363'], ['302', '364'], ['301', '365'], ['301', '366'], ['300', '367'], ['300', '368'], ['300', '369'], ['300', '370'], ['300', '371'], ['300', '372'], ['300', '373'], ['300', '374'], ['299', '375'], ['299', '376'], ['300', '377'], ['300', '378'], ['301', '379'], ['301', '380'], ['302', '381'], ['302', '382'], ['303', '383'], ['304', '383'], ['305', '383'], ['305', '384'], ['306', '385'], ['306', '386'], ['306', '387'], ['306', '388'], ['307', '389'], ['308', '389'], ['309', '388'], ['310', '387'], ['311', '386'], ['312', '385'], ['313', '385'], ['314', '384'], ['315', '383'], ['316', '382'], ['316', '381'], ['316', '380'], ['317', '379'], ['318', '378'], ['319', '378'], ['320', '377'], ['321', '377'], ['322', '378'], ['323', '378'], ['324', '379'], ['325', '379'], ['326', '379'], ['327', '379'], ['328', '379'], ['329', '379'], ['330', '378'], ['331', '377'], ['331', '376'], ['331', '375'], ['331', '374'], ['331', '373'], ['332', '373'], ['333', '373'], ['334', '372'], ['335', '371'], ['336', '370'], ['336', '369'], ['337', '368'], ['337', '367'], ['337', '366'], ['337', '365'], ['337', '364'], ['336', '363'], ['335', '362'], ['335', '361'], ['334', '360'], ['333', '360'], ['333', '359'], ['332', '358'], ['331', '358'], ['330', '358'], ['329', '358'], ['328', '357'], ['327', '356'], ['326', '355'], ['325', '355'], ['324', '355'], ['323', '354'], ['322', '354'], ['322', '353'], ['321', '352'], ['320', '352'], ['319', '351'], ['318', '350'], ['318', '349'], ['317', '348'], ['316', '348'], ['315', '348'], ['314', '348'], ['314', '347'], ['315', '349'], ['314', '350'], ['313', '351'], ['312', '351'], ['311', '352'], ['310', '353'], ['309', '353'], ['308', '353'], ['307', '353'], ['306', '354'], ['305', '355'], ['304', '356'], ['303', '357'], ['302', '358'], ['302', '359'], ['302', '360'], ['302', '361'], ['302', '362'], ['302', '363'], ['301', '364'], ['300', '365'], ['300', '366'], ['300', '367'], ['300', '368'], ['300', '369'], ['300', '370'], ['300', '371'], ['300', '372'], ['300', '373'], ['300', '374'], ['300', '375'], ['300', '376'], ['301', '377'], ['302', '377'], ['303', '377'], ['304', '378'], ['304', '379'], ['305', '380'], ['305', '381'], ['306', '382'], ['307', '383'], ['308', '384'], ['309', '385'], ['310', '385'], ['311', '384'], ['312', '383'], ['313', '382'], ['313', '381'], ['313', '380'], ['314', '379'], ['315', '379'], ['316', '379'], ['317', '379'], ['318', '379'], ['319', '379'], ['320', '379'], ['321', '379'], ['322', '379'], ['323', '379'], ['324', '379'], ['325', '379'], ['325', '380'], ['325', '381'], ['326', '382'], ['327', '381'], ['328', '381'], ['329', '380'], ['330', '380'], ['331', '380'], ['332', '379'], ['332', '378'], ['332', '377'], ['332', '376'], ['332', '375'], ['332', '374'], ['332', '373'], ['332', '372'], ['332', '371'], ['333', '371'], ['334', '370'], ['335', '369'], ['335', '368'], ['335', '367'], ['335', '366'], ['335', '365'], ['334', '364'], ['334', '363'], ['334', '362'], ['333', '361'], ['332', '360'], ['331', '359'], ['330', '358'], ['330', '357'], ['330', '356'], ['330', '355'], ['329', '354'], ['328', '354'], ['327', '354'], ['326', '355'], ['325', '355'], ['324', '355'], ['323', '355'], ['322', '355'], ['321', '355'], ['320', '354'], ['319', '353'], ['319', '352'], ['319', '351'], ['319', '350'], ['318', '349'], ['317', '349'], ['316', '349'], ['315', '349'], ['310', '351'], ['309', '352'], ['309', '353'], ['309', '354'], ['308', '354'], ['307', '354'], ['306', '355'], ['305', '355'], ['304', '354'], ['303', '355'], ['303', '356'], ['303', '357'], ['303', '358'], ['303', '359'], ['303', '360'], ['302', '361'], ['301', '362'], ['301', '363'], ['301', '364'], ['301', '365'], ['301', '366'], ['301', '367'], ['301', '368'], ['302', '369'], ['303', '369'], ['304', '370'], ['304', '371'], ['303', '372'], ['302', '372'], ['301', '373'], ['301', '374'], ['302', '375'], ['303', '375'], ['304', '375'], ['305', '376'], ['306', '377'], ['307', '377'], ['307', '378'], ['307', '379'], ['308', '380'], ['309', '381'], ['310', '382'], ['311', '381'], ['312', '380'], ['313', '380'], ['314', '379'], ['315', '378'], ['316', '378'], ['317', '378'], ['318', '378'], ['319', '378'], ['320', '379'], ['321', '379'], ['322', '379'], ['323', '378'], ['323', '377'], ['324', '376'], ['325', '376'], ['326', '376'], ['327', '377'], ['327', '378'], ['328', '379'], ['329', '379'], ['330', '379'], ['331', '379'], ['332', '378'], ['332', '377'], ['332', '376'], ['332', '375'], ['332', '374'], ['332', '373'], ['333', '372'], ['334', '371'], ['334', '370'], ['334', '369'], ['334', '368'], ['333', '367'], ['333', '366'], ['332', '365'], ['331', '364'], ['331', '363'], ['330', '362'], ['330', '361'], ['330', '360'], ['330', '359'], ['330', '358'], ['330', '357'], ['330', '356'], ['330', '355'], ['330', '354'], ['330', '353'], ['329', '352'], ['328', '353'], ['327', '354'], ['326', '354'], ['325', '354'], ['324', '354'], ['323', '354'], ['322', '354'], ['321', '354'], ['320', '354'], ['319', '354'], ['319', '353'], ['319', '352'], ['318', '351'], ['317', '352'], ['317', '353'], ['317', '354'], ['316', '354'], ['315', '354'], ['314', '355'], ['313', '355'], ['313', '354'], ['313', '353'], ['313', '352'], ['312', '351'], ['311', '351'], ['310', '351'], ['306', '351'], ['305', '352'], ['305', '353'], ['304', '354'], ['304', '355'], ['304', '356'], ['304', '357'], ['304', '358'], ['304', '359'], ['304', '360'], ['304', '361'], ['304', '362'], ['304', '363'], ['303', '364'], ['302', '365'], ['302', '366'], ['302', '367'], ['303', '368'], ['303', '369'], ['303', '370'], ['303', '371'], ['303', '372'], ['302', '373'], ['303', '374'], ['304', '375'], ['305', '376'], ['305', '377'], ['304', '378'], ['304', '379'], ['304', '380'], ['304', '381'], ['305', '382'], ['306', '381'], ['307', '381'], ['308', '381'], ['309', '381'], ['310', '382'], ['311', '382'], ['312', '383'], ['313', '384'], ['314', '383'], ['314', '382'], ['314', '381'], ['315', '380'], ['316', '380'], ['317', '380'], ['318', '380'], ['319', '380'], ['320', '380'], ['321', '380'], ['322', '380'], ['323', '379'], ['324', '378'], ['325', '378'], ['326', '378'], ['327', '378'], ['328', '377'], ['328', '376'], ['328', '375'], ['328', '374'], ['328', '373'], ['328', '372'], ['328', '371'], ['328', '370'], ['328', '369'], ['327', '368'], ['327', '367'], ['326', '366'], ['325', '365'], ['325', '364'], ['324', '363'], ['324', '362'], ['325', '361'], ['326', '360'], ['327', '359'], ['328', '359'], ['329', '358'], ['329', '357'], ['329', '356'], ['328', '355'], ['327', '354'], ['326', '353'], ['325', '353'], ['324', '353'], ['323', '354'], ['322', '354'], ['321', '354'], ['320', '354'], ['319', '354'], ['318', '354'], ['317', '354'], ['316', '353'], ['315', '352'], ['314', '352'], ['313', '351'], ['312', '351'], ['311', '351'], ['310', '351'], ['309', '351'], ['308', '351'], ['307', '351'], ['306', '351'], ['187', '166'], ['403', '272'], ['392', '317']]
x_ary = []
y_ary = []
for i in a:
	x_ary += [int(i[0])]
	y_ary += [int(i[1])]

x_min = min(x_ary)
x_max = max(x_ary)
y_min = min(y_ary)
y_max = max(y_ary)


print("x: " + str(x_min) + " " + str(x_max))
print("y: " + str(y_min) + " " + str(y_max))

tmp = ref.pixel_array
ref.PixelData = ref.pixel_array.tostring()
img_ary = tmp[x_min:x_max, y_min:y_max]

scipy.misc.toimage(img_ary, cmin=0.0).save("3.jpg")
#TODO resize the cropped dcm to a uniformed size

# plot 2 original and modified dcm images
a = [ref.pixel_array, img_ary]
fig, axes = plt.subplots(1,2)
fig.subplots_adjust(hspace = 0.01, wspace = 0.2)

for i, ax in enumerate(axes.flat):
	#ax.imshow(a[i].pixel_array, cmap=pylab.cm.gist_gray)
	ax.imshow(a[i], cmap='binary')

	#adding label
	xlabel = "ref %d" % i
	ax.set_xlabel(xlabel)


plt.show()
"""
