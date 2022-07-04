from array import typecodes
import subprocess as sb
from glob import glob
from random import randint
from colorama import init, Fore
import time
import sys
import os
import platform


init(autoreset=True)# Գունավոր տպելու համար

def terminal(arg, input="", ret="out"):
    proc = sb.Popen(arg, stdin=sb.PIPE, stdout=sb.PIPE, stderr=sb.PIPE, text=True)
    std_out, std_err = proc.communicate(input)
    proc.wait()
    if ret == "out":
        return std_out.split("\n")[:-1]
    elif ret == "err":
        return std_err.split("\n")[:-1]
    else:
        return proc.poll()


working_directory = terminal(["pwd"])[0]
ngit_working_directory = f"{sys.path[0]}/.."
try:
    f = open(f"{working_directory}/.ngit/branch_info.txt", "r")
    branch = f.readlines()[1].split()[-1]
    f.close()
except FileNotFoundError:
    branch = "master"

def ls_a(pth=working_directory):
    return terminal(["ls", "-a", pth])

def ls_la(pth=working_directory):
    return terminal(["ls", "-la", pth])

#NGitIgnore

if not ".ngitignore" in terminal(['ls', '-a', working_directory]):
    terminal(['touch', '.ngitignore'])

ngit_ignore = [[line.strip() for line in open(f"{working_directory}/.ngitignore").readlines() if line.startswith('.')],
               [line.strip() for line in open(f"{working_directory}/.ngitignore").readlines() if not line.startswith('.')]]


def ngit_add(args=[], add_all=False, wd=working_directory):
    try:
        f = open(f"{working_directory}/.ngit/branch_info.txt", "r")
        branch = f.readlines()[1].split()[-1]
        f.close()
    except FileNotFoundError:
        branch = "master"

    if add_all:
        ls = ls_a()
        ls.remove(".")
        ls.remove("..")
        ls.remove(".ngit")
        args = ls
    ls_add = ls_a(f"{wd}/.ngit/{branch}/add/")
    ls_add.remove(".")    
    ls_add.remove("..")
    st = list(set(ls_add) - set(args))
    for i in args:
        pthh = ""
        if "/" in i:# if we want to do ngit add t/tt/ttt/tttt/ttttt/some.py
            name = ""
            for j in i[::-1]:
                if j != "/":
                    name += j
                else:
                    break
            name = name[::-1]
            pthh = i[:len(i)-len(name)]

        if platform.system() == 'Darwin':
            ex_code = terminal(["rsync", "-rua", f"{wd}/{i}", f"{wd}/.ngit/{branch}/add/{pthh}"], ret="ex")
        else:
            ex_code = terminal(["cp", "-rua", f"{wd}/{i}", f"{wd}/.ngit/{branch}/add/{pthh}"], ret="ex")

        if ex_code:
            print("Error in adding")

    if add_all:
        for i in st:
            ex_code_0_5 = terminal(["rm", "-r", f"{wd}/.ngit/{branch}/add/{i}"], ret="ex")
            if ex_code_0_5:
                print(ex_code, "Error on deleting something in add") 

def generate_code():
    ls = "qwertyuiopasdfghjklzxcvbnm_0123456789"
    res = ""
    for _ in range(20):
        i = randint(0, len(ls) - 1)
        res += ls[i]
    return res




