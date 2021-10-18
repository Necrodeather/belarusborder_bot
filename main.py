from os import system
from re import compile, escape
   
#название программы, которую мы ищем
search_bdo = compile(escape(' '))

def recursion(command):
    system('tasklist /NH /SVC > processes.txt')
    with open('processes.txt', 'r') as logs:
        lines = logs.readlines()
        for line in lines:
            bdo = command.search(line)
            if bdo is None:
                continue
            else:
                with open('bdo.txt', 'w') as bdo:
                    bdo.write('done')
                    bdo.close()
                    logs.close()
                with open('bdo.txt', 'r') as bdo:
                    exam = bdo.readlines()
                    for line in exam:
                        if line is None:
                            bdo.close()
                            break
                        else:
                            try:
                                recursion(search_bdo)
                            except RecursionError:
                                continue

recursion(search_bdo)
system('del bdo.txt')
system('del processes.txt')