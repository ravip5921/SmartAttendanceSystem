import json
import socket
from typing import final
from server import communication_json

#from communication_json import convert2send, readall

ATTENDANCE_SERVER = {'host': '127.0.0.1', 'port': 60001}
#ATTENDANCE_SERVER = {'host': '192.168.1.65', 'port': 60001}
#ATTENDANCE_SERVER = {'host': '192.168.152.108', 'port': 60001}
SERVER_TIMEOUT = 30 #timeout after 20 seconds if server didn't respond

def sendAttendanceData(teacher_id, class_id, subject_code, attendance_request, attendance_server, student_id = None):
    data = {}
    if teacher_id != None:
        data['tid'] = teacher_id
    if class_id != None:
        data['cid'] = class_id
    if subject_code != None:
        data['scode'] = subject_code
    if student_id != None:
        data['sid'] = student_id
    data['attendance'] = attendance_request
    #convert the data to be sent into json format
    datastr = communication_json.convert2send(data)
    #print(datastr)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(SERVER_TIMEOUT)
        sock.connect((attendance_server['host'], attendance_server['port']))
        try:
            #sending attendance start data to server
            sock.sendall(datastr)
            #receive response which is byte representing attendance done or not
            response = communication_json.readall(sock)
            if "error" in response:
                print(response['error'])
                return response
            else:
                # response contains {'student_list': list of students(id, name) for this class, 'acode':attendance code}
                return response
        except TimeoutError as t:
    	    raise
        except:
            return {'error': 'error sending data'}
        finally:
            sock.close()
    except TimeoutError as t:
    	return{'error':'Server took long to respond'}
    except:
        return {'error': 'server not avialable'}


def startAttendance(teacher_id, class_id, subject_code):
    response = sendAttendanceData(
        teacher_id, class_id,subject_code, 'start',ATTENDANCE_SERVER)
    return response


def getAttendance(teacher_id, class_id, attendance_server=ATTENDANCE_SERVER):
    # doesn't require subject to be specified to get attendance
    response = sendAttendanceData(
        teacher_id, class_id, None, 'get', attendance_server)
    return response

def markAttendance(teacher_id, class_id, student_id, attendance_server=ATTENDANCE_SERVER):
    #explicitly mark a student as present
    response = sendAttendanceData(
        teacher_id, class_id, None, 'mark', attendance_server, student_id)
    return response

def stopAttendance(teacher_id, class_id, attendance_server=ATTENDANCE_SERVER):
    # doesn't require subject to be specified to close attendance
    response = sendAttendanceData(
        teacher_id, class_id, None, 'end', attendance_server)
    return response


def updateClassAndSubjects(teacher_id, attendance_server=ATTENDANCE_SERVER):
    response = sendAttendanceData(
        teacher_id, None, None, 'update', attendance_server)
    return response


# if __name__ == '__main__':
#     #start attendance
#     startAttendance('bct12', 'bctcd', 'mp')
#     #wait some time
#     #get realtime attendance ststus
#     getAttendance('bct12', 'bctcd')
#     #stop attendance
#     stopAttendance('bct12', 'bctcd')
#     input()
