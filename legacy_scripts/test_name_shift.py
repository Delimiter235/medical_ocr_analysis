import os


project_path = os.path.abspath(os.getcwd())
input_path = f"{project_path}/data/raw/images/blood_routine/"

files = os.listdir(input_path)
for file in files:
    file_path = os.path.join(input_path, file)

    os.rename(file_path, f"{input_path}{file[0:10]}_blood_routine.png")
    #print(file[0:10])