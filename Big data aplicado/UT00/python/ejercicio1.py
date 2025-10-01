num = input("Dame un numero")
num_int = int(num)
while type(num_int) != int:
    num = input("Dame un numero válido")
    num_int = int(num)  
else:
     print ("grasia x el numero amico")
