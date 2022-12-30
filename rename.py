import os

#folder = "friends_Courteney"
#name = "Courteney"

#folder = "friends_Jennifer"
#name = "Jennifer"

#folder = "friends_Lisa"
#name = "Lisa"

#folder = "friends_Matt"
#name = "Matt"

folder = "friends_Matthew"
name = "Matthew"


for count, filename in enumerate(os.listdir(folder)):
    dst = f"{name}_{str(count)}.jpg"
    src =f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
    dst =f"{folder}/{dst}"
        
    # rename() function will
    # rename all the files
    os.rename(src, dst)
