import socket
import json
import time
import threading


def is_port_open(host, port):
    # 创建一个socket对象
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # 设置超时时间
    try:
        # 尝试连接到指定的主机和端口
        result = sock.connect_ex((host, port))
        if result == 0:
            return True  # 端口是打开的
        else:
            return False  # 端口是关闭的
    except socket.error as e:
        print(f"Socket error: {e}")
        return False  # 无法连接，端口可能关闭或主机不可达
    finally:
        sock.close()  # 确保释放资源
        

def socket_server(listen_port, connect_number, process_func,process_args=None,debug=False):

    # 创建一个TCP socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定IP地址和端口号
    server_address = ('localhost', listen_port)
    server_socket.bind(server_address)

    # 监听连接请求
    server_socket.listen(connect_number)
    print(f'socket_server启动完毕，监听{listen_port}，等待连接中...')
    with server_socket:
        while True:
            try:
                if debug: print("# 接受客户端连接请求并建立连接")
                client_socket, client_address = server_socket.accept()
                if debug: print(f'连接来自 {client_address}')
                # 处理客户端请求
                data = client_socket.recv(10024)
                if not data:
                    break
                if debug: print(f"Received data from {client_address}: {data.decode()}")
                    
                query = data.decode()
                if debug: print("query=",query)
                if process_args is not None:
                    result = process_func(query,process_args=process_args)
                else:
                    result = process_func(query)

                # response_json = json.dumps(result)
                if result is not None:
                    client_socket.sendall(result.encode())

                if debug: print("# 关闭客户端连接和服务器socket对象")
                client_socket.close()
            except Exception as e:
                print("socket server error, msg",str(e))
    server_socket.close()


def lyyhttp(listen_port, process_func, path="/", process_args=None,debug=False):
    from flask import Flask, request,jsonify

    print(f"strart lyyhttp, listen on {listen_port}")
    app = Flask(__name__)
    
    app.debug = debug
    if debug is False:
        # 禁止werkzeug输出日志
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        

    @app.route(path,methods=['GET', 'POST'])
    def ssbz():
        print("get data")#http://127.0.0.1:8088/jiepan?code=000025
        data = request.get_data().decode()
        if request.method=="GET":
            code = request.args.get('code')             
            if process_args is None:
                result_dict = process_func(code)
            else:
                result_dict = process_func(process_args,code)


            return (result_dict)

    @app.route('/send', methods=['GET', 'POST'])
    def send():
        data_dict = {}
        if request.method=="GET":
            data_dict['code']= request.args.getlist()
            data_dict['value']= request.args.get('value')
            result_dict = process_func(data_dict)
            return result_dict
        
        elif request.method=="POST":
            data = request.get_data().decode()
            print("data=",data)
            result_dict = process_func(data)
            return result_dict
        
        if request.method == 'GET':
            code = request.args.get('code')
            date = request.args.get('date')
        elif request.method == 'POST':
            code = request.form.get('code')
            date = request.form.get('date')
        else:
            return jsonify({"error": "Invalid request method"}), 400
        print("get data",code)
        if process_args is None:
            result_dict = process_func(code,date)
        else:
            result_dict = process_func(process_args,code,date)
        if not code or not date:
            return jsonify({"error": "Missing required parameters"}), 400

        # 在这里处理参数，例如验证它们或将它们存储在数据库中
        # ...
        return jsonify(result_dict), 200
    app.run(host='0.0.0.0', port=listen_port,debug=debug)
    
def lyyfastapi(listen_port, process_func, path="/", process_args=None,debug=False):
    from fastapi import FastAPI, Request, Response

    app = FastAPI()

    @app.route(path, methods=['GET', 'POST'])
    async def ssbz(request: Request):
        data = await request.body()
        data = data.decode()
        if request.method == "GET":
            code = request.query_params.get('code')
            if process_args is None:
                result_dict = process_func(code)
            else:
                result_dict = process_func(process_args, code)
            return Response(content=result_dict)

    @app.route("/send", methods=['GET', 'POST'])
    async def send(request: Request):
        data_dict = {}
        if request.method == "GET":
            data_dict['code'] = request.query_params.getlist()
            data_dict['value'] = request.query_params.get('value')
            result_dict = process_func(data_dict)
            return Response(content=result_dict)

        elif request.method == "POST":
            data = await request.body()
            data = data.decode()
            result_dict = process_func(data)
            return Response(content=result_dict)

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=listen_port)
    
def process_request(query):

    query = query.strip("\n").strip()
    print("get request from socket server, query=<" + query + ">")
    #  解析查询条件
    try:
        print("xx")
        result = {"result": "r u ok"}

    except Exception as e:
        print(e)
        pass
        # result = str(e)
    if isinstance(result, dict):
        return json.dumps(result)
    else:
        return result


def send_message(message,debug=False):
    print("send message to ",("127.0.0.1", 9999))
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("127.0.0.1", 9999)
        client_socket.connect(server_address)
        client_socket.sendall(message.encode("utf-8"))
        client_socket.close()

        if debug: print("send_message finish. msg=" + message)
    except Exception as e:
        print(f"send_message to {server_address} error" + str(e))
        time.sleep(5)


if __name__ == '__main__':
    import threading

    threading.Thread(target=lyyhttp,         kwargs={
            "listen_port": 8088,
            "process_func": process_request,
            "path": "/jiepan",
            "process_args": None,
        }, daemon=False).start()
