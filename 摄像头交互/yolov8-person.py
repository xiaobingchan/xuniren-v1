from ultralytics import YOLO
import cv2
import time
import asyncio
import websockets
import json

duration = 2 # 检测时间（秒）
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("3714c8f4b2a6502316bab8ce46e53fbf.mp4")
# 识别框位置
rectangle_coordinates = [(350, 50), (700, 600)]
model =  YOLO('yolov8n.pt')
model.conf = 0.8  # 置信度阈值
# 初始化计时器和标志位
last_alarm_time = 0
face_detected = False
# 初始化计时器
timer = 0
start_time = -1  # 将start_time初始化为-1


async def send_message_to_websocket(message):
    async with websockets.connect('ws://localhost:60001') as websocket:
        await websocket.send(message)  # 发送消息给服务器
        print("Message sent")

def send_message(message):
    asyncio.run(send_message_to_websocket(message))

def append_to_file(file_path, string_to_append):
   """bixu
   将字符串追加到指定的文件中。
   如果文件不存在,将创建新文件。
   """
   try:
      # 以追加模式打开文件
      with open(file_path, 'a', encoding='utf-8') as file:
         # 将字符串写入文件
         file.write(string_to_append)
   except IOError:
      print(f"无法打开文件 {file_path}")

if __name__ == '__main__':
 
   while True:

      ret, frame = cap.read()

      if not ret:
         break

      cv2.rectangle(frame, rectangle_coordinates[0], rectangle_coordinates[1], (0, 0, 255), thickness=2)
      results = model.predict(source=frame)
      for result in results:
         boxes = result.boxes  # Boxes object for bbox outputs
         for box in boxes:

            x1, y1, x2, y2 = box.xyxy[0]  # getBboxCoordinates
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # 获取置信度和类别标签
            conf = box.conf[0]
            cls = int(box.cls[0])
            label = f"{model.names[cls]} {conf:.2f}"
            if conf>0.8 and "person" in str(label):
               frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
               frame = cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)
               
               # print(f"检测到有人: ({x1}, {y1}), ({x2}, {y2})")
               # 判断人脸是否完全位于矩形框范围内
               if (x1 >= rectangle_coordinates[0][0] and x2 <= rectangle_coordinates[1][0]):
                  print("人脸完全位于矩形框范围内！")
                  print(start_time)
                  # 如果计时器未启动,启动计时器
                  if start_time == -1:
                        start_time = time.time()

                  # 计算当前计时器值
                  timer = time.time() - start_time
                  print("当前进入时间为："+str(timer))

                  # 如果计时器超过3秒,报警
                  if timer > 3:
                      print("人物停留时间过长,报警!")
                      print("警报！")
                      append_to_file('output.txt', "警报！"+'\n')
                      my_dict = {"type": "camera"}
                      json_string = json.dumps(my_dict, ensure_ascii=False)
                      result = json_string
                      print("ws 60001发送数据："+result)
                      send_message(result)
                      time.sleep(1)
                      print("重新计时")
                      start_time = -1
                      timer = -1
               else:
                   print("清空计时器")
                   start_time = -1
                   timer = -1
      cv2.imshow('Face detection', frame)

      if cv2.waitKey(1) & 0xFF == ord('q'):
         break


cap.release()
cv2.destroyAllWindows()
