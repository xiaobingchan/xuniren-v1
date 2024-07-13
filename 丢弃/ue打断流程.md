1, 第一次说小红小红唤醒的时候，ue http post发送说话：
   http://127.0.0.1:5000/apppost
   {
	"message": "你好我在"
}

2，如果是第二次说小红小红的时候，无论是否在说话都http post请求打断：
http://127.0.0.1:5000/daduan
{
    "message": "你好我是火星一朗"
}

   2.1 如果没有说话，则服务器会返回json：
       {
    "message": "failed"
}

   2.2 如果在说话，则服务器会返回json：
   {
    "message": "ok"
}