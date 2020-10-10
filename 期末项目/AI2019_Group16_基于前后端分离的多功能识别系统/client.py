# coding=gbk
from tkinter import *
from socket import *
from tkinter.filedialog import askopenfilename
import os
import re
import cv2
import numpy as np
from tkinter import messagebox
HOST = '127.0.0.1'
PORT = 19225
BUFSIZ = 1024
ADDR = (HOST, PORT)


class FaceDetect:
 def __init__(self):
  window=Tk()
  window.title("FaceDetect")
  self.text=Text(window,width=100,height=20)
  self.text.pack()
  self.Var=StringVar()
  frame1=Frame(window)
  frame1.pack()
  Label(frame1,text="Select a picture:").grid(row=1,column=1,sticky=W)
  e=Entry(frame1,textvariable=self.Var,width=40)
  e.grid(row=1,column=2)
  Button(frame1,text="���",command=lambda:self.processBrowse(e)).grid(row=1,column=3)
  Button(frame1,text="ȷ�Ϸ���",command=lambda:self.processDelivery(e)).grid(row=1,column=4)
  Button(frame1,text="�����",command=self.processResult).grid(row=1,column=5)
  window.mainloop()
 
 def processBrowse(self,e):
  e.delete(0,END)
  m=askopenfilename()
  e.insert(0,m)

 def processDelivery(self,e):
  self.filename=e.get()
  if os.path.exists(self.filename)==0: 
   messagebox.showinfo("Tip","The file is not exist!")
   return 0
  elif re.search('\.jpg',self.filename) is None:
   messagebox.showinfo("Tip","The file is not picture.jpg!")
   return 
  tcpCliSock = socket(AF_INET, SOCK_STREAM)
  tcpCliSock.connect(ADDR)
  tcpCliSock.send('����ͼƬmode'.encode())
  if tcpCliSock.recv(BUFSIZ).decode()=='OK':
   self.text.insert(INSERT,'׼������ͼƬ\n')
  myfile = open(self.filename, 'rb')
  data = myfile.read()
  size = str(len(data))
  tcpCliSock.send(size.encode())
  rec = tcpCliSock.recv(BUFSIZ).decode()
  tcpCliSock.send(data)
  if tcpCliSock.recv(BUFSIZ).decode()=='OK':
   self.text.insert(INSERT,'����ͼƬ���\n')
  tcpCliSock.close()

 def processResult(self):
  # ���͹���ģʽ�������
  tcpCliSock = socket(AF_INET, SOCK_STREAM)
  tcpCliSock.connect(ADDR)
  tcpCliSock.send('����ʶ��mode'.encode())
  # ���ܵ�����˷�������Ϣ
  rec = tcpCliSock.recv(BUFSIZ).decode()
  # �ж�û���������
  if rec=='No face':
   tcpCliSock.close()
   messagebox.showinfo("Tip","No face in the picture!")
  # ���������
  else:
   # ȥ��','�γ��б�
   list=rec.split(',')
   tcpCliSock.close()
   # ʹ��opencv����ͼƬ
   img = cv2.imdecode(np.fromfile(self.filename,dtype=np.uint8),-1)
   vis = img.copy()
   # ����ÿ������7���������ֱ��Ǿ��ο����Ͻǵ�����(l,t)�����ο�ĸ�h�Ϳ�w��������Ӧ���Ա����䡢��ֵ�÷�
   # forѭ�������Զ�����len(list)/7ȷ������
   for i in range(int(len(list)/7)):
    # ��ȡ�������ο����
    t,l,w,h=int(list[0+7*i]),int(list[1+7*i]),int(list[2+7*i]),int(list[3+7*i])
    # ������ο����Ͻ��Լ����½ǵ��������
    cv2.rectangle(vis, (l, t), (l+w, t+h),(255, 0, 0), 2)
    # ��ÿһ�������ο�����ϽǱ�ע�Ա�������ֵ�����Ϣ
    cv2.putText(vis, 'gender:'+list[4+7*i]+' '+'age:'+list[5+7*i]+' '+'score:'+list[6+7*i], (l, t), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 0), 1)
   # ��ʾ�������ͼƬ
   cv2.imshow("Image", vis)
   cv2.waitKey (0)

