import sys
try:
    shell_connect = sys.stdout.shell
    kk=1
except AttributeError:
    kk=0

colormap = {"red": "COMMENT",
                "orange": "KEYWORD",
                "green": "STRING",
                "blue": "stdout",
                "purple": "BUILTIN",
                "black": "SYNC",
                "brown": "console",

                "user1": "DEFINITION",
                "user2": "sel",
                "user3": "hit",
                "user4": "ERROR",
                "user5": "stderr"}
def print_Red(text):
    if(kk):
        return shell_connect.write(text, colormap["user5"])
    else:
        print(text)
def print_user3(text):
    if(kk):
        return shell_connect.write(text, colormap["user3"])
    else:
        print(text)
def print_green(text):
    if(kk):
        return shell_connect.write(text, colormap["green"])
    else:
        print(text)
def print_orange(text):
    if(kk):
        return shell_connect.write(text,colormap["orange"])
    else:
        print(text)



def get_subnetmask(prefix_length):
    subnetmask_binary=["1"]*prefix_length+["0"]*(32-prefix_length)
    subnetmask_binary=[subnetmask_binary[i:i+8] for i in range(0,32,8)]
    s=[]
    for i in range(len(subnetmask_binary)):
        s1="".join(subnetmask_binary[i])
        s.append(str(int(s1,2)))
    subnetmask=".".join(s)
    return subnetmask

def add(list1,n):
    k=n+list1[3]
    k1=k//256
    k2=k%256
    list1[3]=k2
    list1[2]+=k1
    if(list1[2]>255):
        k1=list1[2]//256
        k2=list1[2]%256
        list1[2]=k2
        list1[1]+=k1
    return list1


def get_class(a):
    if   (a < 128):
        b= 'A'
    elif(a < 192) :
        b= 'B'
    elif(a < 224) :
        b= 'C'
    return b

def check_id(a,prefix_length,ip,w):
    k=1
    l=["C","B","A"]
    if (len(ip) == 4) and (1 <= int(ip[0]) <= 223) and (int(ip[0]) != 127) and (int(ip[0]) != 169 or int(ip[1]) != 254) and (0 <= int(ip[1]) <= 255 and 0 <= int(ip[2]) <= 255 and 0 <= int(ip[3]) <= 255):  
        if(get_class(a)=="A"):
            ip[3]=0 ; ip[2]=0 ; ip[1]=0
            if( prefix_length>=16):
                print_user3("You entered A class network id instead of {} class network id\n".format(l[w]))
                print_Red("* * * wasting several ips * * *\n")
                ip[3]=0 ; ip[2]=0 ; ip[1]=0
                k=0
        elif(get_class(a)=="B"):
            ip[2]=0 ; ip[3]=0
            if(prefix_length<16):
                print_user3("You entered B class network id instead of {} class network id\n".format(l[w]))
                print_Red("* * Cannot subnet this using network id you entered * *")
                k=0
            elif(prefix_length>=24):
                print_user3("You entered B class network id instead of {} class network id\n".format(l[w]))
                print_Red("* * * wasting several ips * * *\n")
                k=0
        elif(get_class(a)=="C"):
            ip[3]=0
            if(prefix_length <24):
                print("You entered C class network id instead of {} class network id".format(l[w]))
                print_Red("* * * wasting several ips * * *\n")
                k=0
    else:
        k=0
        print_Red("Network id you entered is not valid\n")
    return k,ip


def Prefix_Length(Req):
    h=1
    while(2**h<Req+2):
        h+=1
    return (32-h)




def print_networks(prefix_length,ip,subnetmask,x):
    Hosts=2**(32-prefix_length)
    Networks=2**(prefix_length%8)
    print("Prefix_Length",prefix_length)
    print("Subnet_Mask :",subnetmask)#"/",prefix_length)
    print("Hosts :",Hosts)
    print("Networks :",Networks)
    if(x==1):
        Current_Network(ip,prefix_length)
    print_orange("Do you want print all networks (y or n) ")
    while(1):
        w=input()
        if(w=="y"):
            for i in range(Networks):
                print("\nNetwork : ",i+1)
                ip=print_N(ip)
            break
        elif(w=="n"):
            print(" Thank you... ")
            break
        else:
            print_red("You must enter y or n\n")
            print_orange("Do you want print all networks (y or n)")