def ngit_status(for_user = True):
    if for_user:
        print("On branch ", branch, "\n")
    
    
    f = open(f"{working_directory}/.ngit/{branch}/commits/info.txt", "r")
    num = f.readlines()[0].split()[-1]
    f.close()

    f = open(f"{working_directory}/.ngit/{branch}/commits/info.txt", "r")
    num = f.readlines()[0].split()[-1]
    f.close()
    if num == "0" and for_user:
        print("No commits yet")
    
    def have_dif(tpl):
        return tpl[0] or tpl[1] or tpl[2]

    def print_dif(tpl, color = ""):
        keys_for_print = ["New file : ", "Deleted : ", "Modified : "]
        for i in range(len(tpl)):
            if tpl[i]:
                for elem in tpl[i]:
                    print(color + keys_for_print[i], end="")
                    print(elem)

    
    curr_path = working_directory
    addd_path = f"{working_directory}/.ngit/{branch}/add"
    comm_m_1_path = f"{working_directory}/.ngit/{branch}/commits/{num}"

    # are_dif_curr_comm_m_1 = are_different(curr_path, comm_m_1_path)
    # are_dif_curr_addd = are_different(curr_path, addd_path)
    # are_dif_add_comm_m_1 = are_different(addd_path, comm_m_1_path)

    dif_curr_comm_m_1 = find_diff_for_status(curr_path, comm_m_1_path)
    dif_curr_addd = find_diff_for_status(curr_path, addd_path)
    dif_add_comm_m_1 = find_diff_for_status(addd_path, comm_m_1_path)

    ignored = set()

    # appendes, deletes, modifies
    for lst in dif_curr_addd:
        for file in lst:
            if in_ngitignore(file):
                ignored.add(file)

    dif_curr_addd[0] = list(set(dif_curr_addd[0]) - ignored)

    if for_user:
        bool_for_print = True
        if have_dif(dif_add_comm_m_1):
            bool_for_print = False
            print("\nYou have to commit`\n")
            print_dif(dif_add_comm_m_1, Fore.GREEN)
        if have_dif(dif_curr_addd):
            bool_for_print = False
            print("\nUntracked files:")
            print("  (use \"ngit add ...\" to include in what will be committed)")
            print_dif(dif_curr_addd, Fore.RED)
        if bool_for_print:
            print("nothing to add or commit, working tree clean")
    else:
        return dif_curr_comm_m_1 


def in_ngitignore(file):
    if file.startswith('.') and file in ngit_ignore[0] or file in ngit_ignore[1]:
        return True


def ngit_branch():
    f = open(f"{working_directory}/.ngit/branch_info.txt", "r")
    ls = f.readlines()
    f.close()
    for i in ls[:2]:
        print(i, end="")
    for i in ls[2:]:
        br = ls[1].split()[-1]
        if i == br + "\n":
            print(Fore.GREEN + ">" + " ", end="")
            print(i, end="")
        else:
            print(" ", i, end="")


def ngit_new_branch(br_name):
    ex_code_7 = terminal(["mkdir", working_directory + "/.ngit/" + br_name], ret="ex")
    if ex_code_7:
        print(ex_code_7, "7")

    ex_code_8 = terminal(["rsync", "-r"] + glob(f"{ngit_working_directory}/.ngit/master/*") + [working_directory + "/.ngit/" + br_name + "/"], ret="ex")
    if ex_code_8:
        print("Error in initializing new branch : " + br_name)
    f = open(f"{working_directory}/.ngit/branch_info.txt", "r")
    ls = f.readlines()
    f.close()    
    spl = ls[0].split()
    spl[-1] = str(int(spl[-1]) + 1)
    ls_2 = [" ".join(spl) + "\n"]
    ls_2 += ls[1:] + [br_name + "\n"]
    f = open(f"{working_directory}/.ngit/branch_info.txt", "w")
    f.writelines(ls_2)
    f.close()  