class Recognize:
 def __init__(self):
  window=Tk()
  window.title("Recognize")
  self.text=Text(window,width=100,height=20)
  self.text.pack()
  self.Var=StringVar()
  frame1=Frame(window)
  frame1.pack()
  Label(frame1,text="Select a picture:").grid(row=1,column=1,sticky=W)
  e=Entry(frame1,textvariable=self.Var,width=40)
  e.grid(row=1,column=2)
  Button(frame1,text="���",command=lambda:self.processBrowse(e)).grid(row=1,column=3)
  Button(frame1,text="ȷ�Ϸ���",command=lambda:self.processDelivery(e)).grid(row=1,column=4)
  Button(frame1,text="ʶ����",command=self.processResult).grid(row=1,column=5)
  window.mainloop()

 def processBrowse(self,e):
  e.delete(0,END)
  m=askopenfilename()
  e.insert(0,m)

 def processDelivery(self,e):
  self.filename=e.get()
  if os.path.exists(self.filename)==0: 
   messagebox.showinfo("Tip","The file is not exist!")
   return 0
  elif re.search('\.jpg',self.filename) is None:
   messagebox.showinfo("Tip","The file is not picture.jpg!")
   return 
  tcpCliSock = socket(AF_INET, SOCK_STREAM)
  tcpCliSock.connect(ADDR)
  tcpCliSock.send('����ͼƬmode'.encode())
  if tcpCliSock.recv(BUFSIZ).decode()=='OK':
   self.text.insert(INSERT,'׼������ͼƬ\n')
  myfile = open(self.filename, 'rb')
  data = myfile.read()
  size = str(len(data))
  tcpCliSock.send(size.encode())
  rec = tcpCliSock.recv(BUFSIZ).decode()
  tcpCliSock.send(data)
  if tcpCliSock.recv(BUFSIZ).decode()=='OK':
   self.text.insert(INSERT,'����ͼƬ���\n')
  tcpCliSock.close()

 def processResult(self):
  # ���͹���ģʽ�������
  tcpCliSock = socket(AF_INET, SOCK_STREAM)
  tcpCliSock.connect(ADDR)
  tcpCliSock.send('Ŀ��ʶ��mode'.encode())
  # ���ܵ�����˷�������Ϣ
  rec=tcpCliSock.recv(BUFSIZ).decode()
  tcpCliSock.close()
  # �����ͨ��'!'���ָ���Ϊ�ַ������ͻ���ͨ��'!'ȥ��������ת��Ϊ�б�
  list=rec.split('!')
  # ʹ��opencv��ͼƬ
  img = cv2.imdecode(np.fromfile(self.filename,dtype=np.uint8),-1)
  window=Tk()
  window.title("Information")
  canvas=Canvas(window,width=1400,height=700,bg='white')
  canvas.pack()
  # ����б����Ϣ
  for i in range(0,len(list),2):
   canvas.create_text(700,100+60*i,text=list[i]+':'+list[i+1],font=('Times',40))
  # ��ʾͼƬ
  cv2.imshow("Image", img)
  cv2.waitKey (0)