def print_N(ip):
    c=ip.copy()
    new_subnetmask=add(c,1)
    print("                          Network id : ",".".join(map(str,ip)))
    print("                          First usable ip : ",".".join(map(str,new_subnetmask)))
    new_subnetmask=add(c,2**(32-prefix_length)-3)
    print("                          Last usable ip : ",".".join(map(str,new_subnetmask)))
    new_subnetmask=add(new_subnetmask,1)
    print("                          Broadcast id : ",".".join(map(str,new_subnetmask)))
    new_subnetmask=add(new_subnetmask,1)
    ip=new_subnetmask
    return ip


def Current_Network(l,x):
    ip_bin=""
    ip_bin='0'*(10-len(bin(int(l[0]))))+bin(int(l[0])).replace("0b","")+'0'*(10-len(bin(int(l[1]))))+bin(int(l[1])).replace("0b","")+'0'*(10-len(bin(int(l[2]))))+bin(int(l[2])).replace("0b","")+'0'*(10-len(bin(int(l[3]))))+bin(int(l[3])).replace("0b","")
    net_Id=ip_bin[:x]+((32-x)*'0')
    brd_Id=ip_bin[:x]+((32-x)*'1')
    first_IP=ip_bin[:x]+((31-x)*'0')+'1'
    last_IP=ip_bin[:x]+((31-x)*'1')+'0'
    print("\nCurrent_Network")
    print("Network id :"+str(int("0b"+net_Id[:8],2))+"."+str(int("0b"+net_Id[8:16],2))+"."+str(int("0b"+net_Id[16:24],2))+"."+str(int("0b"+net_Id[24:32],2)))
    print("First usable ip :"+str(int("0b"+first_IP[:8],2))+"."+str(int("0b"+first_IP[8:16],2))+"."+str(int("0b"+first_IP[16:24],2))+"."+str(int("0b"+first_IP[24:32],2)))
    print("Last usable ip :"+str(int("0b"+last_IP[:8],2))+"."+str(int("0b"+last_IP[8:16],2))+"."+str(int("0b"+last_IP[16:24],2))+"."+str(int("0b"+last_IP[24:32],2)))
    print("Broadcast id :"+str(int("0b"+brd_Id[:8],2))+"."+str(int("0b"+brd_Id[8:16],2))+"."+str(int("0b"+brd_Id[16:24],2))+"."+str(int("0b"+brd_Id[24:32],2)))
    print("")

