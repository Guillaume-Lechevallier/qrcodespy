from flask import Flask, render_template_string, Response
import time
import qrcode
import base64
from io import BytesIO
import cv2
from pyzbar.pyzbar import decode
import pyautogui

app = Flask(__name__)


def generate_qr_code(data):
    img = qrcode.make(data)
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    return base64.b64encode(img_io.getvalue()).decode('utf-8')


def countdown_generator():
    for i in range(100000000000000000000000, -1, -1):
        qr_code_data = generate_qr_code(str(i))
        yield f"<h1>{i}</h1><img src='data:image/png;base64,{qr_code_data}'>"


@app.route('/')
def countdown():
    return render_template_string('''
        <head>
        <style>
        .centered {
            position: absolute;
            top: 40%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 96%;
        }
        .bouton {
            position: absolute;
            top: 70%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 96%;
            background-color: #6131AD;
            text-align: center;
            color:white;
            font-family: Arial, sans-serif;
            font-size: 40px;
        }
        </style>
        </head>
        
        <h1 id="countdown" style:"color:white;">×</h1>

        <img class="centered" style="border: 6px solid orange;" id="qrcode" src="" alt="QR Code" >

        
        <script class="bouton">

            function updateCountdown(count) {
                document.getElementById('countdown').innerText = count;
                fetch(`/qrcode/${count}`)
                    .then(response => response.text())
                    .then(qrcodeData => {
                        document.getElementById('qrcode').src = `data:image/png;base64,${qrcodeData}`;
                    });
            }

            let count = 1;
            updateCountdown(count);

            const countdownInterval = setInterval(function() {
                count--;
                count++;
                if (count < 0) {
                    clearInterval(countdownInterval);
                } else {
                    updateCountdown(count);
                }
            }, 1000);
        </script>
        <h2 class="bouton">COMMENT UTILISER LE QR CODE</h2>
    ''')


@app.route('/qrcode/<int:count>')
def get_qrcode(count):
    screenshot = pyautogui.screenshot()

    screenshot.save('screenshot.png')

    image = cv2.imread('screenshot.png')

    decoded_objects = decode(image)
    if decoded_objects:
        for obj in decoded_objects:
            print("Type :", obj.type)
            count = obj.data


    else:

        count = "il n'y a pas de qr code"
    import os
    os.remove('screenshot.png')


    count = str(count)
    count = count[2:-1]
    print("Données :", count)
    qr_code_data = generate_qr_code(str(count))
    return qr_code_data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=32769)