class PlaceDetect:
 def __init__(self):
  # ����һ��tkinter����
  window=Tk()
  window.title("����ʶ��")
  # �ڴ����Ͻ����ı���
  self.text=Text(window,width=100,height=20)
  self.text.pack()
  self.Var=StringVar()
  frame1=Frame(window)
  frame1.pack()
  # ��ǩ��ʾ
  Label(frame1,text="Select a picture:").grid(row=1,column=1,sticky=W)
  # ������һ�������
  e=Entry(frame1,textvariable=self.Var,width=40)
  e.grid(row=1,column=2)
  # ����������ť ��frame1������ ���ʱ���ö�Ӧ���� ����λ��
  Button(frame1,text="���",command=lambda:self.processBrowse(e)).grid(row=1,column=3)
  Button(frame1,text="ȷ�Ϸ���",command=lambda:self.processDelivery(e)).grid(row=1,column=4)
  Button(frame1,text="ʶ����",command=self.processResult).grid(row=1,column=5)
  # ����ѭ��
  window.mainloop()

 def processBrowse(self,e):
  # ��������
  e.delete(0,END)
  # ���ô��ļ�����
  m=askopenfilename()
  # ���ļ������������
  e.insert(0,m)

 def processDelivery(self,e):
  # ��ȡ�ļ��������ļ�·��
  self.filename=e.get()
  # �ж��ļ�·���Ƿ����
  if os.path.exists(self.filename)==0: 
   messagebox.showinfo("Tip","The file is not exist!")
   return 0
  # �ж��Ƿ���jpgͼƬ�ļ�
  elif re.search('\.jpg',self.filename) is None:
   messagebox.showinfo("Tip","The file is not picture.jpg!")
   return 
  tcpCliSock = socket(AF_INET, SOCK_STREAM)
  # ���ӵ���������ַ
  tcpCliSock.connect(ADDR)
  # �����ַ���'����ͼƬmode'�÷����֪������ģʽ
  tcpCliSock.send('����ͼƬmode'.encode())
  # ������ܵ�����˵�ȷ�Ͼ����ı�����ʾ׼������ͼƬ
  if tcpCliSock.recv(BUFSIZ).decode()=='OK':
   self.text.insert(INSERT,'׼������ͼƬ\n')
  myfile = open(self.filename, 'rb')
  # ���ļ�����data��
  data = myfile.read()
  # ��ȡ�ļ��ַ�������
  size = str(len(data))
  tcpCliSock.send(size.encode())
  rec = tcpCliSock.recv(BUFSIZ).decode()
  # ����ͼƬ
  tcpCliSock.send(data)
  if tcpCliSock.recv(BUFSIZ).decode()=='OK':
   self.text.insert(INSERT,'����ͼƬ���\n')
  # �ر�����
  tcpCliSock.close()

 def processResult(self):
  # ���͹���ģʽ�������
  tcpCliSock = socket(AF_INET, SOCK_STREAM)
  tcpCliSock.connect(ADDR)
  tcpCliSock.send('����ʶ��mode'.encode())
  # ���ܵ�����˷�������Ϣ
  rec=tcpCliSock.recv(BUFSIZ).decode()
  # �ر�����
  tcpCliSock.close()
  # �����ͨ��'!'���ָ���Ϊ�ַ������ͻ���ͨ��'!'ȥ��������ת��Ϊ�б�
  list=rec.split('!')
  # �鿴�б���Ϣ���������Գ���
  print(list)
  # ʹ��opencv��ͼƬ
  img = cv2.imdecode(np.fromfile(self.filename,dtype=np.uint8),-1)
  # �½�tkinter����
  window=Tk()
  window.title("ʶ����Ϣ")
  canvas=Canvas(window,width=250,height=600,bg='white')
  canvas.pack()
  # ����б����Ϣ
  for i in range(0,len(list),2):
   canvas.create_text(125,30+30*i,text=list[i]+':'+list[i+1],font=('Times',20))
  # ��ʾͼƬ
  cv2.imshow("Image", img)
  cv2.waitKey (0)

