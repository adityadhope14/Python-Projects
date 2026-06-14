from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import cgi
import cv2
import numpy as np
import base64

PORT = 8080

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

class FaceDetectionHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/upload":
            self.handle_upload()
        else:
            self.send_error(404, "Invalid endpoint")
    
    def handle_upload(self):
        content_type, pdict = cgi.parse_header(self.headers.get('Content-Type'))
        if content_type == 'multipart/form-data':
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            form_data = cgi.parse_multipart(self.rfile, pdict)
            
            if "image" in form_data:
                image_data = form_data["image"][0]

                face_count, encoded_image = self.detect_faces(image_data)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "faces_detected": face_count,
                    "processed_image": encoded_image  
                }).encode())
            else:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid content type"}).encode())

    def detect_faces(self, image_data):

        np_arr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for i, (x, y, w, h) in enumerate(faces):
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image, f'Face {i+1}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        _, buffer = cv2.imencode(".jpg", image)
        encoded_image = base64.b64encode(buffer).decode("utf-8") 

        return len(faces), f"data:image/jpeg;base64,{encoded_image}" 

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), FaceDetectionHandler)
    print(f"Server running on port {PORT}")
    server.serve_forever()