def ngit_checkout(branch_name):
    f = open(f"{working_directory}/.ngit/branch_info.txt", "r")
    ls = f.readlines()
    f.close()
    branch_list = [strr[:-1] for strr in ls[2:]]
    if branch_name in branch_list:
        dif_curr_comm_m_1 = ngit_status(for_user=False)
        if not True in [bool(i) for i in dif_curr_comm_m_1]:
            line_2 = ls[1].split()[:2] + [branch_name + "\n"]
            line_2 = " ".join(line_2)
            # print(repr(line_2))
            ls_2 = [ls[0]] + [line_2] + ls[2:]        
            f = open(f"{working_directory}/.ngit/branch_info.txt", "w")
            f.writelines(ls_2)
            f.close()
            # ngit_brunch()
            ex_code_9 = terminal(["rm", "-r"] + glob(f"{working_directory}/[!.'ngit']*", recursive=True))
            if ex_code_9:
                print(ex_code_9, 99999999999999)
            f = open(f"{working_directory}/.ngit/{branch_name}/commits/info.txt", "r")
            num = f.readlines()[0].split()[-1]
            f.close()
            if num:
                lst = ls_a(pth=f"{working_directory}/.ngit/{branch_name}/commits/{num}/")
                for i in lst:
                    if i != ".." and i != "." and i != ".ngit":
                        a = f"{working_directory}/.ngit/{branch_name}/commits/{num}/{i}"
                        b = f"{working_directory}/"
                        ex_code_10 = terminal(["rsync", "-ra", a, b], ret="ex")
                        if ex_code_10:
                            print("10 10 10", ex_code_10)
            

        else:
            print("You need to commit your changes before changing branch")    

    else:
        print("Branch " + branch_name + " dont exist")


def ngit_merge(br_name):
    f = open(f"{working_directory}/.ngit/branch_info.txt", "r")
    ls = f.readlines()
    f.close()
    branch_list = [strr[:-1] for strr in ls[2:]]
    if br_name in branch_list:
        f = open(f"{working_directory}/.ngit/master/commits/info.txt", "r")
        num_master = f.readlines()[0].split()[-1]
        f.close()
        f = open(f"{working_directory}/.ngit/{br_name}/commits/info.txt", "r")
        num_other = f.readlines()[0].split()[-1]
        f.close()
        a = ""
        if num_master:
            a = f"{working_directory}/.ngit/master/commits/{num_master}"
        b = ""
        if num_other:
            b = f"{working_directory}/.ngit/{br_name}/commits/{num_other}"
        dif_of_br = find_diff_for_status(a, b)
        for i, elem in enumerate(dif_of_br):
            print(i, " : ", elem)
        dif = dif_of_br[1] + dif_of_br[2]    
        for i in dif:
            ex_code_14 = terminal(["rsync", "-rau"] + [f"{working_directory}/.ngit/{br_name}/commits/{num_other}/{i}"] + [working_directory + "/"], ret="ex")
            if ex_code_14:
                print("14 14 14", ex_code_14)  
        ngit_add(add_all=True)
        ngit_commit("for branch")


    else:
        print("brach not exists")



def time_equal(a, b):
    """Համեմատեւմ է ֆայլերի վերջին փոփոխության ժամանակները։ Օրինակ՝
    ["Մայ", "15", "18։05"] == ["Մայ", "15", "18։05"]"""
    if len(a) != 3 or len(b) != 3:
        return False
    i = 2
    while i >= 0:
        if a[i] != b[i]:
            return False
        i -= 1
    return True


def ret_dict_name_type_time(pth): # ognakan funkia, commiti meja ogtagorcvum
    """Վերադարձնում է dictionary հետևյալ ձևով`
    {անուն : [տիպ, վերջին փոփոխության ժամանակ(ամիս։օր։ժամ)]}"""
    types = ""
    if pth:
        types = ls_la(pth=f"{pth}")[1:]
    i = 0
    count = 0
    while i < len(types):
        if types[i][-3:] == " .." or types[i][-2:] == " ." or types[i][-6:] == " .ngit":
            del types[i]
            count += 1
            i -= 1
        i += 1
    dict = {}
    for i in types:
        spl = i.split()
        dict[spl[-1]] = spl[0][0], spl[-4:-1]

    return dict


def are_different(pth_1, pth_2):
    # import pdb; pdb.set_trace()

    addd = ret_dict_name_type_time(pth_1)
    comm_min_1 = ret_dict_name_type_time(pth_2)
    if len(addd) != len(comm_min_1):
        return True
    elif addd.keys() != comm_min_1.keys():
        return True
    else:
        for i in addd.keys():# Keys are equal
            if addd[i][0] == "-":
                if not time_equal(addd[i][1], comm_min_1[i][1]):
                    return True
            else:
                rett = are_different(pth_1 + "/" + i, pth_2 + "/" + i)# return ????
                if rett:
                    return rett
    return False            

