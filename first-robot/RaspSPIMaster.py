import spidev

def list_int_to_bytes(input_list):
    # Split list int values to list ready for transfer by SPI
    # every value from -32768 to 32767
    # will be replaced two values from -255 to 255
    # Original values must be collected by Arduino after transfer 
    output_list = []
    for int_data in input_list:
        output_list.append(int_data >> 8)
        output_list.append(int_data & 255)
    return output_list


def spi_send(txData):
    # Send and recieve 40 bytes
    N = 40
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1000000
    txData = list_int_to_bytes(txData)
    txData = txData+[0]*(N-len(txData))
    rxData = []
    _ = spi.xfer2([240])  # 240 - b11110000 - start byte
    for i in range(40):
        rxData.append(spi.xfer2([txData[i]])[0])
    spi.close()
    return rxData


send_data = [1,-1,1,256,-256,1]+[240]*12 #Not more then 20 value from -32768 to 32767
recieved_data = spi_send(send_data)
print(recieved_data)
