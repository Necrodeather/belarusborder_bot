from os import system
from re import compile, escape

def cmd_processes(cmd):
    system(cmd)

def exam_process(file, prcs):
    with open(file) as logs:
        lines = logs.readlines()
    for line in lines:
        proc = prcs.search(line)
        if proc is None:
            continue
        else:
            logs.close()
            var=0
        while var == 1:
            system('del {file}')
            break
        else:
            print('done')

filename = 'processes.txt'
command = f'tasklist /NH /SVC > {filename}'

process = compile(escape('putty.exe'))

while True:
    cmd_processes(command)
    exam_process(filename, process)


