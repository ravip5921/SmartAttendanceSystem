import json
import socket
import server.communication_json as communication_json

attendance_server = {'host': '127.0.0.1', 'port': 60000}
#attendance_server = {'host': '192.168.152.108', 'port': 60000}
#attendance_server = {'host': '192.168.1.65', 'port': 60000}
SERVER_TIMEOUT = 30 #timeout after 20 seconds if server didn't respond


def markAttendance(student_id, acode, face_embd, _attendance_server=attendance_server):
    data = {}
    data['sid'] = student_id
    data['acode'] = int(acode)
    data['face'] = [float(x) for x in face_embd]
    #convert the data to be sent into json format
    datastr = communication_json.convert2send(data)
    #print(datastr)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(SERVER_TIMEOUT)
        sock.connect((attendance_server['host'], attendance_server['port']))
        # print("zxc ")
        try:
            #sending attendance start data to server
            sock.sendall(datastr)
            # print("zxc 2")
            #receive response which is byte representing attendance done or not
            response = communication_json.readall(sock)
            if "error" in response:
                # print(response['error'])
                return response
            elif "success" in response:
                # print(response['success'])
                return response #response contains 
        except TimeoutError as t:
            raise
        except:
            return {'error': 'error sending/receiving data'}
        finally:
            sock.close()
    except TimeoutError as t:
    	return{'error':'Server took long to respond'}
    except:
        return {'error': 'server not avialable'}

if __name__ == '__main__':
##    markAttendance('075bct052', '88', 
##                 [0.258, 0.444447, 0.1258, 0.36697, 0.125887, 0.11245588])
    input()
