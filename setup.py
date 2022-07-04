import subprocess as sb
import sys
import platform

if sb.getstatusoutput('echo $SHELL')[1] == '/bin/zsh':
    
    if platform.system() == 'Darwin':
        proc = sb.Popen(["whoami"], stdin=sb.PIPE, stdout=sb.PIPE, stderr=sb.PIPE, text=True)
        uname = proc.communicate()[0]
        proc.wait()
        path = "/Users/" + uname[:-1] + "/.zshrc"

    elif platform.system() == 'Linux':
        proc = sb.Popen(["xdg-user-dir"], stdin=sb.PIPE, stdout=sb.PIPE, stderr=sb.PIPE, text=True)
        uname = proc.communicate()[0]
        proc.wait()
        path = uname[:-1] + "/.zshrc"

elif sb.getstatusoutput('echo $SHELL')[1] == '/bin/bash':
    if platform.system() == 'Linux':
        proc = sb.Popen(["xdg-user-dir"], stdin=sb.PIPE, stdout=sb.PIPE, stderr=sb.PIPE, text=True)
        uname = proc.communicate()[0]
        proc.wait()
        path = uname[:-1] + "/.bashrc"
    
f = open(path, "r")
ls = f.readlines()
f.close()
f = open(path, "a")

if f"alias ngit='python3 {sys.path[0]}/Git_clone/git_clone.py' \n" in ls:
    print("You already have ngit")    

else:
    f.write(f"alias ngit='python3 {sys.path[0]}/Git_clone/git_clone.py' \n")
    print("Now you can use ngit in your terminal")

f.close()