def find_diff_for_status(pthh_1, pthh_2):

    appendes = []
    deletes = []
    modifies = []

    def foo(pth_1, pth_2, appnd = ""):

        dir_1 = ret_dict_name_type_time(pth_1)
        dir_2 = ret_dict_name_type_time(pth_2)

        dir_1_names = set(dir_1.keys())
        dir_2_names = set(dir_2.keys())

        deletes.extend([appnd + i for i in dir_2_names - dir_1_names])
        appendes.extend([appnd + i for i in dir_1_names - dir_2_names])

        for i in dir_1_names.intersection(dir_2_names):# Keys are equal
            if dir_1[i][0] == "-":
                if not time_equal(dir_1[i][1], dir_2[i][1]):# keys are equal
                    modifies.append(appnd + i)
            else:
                foo(pth_1 + "/" + i, pth_2 + "/" + i, appnd=appnd + i + "/")
        return 
    foo(pthh_1, pthh_2)
    return [appendes, deletes, modifies]


def ngit_commit(message=""):
    """Executng commit"""
    try:
        f = open(f"{working_directory}/.ngit/branch_info.txt", "r")
        branch = f.readlines()[1].split()[-1]
        f.close()
    except FileNotFoundError:
        branch = "master"
    
    f = open(f"{working_directory}/.ngit/{branch}/commits/info.txt", "r")
    ls = f.readlines()
    f.close()
    num = ls[0].split()[-1]
    num = str(int(num) + 1)
    terminal(["mkdir", f"{working_directory}/.ngit/{branch}/commits/{num}"])
    code = generate_code()

   

    def subfunc(commit_minus_1_path, current_path, commit_current_path):
        """Commit-ի հիմնական ֆունկցիա։ Առաջին commit-ի ժամանակ կլոնավորում է բոլոր ֆայլերը,
        երկրորդից սկսած ռեկուրսիվ կերպով անցնում է ֆայլային համակարգի բոլոր մակարդակնորով,
        նոր commit-ի մեջ կլոնավորում է միայն այն ֆայլերը, որոնք փոփոխության են ենթարկվել կամ չկան նախորդ commit֊ում,
        իսկ նմացած ֆայլերի վրա ստեղծում է hard link էր"""
        # commit_minus_1_path = commit num - 1
        # current_path = add
        # commit_corrent_path = commit current num

        commit_minus_1 = ret_dict_name_type_time(pth=commit_minus_1_path)
        current = ret_dict_name_type_time(pth=current_path)

        for i in current.keys():
            if current[i][0] == "-":# սիմվոլիկ լինքերը երևի պետք չի հաշվի առնել(== "l")
                if i in commit_minus_1.keys():
                    if time_equal(current[i][1], commit_minus_1[i][1]):
                        ex_code_1 = terminal(["ln", f"{commit_minus_1_path}/{i}", f"{commit_current_path}"], ret="ex")
                        if ex_code_1:
                            print(i, " -- ", ex_code_1, "  1")
                    else:
                        ex_code_2 = terminal(["rsync", "-a", f"{current_path}/{i}", commit_current_path], ret="ex")
                        if ex_code_2:
                            print(ex_code_2, "  2")

                else:# i not in commit_minus_1.keys()
                    ex_code_3 = terminal(["rsync", "-a", f"{current_path}/{i}", commit_current_path], ret="ex")
                    if ex_code_3:
                        print(ex_code_3, "  3")
            elif current[i][0] == "d":
                ex_code_4 = terminal(["mkdir", "-p", f"{commit_current_path}/{i}"], ret="ex")
                if ex_code_4:
                    print(ex_code_4, "  4")
                if i in commit_minus_1.keys():
                    subfunc(commit_minus_1_path + "/" + i, current_path + "/" + i, commit_current_path + "/" + i)
                else:
                    lst = ls_a(pth=f"{current_path}/{i}")
                    lst.remove(".")
                    lst.remove("..")
                    for j in lst:
                        ex_code_5 = terminal(["rsync", "-rua", f"{current_path}/{i}/{j}", f"{commit_current_path}/{i}"], ret="ex")
                        if ex_code_5:
                            print(ex_code_5, i, "  5")            

            

    can_append = False

    lst = ls_a(pth=f"{working_directory}/.ngit/{branch}/add")
    lst.remove(".")
    lst.remove("..")
    if num == "1":
        if lst:
            for i in lst:
                ex_code = terminal(["rsync", "-rua", f"{working_directory}/.ngit/{branch}/add/{i}", f"{working_directory}/.ngit/{branch}/commits/{num}/"], ret="ex")
                if ex_code:
                    print(ex_code)
                can_append = True
        else:
            print("You need to add something before commiting")        

    else:
        if are_different(pth_1=f"{working_directory}/.ngit/{branch}/add", pth_2=f"{working_directory}/.ngit/{branch}/commits/{str(int(num) - 1)}"):
            subfunc(f"{working_directory}/.ngit/{branch}/commits/{str(int(num) - 1)}", f"{working_directory}/.ngit/{branch}/add", f"{working_directory}/.ngit/{branch}/commits/{num}")   
            can_append = True
        else:
            # print("You need to type ngit add to add you changs before commiting")    
            print("First you need to change something, then type ngit add ...\n\
             to add what you changes and then type ngit commit -m \"some massege\"\
             to commit your changes ")    

    if can_append:  
        print("Chosen files are commited successfully") 
        with open(f"{working_directory}/.ngit/{branch}/commits/info.txt",'w') as f:
            ls.append(num + " " + code + " " + message + "\n")
            ls_0 = "Number of commits: " + num + ls[0][-1]
            ls[0] = ls_0
            f.writelines(ls)


        with open(f"{working_directory}/.ngit/{branch}/commits/commits_info.txt",'r+') as file:
            file.write("Num: " + "\t" + num + "\n") #    
            file.write("Code: " + "\t" + code + "\n") 
            file.write("Message: " + "\t" + message + "\n") 


