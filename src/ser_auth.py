# import dependency(s)
import time
import serial

uart_message = "read_id"

# class to detect arduino identity
def ser_node(port_number, tty_name, uart_baudrate):
    with serial.Serial("/dev/{}{}".format(tty_name, port_number), uart_baudrate, timeout=1) as checked_port:
        
        # wait serial com to open
        time.sleep(0.25)
        print("Check node module in {}".format(checked_port.port))

        # if serial com is open, send message to get the node id
        if checked_port.isOpen():
            print("Node in {} is connected".format(checked_port.port))
            print("Check Node identity at {}".format(checked_port.port))
            check_message = ("{}\n".format(uart_message))
            
            time.sleep(3)

            # send message to node
            checked_port.flushInput()
            checked_port.write(check_message.encode('utf-8'))

            # wait for node's response
            while checked_port.inWaiting()==0: pass

            if checked_port.inWaiting():
                # get node id
                answer = checked_port.readline()
                decode_answer = answer.decode('utf-8').rstrip()
                checked_port.flushInput()
            
        else:
            print("{} is not connected".format(checked_port.port))

    # send node id to main program
    return decode_answer
