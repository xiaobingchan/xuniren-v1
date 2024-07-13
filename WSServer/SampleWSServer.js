var readline = require('readline');
var rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

var WebSocketServer = require('ws').Server;
wss = new WebSocketServer({ port: 60001 });

var clients = []; // 客户端列表

wss.on('connection', (ws) => {
  console.log('客户端已连接');
  clients.push(ws); // 将新连接的客户端添加到列表中

  ws.on('message', (message) => {
    console.log('收到客户端消息: ' + message);
    clients.forEach(client => {
        client.send(`${message}`); // 向每个客户端发送数据
      });
  });

  ws.on('close', () => {
    console.log('客户端断开连接');
    clients = clients.filter(client => client !== ws); // 从列表中移除断开连接的客户端
  });

});

console.log('服务器启动');