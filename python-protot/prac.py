def power(base:float, exponent: int)->float:
    result =1
    for _ in range(abs(exponent)):
            result*=base
    if result>2147483647 : 
        print("over maximum int!!!")
        exit()
    elif exponent<0:
        return 1/result
    else:
        return result
    
def main():
    try:
        base=float(input("Put the base number in:"))
    except:
        print("Invalid Input!")
        exit()
    try:
        exponent=int(input("Put the exponent in:"))
    except:
         print("Invalid Input!")
         exit()
    print(power(base,exponent))

if __name__=="__main__":
     main()

