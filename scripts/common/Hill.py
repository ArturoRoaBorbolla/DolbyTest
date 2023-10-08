import numpy as np 

Cadena = input("Escribe una cadena: ")

Div=[]
for i in range(0,len(Cadena),3):
    Div.append(Cadena[i:i+3])
Wrapping = [ [ord(Charactes) for Charactes in Wrappedtext] for Wrappedtext in Div] 
Alfabeto = {ord(Character) : Character  for Character in Cadena}
Alfabeto.update({-1:''})
Encoded_Comp=[]
Decode_Text=[]
for A in Wrapping:
    if len(A) < 3:
        for i in range(3-len(A)):
            A.append(-1)
    print("Vector de letras: ",A)
    A=np.asarray(A)
    M=np.asanyarray([[1,2,3],[5,5,6],[8,8,9]])
    Encoded= [Line_Encoded.sum() for Line_Encoded in A*M]
    Encoded_Comp+= Encoded
    #Decoded = [round(Line_Decoded.sum())  for Line_Decoded in Encoded*np.linalg.inv(M)]
    #Decode_Text=[Alfabeto[letra] for letra in Decoded]
    print("Array a encriptar: ",A)
    print("Vector por Matriz:  ({A*M})")
    print("Texto codificado: ",Encoded)
    print("Texto decodificado: ",Decode_Text)
print("Texto Completo: ",Encoded_Comp)


