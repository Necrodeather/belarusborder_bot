import subprocess

def proccess():
    run = subprocess.run(['script.bat'], stdout=subprocess.DEVNULL)

    if run.returncode == 0:
        proccess()
    else:
        raise FileNotFoundError() #Временное решение

proccess()
