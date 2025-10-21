print("\033c\033[43;30m\n")
files="stock.csv"
def menu():
    value="""0...add
1...list
2...report
3...exit"""
    print(value)
    a=input().strip()
    return int(a)
def adds():
    print("id entry number?")
    a=input().replace(",",";")
    print("id product?")
    b=input().replace(",",";")
    print("units?")
    c=input().replace(",",";")
    a=a+","+b+","+c+"\n"
    f1=open(files,"a")
    f1.write(a)
    f1.close()
def lists():
    f1=open(files,"r")
    a=f1.read()
    f1.close()
    print("\033c\033[43;30m\n")
    print(a)
def reports():
    f1=open(files,"r")
    a=f1.read()
    f1.close()
    b=a.split("\n")
    a=""
    print("\033c\033[43;30m\n")
    print("find wat?")
    c=input()
    for d in b:
        f=d.find(c)
        if f>-1:
            print(d)
w=True
while w:
    a=menu()
    if a==0:
        adds()
    if a==1:
        lists()
    if a==2:
        reports()
    if a>2:
        break