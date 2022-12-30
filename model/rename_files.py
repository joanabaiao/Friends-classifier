import os

folder = "./images_dataset/cropped/"
names = ["David_Schwimmer", "Courteney_Cox", "Jennifer_Aniston", "Lisa_Kudrow", "Matt_LeBlanc", "Matthew_Perry"]

for name in names:
    path = folder + name
    for count, filename in enumerate(os.listdir(path)):
        dst = f"{name}_{str(count)}.jpg"
        src =f"{path}/{filename}"  # foldername/filename, if .py file is outside folder
        dst =f"{path}/{dst}"
            
        # rename() function will rename all the files
        os.rename(src, dst)
