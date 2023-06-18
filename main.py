from dotenv import load_dotenv
import os
import subprocess
import threading

dir = os.getcwd()
load_dotenv()

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
fnpath = os.getenv("FNPATH")
userargs = os.getenv("ARGS")
redirect = os.getenv("REDIRECT")
server = os.getenv("SERVER")
injector = os.getenv("INJECTOR")

def CheckForCrash():
    while (True):
        output = subprocess.check_output(["tasklist", "/FI", "IMAGENAME eq CrashReportClient.exe"]).decode("utf-8")
        if "INFO: No tasks are running which match the specified criteria" not in output:
            os.system("taskkill /f /im CrashReportClient.exe")

CheckForCrashes = threading.Thread(target=CheckForCrash)
CheckForCrashes.start()

args = f" -epicapp=Fortnite -epicenv=Prod -epicportal -AUTH_TYPE=epic -AUTH_LOGIN=\"{email}\" -AUTH_PASSWORD=\"{password}\" -epiclocale=en-us -fltoken=3db3ba5dcbd2e16703f3978d -fromfl=none -noeac -nobe -skippatchcheck -caldera=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiYmU5ZGE1YzJmYmVhNDQwN2IyZjQwZWJhYWQ4NTlhZDQiLCJnZW5lcmF0ZWQiOjE2Mzg3MTcyNzgsImNhbGRlcmFHdWlkIjoiMzgxMGI4NjMtMmE2NS00NDU3LTliNTgtNGRhYjNiNDgyYTg2IiwiYWNQcm92aWRlciI6IkVhc3lBbnRpQ2hlYXQiLCJub3RlcyI6IiIsImZhbGxiYWNrIjpmYWxzZX0.VAWQB67RTxhiWOxx7DBjnzDnXyyEnX7OljJm-j2d88G_WgwQ9wrE6lwMEHZHjBd1ISJdUO1UVUqkfLdU5nofBQ " + userargs
exe = fnpath + "\FortniteGame\Binaries\Win64\FortniteClient-Win64-Shipping.exe"

i = 1
givingitems = True
while(givingitems):
    arg = os.getenv(f"ITEM{i}")
    if arg != None:
        args += f" -item{i}={arg}"
    else:
        givingitems = False
    i += 1

playlist = os.getenv("PLAYLIST")
port = os.getenv("PORT")
region = os.getenv("REGION") # this can probably be automated with an ip check but f it
mmcode = os.getenv("MMCODE")

blategame = os.getenv("LATEGAME")
binfmats = os.getenv("INFMATS")
binfammo = os.getenv("INFAMMO")

starthealth = os.getenv("STARTHEALTH")
startshield = os.getenv("STARTSHIELD")
siphon = os.getenv("SIPHON")

args += f" -playlist={playlist} -port={port} -region={region} -mmcode={mmcode} -lategame={blategame} -infmats={binfmats} -infammo={binfammo} -startshield={startshield} -starthealth={starthealth} -siphon={siphon}"

os.system(f"\"{injector}\"")
print(exe + args)
os.system("pause")

def launchfn():
    process = subprocess.Popen(exe + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    while True:
        output = process.stdout.readline().strip()
        print(output)
        if output == '' and process.poll() is not None:
            break
        if output:
            if 'Platform has ' in output:
                print("Injecting redirect!")
                os.system(f"{injector} -p {process.pid} -i {redirect}")
            if 'Region ' in output:
                print("Injecting server!")
                os.system(f"{injector} -p {process.pid} -i {server}") # i promise this is fine
    process.wait()
    return

while True:
    launchfn()