class BodyDetect:
 def __init__(self):
  window=Tk()
  window.title("����ʶ��")
  self.text=Text(window,width=100,height=20)
  self.text.pack()
  self.Var=StringVar()
  frame1=Frame(window)
  frame1.pack()
  Label(frame1,text="ѡ��ͼƬ:").grid(row=1,column=1,sticky=W)
  e=Entry(frame1,textvariable=self.Var,width=40)
  e.grid(row=1,column=2)
  Button(frame1,text="����ļ�",command=lambda:self.processBrowse(e)).grid(row=1,column=3)
  Button(frame1,text="ȷ�Ϸ���",command=lambda:self.processDelivery(e)).grid(row=1,column=4)
  Button(frame1,text="�������",command=self.processResult).grid(row=1,column=5)
  window.mainloop()

 def processBrowse(self,e):
  e.delete(0,END)
  m=askopenfilename()
  e.insert(0,m)

 def processDelivery(self,e):
  self.filename=e.get()
  if os.path.exists(self.filename)==0: 
   messagebox.showinfo("Tip","The file is not exist!")
   return 0
  elif re.search('\.jpg',self.filename) is None:
   messagebox.showinfo("Tip","The file is not picture.jpg!")
   return 
  tcpCliSock = socket(AF_INET, SOCK_STREAM)
  tcpCliSock.connect(ADDR)
  tcpCliSock.send('����ͼƬmode'.encode())
  if tcpCliSock.recv(BUFSIZ).decode()=='OK':
   self.text.insert(INSERT,'׼������ͼƬ\n')
  myfile = open(self.filename, 'rb')
  data = myfile.read()
  size = str(len(data))
  tcpCliSock.send(size.encode())
  rec = tcpCliSock.recv(BUFSIZ).decode()
  tcpCliSock.send(data)
  if tcpCliSock.recv(BUFSIZ).decode()=='OK':
   self.text.insert(INSERT,'����ͼƬ���\n')
  tcpCliSock.close()

 def processResult(self):
  # ���͹���ģʽ�������
  tcpCliSock = socket(AF_INET, SOCK_STREAM)
  tcpCliSock.connect(ADDR)
  tcpCliSock.send('����ʶ��mode'.encode())
  # ���ܵ�����˷�������Ϣ
  rec = tcpCliSock.recv(BUFSIZ).decode()
  # �ж�û���������
  if rec=='No':
   tcpCliSock.close()
   messagebox.showinfo("Tip","No face in the picture!")
  else:
   # ȥ��','�γ��б�
   list=rec.split(',')
   tcpCliSock.close()
   print(list)
   # ʹ��opencv����ͼƬ
   img = cv2.imdecode(np.fromfile(self.filename,dtype=np.uint8),-1)
   vis = img.copy()
   # �½�tk����
   window=Tk()
   window.title("Information")
   # ��һ������
   canvas=Canvas(window,width=300,height=300,bg='white')
   canvas.pack()
   # ���������Ϣ���ֱ������Ը��ʣ�������ɫ��������ɫ
   canvas.create_text(150,50,text=''.join(['���Ը��ʣ�',list[0]]),font=('Times',20))
   canvas.create_text(150,150,text=''.join(['������ɫ��',list[1]]),font=('Times',20))
   canvas.create_text(150,250,text=''.join(['������ɫ��',list[2]]),font=('Times',20))
   # ������ο����Ͻ��Լ����½ǵ��������
   cv2.rectangle(vis, (int(list[6]), int(list[4])), (int(list[6])+int(list[3]), int(list[4])+int(list[5])),(255, 0, 0), 2)
   # ��ע�Ա������Ϣ
   cv2.putText(vis, 'male rate��'+list[0], (int(list[6]), int(list[4])), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
   # ��ʾ�������ͼƬ
   cv2.imshow("Image", vis)
   cv2.waitKey (0)

class BodySkeleton:
 def __init__(self):
  window=Tk()
  window.title("����ؼ���ʶ��")
  self.text=Text(window,width=100,height=20)
  self.text.pack()
  self.Var=StringVar()
  frame1=Frame(window)
  frame1.pack()
  Label(frame1,text="ѡ��ͼƬ:").grid(row=1,column=1,sticky=W)
  e=Entry(frame1,textvariable=self.Var,width=40)
  e.grid(row=1,column=2)
  Button(frame1,text="����ļ�",command=lambda:self.processBrowse(e)).grid(row=1,column=3)
  Button(frame1,text="ȷ�Ϸ���",command=lambda:self.processDelivery(e)).grid(row=1,column=4)
  Button(frame1,text="�������",command=self.processResult).grid(row=1,column=5)
  window.mainloop()

 def processBrowse(self,e):
  e.delete(0,END)
  m=askopenfilename()
  e.insert(0,m)

 def processDelivery(self,e):
  self.filename=e.get()
  if os.path.exists(self.filename)==0: 
   messagebox.showinfo("Tip","The file is not exist!")
   return 0
  elif re.search('\.jpg',self.filename) is None:
   messagebox.showinfo("Tip","The file is not picture.jpg!")
   return 
  tcpCliSock = socket(AF_INET, SOCK_STREAM)
  tcpCliSock.connect(ADDR)
  tcpCliSock.send('����ͼƬmode'.encode())
  if tcpCliSock.recv(BUFSIZ).decode()=='OK':
   self.text.insert(INSERT,'׼������ͼƬ\n')
  myfile = open(self.filename, 'rb')
  data = myfile.read()
  size = str(len(data))
  tcpCliSock.send(size.encode())
  rec = tcpCliSock.recv(BUFSIZ).decode()
  tcpCliSock.send(data)
  if tcpCliSock.recv(BUFSIZ).decode()=='OK':
   self.text.insert(INSERT,'����ͼƬ���\n')
  tcpCliSock.close()

 def processResult(self):
  # ���͹���ģʽ�������
  tcpCliSock = socket(AF_INET, SOCK_STREAM)
  tcpCliSock.connect(ADDR)
  tcpCliSock.send('����ؼ���ʶ��mode'.encode())
  # ���ܵ�����˷�������Ϣ
  rec = tcpCliSock.recv(BUFSIZ).decode()
  # �ж�û����������
  if rec=='No':
   tcpCliSock.close()
   messagebox.showinfo("Tip","No!")
  # ����������
  else:
   # ȥ��','�γ��б�
   list=rec.split(',')
   # �ر�tcp����
   tcpCliSock.close()
   # ���list������ʹ��
   print(list)
   # ���list����
   print(len(list))
   # ʹ��opencv����ͼƬ
   img = cv2.imdecode(np.fromfile(self.filename,dtype=np.uint8),-1)
   vis = img.copy()
   # �ؼ������Ƽ��ϣ��б�
   skeletonName = ['head','neck','left_shoulder','left_elbow','left_hand','right_shoulder','right_elbow','right_hand','left_buttocks','left_knee','left_foot','right_buttocks','right_knee','right_foot']
   # ����ÿ��������32���������ֱ��Ǿ��ο����Ͻǵ�����(l,t)�����ο�ĸ�h�Ϳ�w
   # �Լ�ʮ�ĸ��ؼ�������Ӧ��x��y���� 32=4+2*14
   # ���������������ھ��ο������
   # forѭ�������Զ�����len(list)/32ȷ��������
   for i in range(int(len(list)/32)):
    # ��ȡ������ο����
    t,l,w,h=int(list[0+32*i]),int(list[1+32*i]),int(list[2+32*i]),int(list[3+32*i])
    # ������ο����Ͻ��Լ����½ǵ��������
    cv2.rectangle(vis, (l, t), (l+w, t+h),(255, 0, 0), 2)
    # ͨ��ѭ������ע14���ؼ����λ���Լ�����
    for j in range(14):
      # ͨ���ؼ������Ծ��ο����������൱��ͼƬ������
      pos=(l+int(list[4+2*j+32*i]),t+int(list[5+2*j+32*i]))
      # ��СȦ��ע���ؼ����λ��
      cv2.circle(vis, pos, 5, color=(0, 255, 0))
      # ��ע������Ϣ
      cv2.putText(vis, skeletonName[j], pos, cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 255, 0), 1)
   # ��ʾ��ע���ͼƬ
   cv2.imshow("Image", vis)
   cv2.waitKey (0)

