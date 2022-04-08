import os

DIR_IN='inputs'
DIR_OUT='csar'
FILE_LOG='generate.log'
FILE_OUT='dma_adt.csar'

def save_to_file(dir, file, content):
    f = open(os.path.join(dir,file), "a")
    f.write(str(content)+'\n')
    f.close()
    return

def add_log(full_wd, message):
    f = open(os.path.join(full_wd,FILE_LOG), "a")
    f.write(message)
    f.close()
    return
