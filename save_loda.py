import time
def save(Input_line, Temp_file, Output_line, Output_container, Use_prores, Prores_type, Factor, half, Batch_size, Model_name, Mulit_gpu, gpu_id):
    string=f"{Input_line}\n{Temp_file}\n{Output_line}\n{Output_container}\n{Use_prores}\n{Prores_type}\n{Factor}\n{half}\n{Batch_size}\n{Model_name}\n{Mulit_gpu}\n{gpu_id}"
    print(string)
    text_file = open("save.txt", "w")
    text_file.write(string)
    text_file.close()
def convertbool(string):
    if string=="True":
        ret = True
    if string=="False":
        ret = False
    #print(string, ret)
    return ret   
def load():
    file1 = open('save.txt', 'r')
    Lines = file1.readlines()
    count=0
    for line in Lines:
        count += 1
        print("Line{}: {}".format(count, line.strip()))
        time.sleep(0.1)
        if count==1:
            Input_line = line.strip()
        if count==2:
            Temp_file = line.strip()
        if count==3:
            Output_line = line.strip()
        if count==4:
            Output_container = line.strip()
        if count==5:
            Use_prores = convertbool(line.strip())
        if count==6:
            Prores_type = line.strip()
        if count==7:
            Factor = line.strip()
        if count==8:
            Half = convertbool(line.strip())
        if count==9:
            Batch_size = line.strip()
        if count==10:
            Model_name = line.strip()
        if count==11:
            Mulit_gpu = convertbool(line.strip())
        if count==12:
            gpu_id = line.strip()
    return Input_line, Temp_file, Output_line, Output_container, Use_prores, Prores_type, Factor, Half, Batch_size, Model_name, Mulit_gpu, gpu_id
    print(f"{Input_line}\n{Temp_file}\n{Output_line}\n{Output_container}\n{Use_prores}\n{Prores_type}\n{Factor}\n{Half}\n{Mulit_gpu}\n{gpu_id}\n{Model_name}")
    file1.close()