def ngit_rm(file,wd=working_directory): # rm functiana fila jnjum
    path = os.path.join(wd,file)
    os.remove(path)

def ngit_rmdir(file,wd=working_directory): #rmdir function direcorya jnjum
    path = os.path.join(wd,file)
    os.rmdir(path)

def ls_tree(): # ls-tree cuyca talis im filer u directorianer
    proc = sb.Popen(["tree", "-a"], stdin=sb.PIPE, stdout=sb.PIPE, stderr=sb.PIPE, text=True)
    std_out, std_err = proc.communicate()
    proc.wait() 
    print(std_out)



def reg_name(user_name): #ngit --config user.name 
    return user_name

def reg_email(user_email): #ngit --config user.email
    return f"<{user_email}>"

name_user = ""
email_user = ""


def ngit_log():
    today = time.strftime("%A\t%B\t%D\t%I:%M:%S")
    print("HEAD -> ",os.getlogin().title(), "Origin/"+os.getlogin())
    print("--------------Author------------------------")
    with open(f"{working_directory}/.ngit/{branch}/commits/user_contact.txt",'r') as file:
        print(file.read())

    print("Date: ",today)
    print()
    print("----------------Your Data-------------------")
    with open(f"{working_directory}/.ngit/{branch}/commits/commits_info.txt",'r') as file:
        print(file.read())

