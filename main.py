import socket
import paho.mqtt.client as mqtt
import time
import os
import cv2
import struct
import sys


mqtt_host = 'PNC6FJ41FE.iotcloud.tencentdevices.com'  #mqtt服务器ip
mqtt_port = 1883   #mqtt连接端口
socket_host = '0.0.0.0'  #socket服务器ip
socket_port =  10000   #socket连接端口
#CLIENT_ID = 'PNC6FJ41FElh'  #mqtt存储端ID
topic = 'PNC6FJ41FE/lh/event'      #主题名
message1 = 1
a = 0

def get():
    mqtt_client = mqtt.Client('PNC6FJ41FElh')
    mqtt_client.username_pw_set('PNC6FJ41FElh;12010126;03BJD;1672553636','a4692c8f9601b2ee6dbb1c29c31aa8192fd79c1c93c91bc605e98e1853679fc0;hmacsha256')
    mqtt_client.connect(mqtt_host)
    mqtt_client.publish(topic,message1)
    socket_server(a)

def socket_server(a):
    a = a + 1
    mkpath = "./{}".format(a)
    mkdir(mkpath)
    socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #socket TCP创建对象
    socket_client.bind((socket_host,socket_port))  #绑定socket通信端口
    socket_client.listen(50)         #最大监听量
    time_e = int(time.time())        # 这里时间戳用来命名图片文件
    zz = 0                            # 当前时间戳的第N帧
    num = 0       # 总帧数,此次为测试,可具体参考帧数来设置（我测试的效果大概为每秒6帧,录制20s,所以达到120张照片停止循环）
    print("等待图片数据")
    conn, addr = socket_client.accept()
    print('-1')
    while True:
        try:
            # 接收的数据大小,建议比图片本身大,不然无法传输
            #fileinfo_size = struct.calcsize('128sl')
            buf = conn.recv(10000)
            print('0')
            if buf != b'stop':
                print('1')
                #filesize = buf
                # 每次检查时间戳
                time_b = int(time.time())
                # 每次循环帧数加1
                zz = zz + 1
                # 如果时间戳+1秒,则帧数序号归零
                if time_b != time_e:
                    time_e = time_b
                    zz = 0
                # 存储图片
                file_name = str(time_e) + str(zz) + '.jpg'
                #filename, filesize = struct.unpack(file_name, buf)
                #fn = file_name.strip('\000')
                new_filename = os.path.join('./{}'.format(a) + file_name)
                print('3')
                fp = open(new_filename, 'wb')
                print('start receiving...')
                fp.write(buf)
                print('send over')
                shutil.copyfile(file_name, '{}/{}'.format(a, file_name))
                os.remove('{}'.format(file_name))
                buf = 0
                '''
                write = 0
                while not recvd_size == filesize:
                    write = 1
                    if filesize - recvd_size > 1024:
                        data = socket_client.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = socket_client.recv(filesize - recvd_size)
                        recvd_size = filesize
                        fp.write(data)'''
                num = num + 1  # 总帧数
            if buf == b'stop':
                fps = 6  # 保存视频的FPS
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                videoWriter = cv2.VideoWriter('{}.mp4'.format(a), fourcc, fps, (384, 288))
                # 图片地址
                imgs = glob.glob('{}/*.jpg'.format(a))
                for imgname in imgs:
                    frame = cv2.imread(imgname)
                    videoWriter.write(frame)
                videoWriter.release()
                print("转换mp4完成")
                break
        except:
            pass


def mkdir(path):
    path = path.strip()# 去除首位空格
    path = path.rstrip("\\") # 去除尾部 \ 符号
    isExists = os.path.exists(path) #判断是否存在文件
    if not isExists:
       os.makedirs(path) #创建文件夹
    if isExists:
       os.removedirs(path)
       os.makedirs(path)





if __name__ == '__main__':
    get()
