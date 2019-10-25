import os
import loginDB

def deleteRedundantImages():
	folder = './static/imges/profilePics'


	images = os.listdir(folder)

	imagesToDelete = []
	count = 0

	profilePics = loginDB.listProfilePics()
	#print(len(profilePics))

	for img in images:
		for i in range(len(profilePics)):
			if(img != "defaultProfileImage.png"):
				if(img!=profilePics[i][0]):
					imagesToDelete.append(img)
					count = count + 1

	print("Images existing Currently in the Folder : ")
	print(images)
	print("\n")

	print("List of Redundant Images that can be deleted : ")
	print(imagesToDelete)
	print("\n")

	print("Deleting Redundant Images.....")
	for i in range(len(imagesToDelete)):
		os.remove("/".join([folder,imagesToDelete[i]]))

	print("Deletion Successful..")
	print("{} Image(s) Deleted...\n".format(count))

