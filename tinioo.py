import os
import tinify
import dropbox
import dropbox.files
import datetime

# CREATE .txt FILES WITH ACCESS CREDENTIALS
if os.path.isfile("./dropkey.txt"):
    with open("./dropkey.txt") as file:
        dropkey = file.read()
else:
    dropkey = input("Type your Dropbox App Token: ")
    with open("dropkey.txt", "w+") as f:
        f.write(dropkey)

if os.path.isfile("./tinikey.txt"):
    with open("./tinikey.txt") as file:
        tinikey = file.read()
else:
    tinikey = input("Type your Tinify API Token: ")
    with open("tinikey.txt", "w+") as f:
        f.write(tinikey)

# SELECT SOURCE AND DESTINATION FOLDER
source_folder = input(
    "Where are your original photos stored? (Leave empty if in app's root folder) ")
if source_folder != "":
    source_folder = "/" + source_folder

dest_folder = input(
    "Where do you want to store the optimized photos? ")
#dest_folder = "/" + dest_folder

# AUTHENTICATION
dbx = dropbox.Dropbox(dropkey)
tinify.key = tinikey

dbx.users_get_current_account()
response = dbx.files_list_folder(source_folder)
files = response.entries

# CHECKING FOR DESTINATION FOLDER IN DROPBOX
found = False
for item in response.entries:
    if str(type(item))[22:-10] == "Folder":
        if (str(item.path_display)[1:]) == dest_folder:
            found = True
    else:
        break
if found == False:
    dbx.files_create_folder("/" + dest_folder)
dest_folder = "/" + dest_folder

# CHECKING FOR FOLDER LOCALLY AND CREATING IF NOT EXISTING
if not os.path.isdir("." + dest_folder):
    os.mkdir("." + dest_folder)

# COMPRESSING ALL PHOTOS IN GIVEN FOLDER
for item in files:
    if str(type(item))[22:-10] == "File":
        source = tinify.from_url(
            dbx.files_get_temporary_link(item.path_display).link)
        dest = dest_folder[1:] + "/" + item.name
        source.to_file(dest)
print("Photos successfully optimized")
print("Starting uploading")
# UPLOAD ALL PHOTOS
photos = os.listdir("." + dest_folder)
count = 0
for item in photos:
    itempath = "." + dest_folder + "/" + item
    with open(itempath, 'rb') as f:
        dbx.files_upload(f.read(), dest_folder + "/" + item, mute=True)
    count += 1
    print("Progress: ", count, "out of ", len(photos), uploaded)