class Cli:
 def __init__(self):
  # �½����ڣ��ͻ��˵Ļ������ڣ�
  window=Tk()
  window.title("�˹�����-��ĩ��Ŀ-�ͻ���")
  # �½��ı���
  self.text=Text(window,width=100,height=20)
  self.text.pack()
  # ��ť��һ��
  frame1=Frame(window)
  frame1.pack()
  # 5����ť
  Button(frame1,text="����ʶ��",command=self.processFaceDetect).grid(row=1,column=1)
  Button(frame1,text="Ŀ��ʶ��",command=self.processRecognize).grid(row=1,column=3)
  Button(frame1,text="����ʶ��",command=self.processBodyDetect).grid(row=1,column=5)
  Button(frame1,text="����ؼ���ʶ��",command=self.processBodySkeleton).grid(row=1,column=7)
  Button(frame1,text="����ʶ��",command=self.processPlaceDetect).grid(row=1,column=9)  
  window.mainloop()

 def processFaceDetect(self):
  self.text.insert(INSERT,'����ʶ����\n')
  # FaceDetect����ʵ����
  FaceDetect()

 def processRecognize(self):
  self.text.insert(INSERT,'Ŀ��ʶ����\n')
  # Recognize����ʵ����
  Recognize()

 def processBodyDetect(self):
  self.text.insert(INSERT,'����ʶ����\n')
  # BodyDetect����ʵ����
  BodyDetect()
  
 def processBodySkeleton(self):
  self.text.insert(INSERT,'����ؼ���ʶ����\n')
  # BodySkeleton����ʵ����
  BodySkeleton()

 def processPlaceDetect(self):
  self.text.insert(INSERT,'����ʶ����\n')
  # PlaceDetect����ʵ����
  PlaceDetect()

# ������б��ļ��������ǵ������룬��ô��ִ������ĳ���
if __name__ == '__main__':
  Cli()