print("Choices :\n1. FLSM\n2. VLSM\n3. Using prefix length\n4.Using Subnet mask\nenter your choice (1/2/3/4)")
while(1):
    choice=input()
    if(choice=="1"):
        print_green("You have choosen subnetting using FLSM\n")
        print("enter the Requirement of ips: ")
        while(1):
            try:
                Requirement=int(input())
                if(Requirement<255):
                    print("Enter any C class Network id (192<->223): ",end="")
                    p1=0
                elif(Requirement<65535):
                    print("Enter any B class Network id (128<->191): ",end="")
                    p1=1
                else:
                    print("Enter any A class Network id (1<->127): ",end="")
                    p1=2
                while(1):
                    try:
                        ip=list(map(int,input().split(".")))
                        prefix_length=Prefix_Length(Requirement)
                        j,ip=check_id(ip[0],prefix_length,ip,p1)
                        if(j):
                            subnetmask=get_subnetmask(prefix_length)
                            print_networks(prefix_length,ip,subnetmask,0)
                            break
                        else:
                            print("Please... enter the new Network id")
                    except ValueError:
                        print_Red("*** error ***\nCheck the format of ip you entered\n")
                        print("Please... enter the new Network id")
                break
            except ValueError:
                print_Red("*** error ***\nCheck the Requirement you entered (It must be integer )\n")
                print("Please... enter the new Requirement : ",end="")
    elif(choice=="2"):
        print_green("You have choosen subnetting using VLSM\n")
        print("Enter the requirements in descending order : ",end="")
        while(1):
            try:
                Requirement=list(map(int,input().split()))
                Requirement=sorted(Requirement)[::-1]
                s=sum(Requirement)
                if(s<255):
                    print("Enter any C class Network id (192<->223): ",end="")
                    p1=0
                elif(s<65535):
                    print("Enter any B class Network id (128<->191): ",end="")
                    p1=1
                else:
                    print("Enter any A class Network id (1<->127): ",end="")
                    p1=2
                while(1):
                    try:
                        ip=list(map(int,input().split(".")))
                        prefix_length=Prefix_Length(s)
                        j,ip=check_id(ip[0],prefix_length,ip,p1)
                        if(get_class(ip[0])=="A"):
                            ip[3]=0;ip[2]=0;ip[1]=0
                        elif(get_class(ip[0])=="B"):
                            ip[3]=0;ip[2]=0
                        elif(get_class(ip[0])=="C"):
                            ip[3]=0
                        if(j):
                            for i in range(len(Requirement)):
                                prefix_length=Prefix_Length(Requirement[i])
                                print("\nPrefix_Length",prefix_length)
                                print("Subnet_Mask :",get_subnetmask(prefix_length))
                                print("Hosts :",2**(32-prefix_length))
                                print("Networks :",2**(prefix_length%8))
                                print("\nNetwork : ",i+1)
                                ip=print_N(ip)
                            break
                        else:
                            print("Please... enter the new Network id")
                    except ValueError:
                        print_Red("*** error ***\nCheck the format of ip you entered\n")
                        print("Please... enter the new Network id")
                break
            except ValueError:
                print_Red("*** error ***\nCheck the Requirement you entered (It must be integer )\n")
                print("Please... enter the new Requirements : ",end="")
             
    elif(choice=="3"):
        print_green("You have choosen subnetting using prefix length\n")
        print("enter an Network id  # for example: 172.20.10.0/17 ")
        while(1):
            try:
                p=input()
                s=0
                a=list(map(str,p.split("/")))
                s=1
                ip=list(map(int,a[0].split(".")))
                s=2
                prefix_length=int(a[1])
                if(prefix_length>23):
                    p1=0
                elif(prefix_length>15):
                    p1=1
                else:
                    p1=2
                j,ip=check_id(ip[0],prefix_length,ip,p1)
                if(j):
                    subnetmask=get_subnetmask(prefix_length)
                    print_networks(prefix_length,ip,subnetmask,1)
                    break
                else:
                    print("Please... enter the new Network id")
            except ValueError:
                if(s==0):
                    print_Red(" *** error ***\nCheck the format of _input_ you entered\n")
                elif(s==1):
                    print_Red(" *** error ***\nCheck the format of ip you entered\n")
                elif(s==2):
                    print_Red(" *** error ***\nCheck the prefix length you entered (It must be Integer)\n")
                print("Please... enter the new Network id")
    elif(choice=="4"):
        print_green("You have choosen subnetting using subnetmask\n")
        print("enter an Network id   # for example: 172.20.10.0 255.255.255.240")
        while(1):
            try:
                p=input()
                if(p.count(".")==6):
                    s=0
                    ip,subnetmask=map(str,p.split(" "))
                    s=1
                    ip=list(map(int,ip.split(".")))
                    ip[3]=0
                    s=2
                    x=subnetmask.split(".")
                    subnetmask_binary=bin(int(x[0]))[2:]+bin(int(x[1]))[2:]+bin(int(x[2]))[2:]+bin(int(x[3]))[2:]
                    prefix_length=subnetmask_binary.count("1")
                    if(prefix_length>23):
                        p1=0
                    elif(prefix_length>15):
                        p1=1
                    else:
                        p1=2
                    j,ip=check_id(ip[0],prefix_length,ip,p1)
                    if(j):
                        print_networks(prefix_length,ip,subnetmask,1)
                        break
                    else:
                        print("Please... enter the new Network id")
                else:
                    print_Red(" *** error ***\nCheck the format of ip you entered\n")
                    print("Please... enter the new Network id")
            except ValueError:
                if(s==0):
                    print_Red(" *** error ***\nCheck the format of _input_ you entered\n")
                elif(s==1):
                    print_Red(" *** error ***\nCheck the format of ip you entered\n")
                elif(s==2):
                    print_Red(" *** error ***\nCheck the format of subnetmask you entered\n")
                print("Please... enter the new Network id")
    else:
        print_Red("choice must be among 1/2/3/4\n")
        print("Please... enter your new choice")
    


            


            