def start_if():

    global name_user, email_user
    if len(sys.argv) > 1:

        file_remove = "" # file anunem talis vor jnji
        directory_remove = "" # papki anunem talis vor jnji

        if sys.argv[1] == "--version":
            print("ngit version is 1.0.0")

        elif sys.argv[1] == "--help": #ete eli functtion lini add kaneq
            print("These are common Ngit commands used in various situations:")
            print()
            print("Start a working area (see also: ngit help tutorial)")
            print("""
            clone     Clone a repository into a new directory      
            init      Create an empty Git repository or reinitialize an existing one

    Work on the current change (see also: ngit help everyday)
            add       Add file contents to the index
            rm        Remove files from the working tree and from the index
            log       Show commit logs
            rmdir     Remove directory

    Grow, mark and tweak your common history
            branch    List, create, or delete branches
            commit    Record changes to the repository
            tag       Create, list, delete or verify a tag object signed with GPG
            merge     Join two or more development histories together
            rebase    Reapply commits on top of another base tip
            """)

        elif sys.argv[1] == "init":
            if ".ngit" in terminal(["ls", "-a", working_directory]):
                print("You already have initialized!")
            else:
                ex_code = terminal(["cp", "-r", f"{ngit_working_directory}/.ngit", working_directory], ret="ex")
                if not ex_code:
                    print("Initialized empty ngit repository in " + working_directory)
                else:
                    print("Exit code of init:", ex_code)





        elif ".ngit" in terminal(["ls", "-a", working_directory]):
            if sys.argv[1] == "add":
                if len(sys.argv) == 2 or sys.argv[2] == ".":
                    ngit_add(add_all = True)
                else:
                    ngit_add(sys.argv[2:])

            elif sys.argv[1] == "commit":
                if sys.argv[2] == "-m" and len(sys.argv) == 4:
                    ngit_commit(sys.argv[3])

            elif sys.argv[1] == "status":
                ngit_status()  

            elif sys.argv[1] == "branch":
                if len(sys.argv) > 2 and len(sys.argv) == 3:
                    ngit_new_branch(sys.argv[2])
                else:
                    ngit_branch()    

            elif sys.argv[1] == "checkout":
                if len(sys.argv) > 2 and len(sys.argv) == 3:
                    ngit_checkout(sys.argv[2])
                else:
                    print("You need to type branch name after ngit checkout")
            
            elif sys.argv[1] == "merge":
                if len(sys.argv) > 2 and len(sys.argv) == 3:
                    ngit_merge(sys.argv[2])
                else:
                    print("You need to type branch name after ngit merge")    



            elif sys.argv[1] == "rm":         ## file jnjela jishta ashxatum
                try:
                    file_remove = sys.argv[2]
                    if sys.argv[2] == file_remove:
                        ngit_rm(file_remove,working_directory)
                except IndexError:
                    print("Please ask file name!")
                    print("Not Found: File")
                except OSError as error:
                    print(error)
                    print("Don't removed Directory:")

            elif sys.argv[1] == "rmdir":
                try:
                    directory_remove = sys.argv[2]
                    if sys.argv[2] == directory_remove:
                        ngit_rmdir(directory_remove,working_directory)
                except IndexError:
                    print("Please ask Directory name!")
                    print("Not Found: Directory")
                except OSError as error:
                    print(error)
                    print("Don't removed File")

            elif sys.argv[1] == "ls-tree":  
                ls_tree()

            elif sys.argv[1] == "--config" and sys.argv[2] == "user.name":
                try:
                    name_user = sys.argv[3]
                    if sys.argv[3] == name_user:
                        reg_name(name_user)
                        with open(f"{working_directory}/.ngit/{branch}/commits/user_contact.txt",'a') as file:
                            file.write(sys.argv[3] + "\n")
                except:
                    print("---------ERROR-----------")
                    print("Enter Your UserName!")
                    reg_name("")

            elif sys.argv[1] == "--config" and sys.argv[2] == "user.email":
                try:
                    email_user = sys.argv[3]
                    if sys.argv[3] == email_user:
                        reg_email(email_user)
                        with open(f"{working_directory}/.ngit/{branch}/commits/user_contact.txt",'a') as file:
                            file.write(sys.argv[3] + "\n")
                except:
                    print("---------ERROR-----------")
                    print("Enter Your UserName!")
                    reg_email("")

            elif sys.argv[1] == "log":
                ngit_log()

            elif sys.argv[1] == "init":
                pass    

            else:
                print(f"ngit: {sys.argv[1]} is not a ngit command. See 'ngit --help'.")
    else:# Ստեղ պետքա գրել նգիթի նկարագրությունը
        print("Type ngit --help for more information")

if __name__ == "__main__":
    start_if()
