import receive_data
#import send_data
import time
from get_rain import get_rain

memoria_estat = 0
freq = 5

def split_string(frase): ## Format de raw data => b'232;452;0\r\n'

    frase=frase[2:11] ## Substring format de raw data => 232;452;0
    split_data = frase.split(";") ## Split de l'string en una llista [Data1, Data2, Data3]
    
    return split_data

def data_construction(llista, poble, fruita): ## Format de la llista + dades
    var1 = str(int(llista[0])/10)
    var2 = str(int(llista[1])/10)
    var3 = llista[2]
    var4 = poble
    var5 = fruita

    data_dict={
        "temperatura":  var1,
        "humitat":      var2,
        "status":       var3,
        "ubi":        var4,
        "fruit":       var5}
    
    return data_dict

def send_data(ordre):
    import serial 
    import time
    
    SerialObj = serial.Serial('/dev/ttyACM0') # COMxx  format on Windows
                    # ttyUSBx format on Linux
    SerialObj.baudrate = 115200  # set Baud rate to 9600
    SerialObj.bytesize = 8   # Number of data bits = 8
    SerialObj.parity  ='N'   # No parity
    SerialObj.stopbits = 1   # Number of Stop bits = 1
    time.sleep(3)

    if ordre == "S":
        SerialObj.write(b'S')    #transmit 'S' (8bit) to micro/Arduino
    elif ordre == "N":
        SerialObj.write(b'N')    #transmit 'N' (8bit) to micro/Arduino

    print(ordre)

    SerialObj.close()      # Close the port


poble =input("Entra la teva ubicació: ")
fruita = input("Entra la tipologia de conrreu: ")


while True: 
    
    ################# TIMER #################

    start_time = time.time() # Hora inici temporitzador
    ref = 0.0
    segons = 0

    while True:  # Per assegurar-nos que les dades d'Arduiono es reben correctament
        temps_actual=round((time.time()-start_time), 1) # Cálcul del temps actual des de l'hora d'inicic, funció de temporització. 
        temp = temps_actual-ref

        if temp==1.0:
            ref+=1
            segons+=1

        if segons == 2:
            break


    ################# Recepció de les dades #################

    raw_data = str(receive_data.ReceivedString) # Crida de la funció per fer la petició de dades a arduino. 


    ################# Tractament de les dades #################

    split_data =split_string(raw_data) # Crida de la funció per splitejar les dades en un format entenedor. 

    ################# Construcció del diccionari #################

 

    data_dict = data_construction(split_data,poble,fruita) # Crida de la funció per construir el diccionari de dades. 
    print(data_dict)

    memoria_estat = data_dict["status"]
    


    ################# Resposta de l'status #################

    
    response = get_rain(data_dict)
    status=int(response["status"])

    
    
    if status != memoria_estat and status ==1: 
        send_data.ordre = "S"
        print("#### REGANT ####")

    elif status != memoria_estat and status == 0:
        send_data.ordre = "N"
        print("#### NO REGANT ####")


################# TEST FLIP FLOP STATUS #################

   # if status ==1 and memoria_estat%2 ==0: 
        #send_data(ordre = "S")

    #elif status ==1 and memoria_estat%2 != 0:
        #send_data(ordre = "N")

    #memoria_estat+=1
    #print(memoria_estat)



    time.sleep(freq)

    

















