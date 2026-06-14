function getBackendDomain() {
    const domain = window.location.hostname || window.currentURL.hostname;
    const firstDotIndex = domain.indexOf('.');
    const subdomain = domain.substring(0, firstDotIndex);
    const restOfDomain = domain.substring(firstDotIndex);
    return "https://" + subdomain + "-backend" + restOfDomain;
}

document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    const processedImage = document.getElementById("processedImage");
    const faceCountText = document.getElementById("faceCount");

    if (!faceCountText) {
        console.error("Error: faceCountText element is missing in the DOM.");
        return;
    }

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => { video.srcObject = stream; })
        .catch(err => console.error("Camera access denied:", err));

    window.captureImage = function () {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(blob => sendImageToServer(blob), "image/png");
    };

    document.getElementById("fileInput").addEventListener("change", (event) => {
        const file = event.target.files[0];
        if (file) sendImageToServer(file);
    });

    const api = getBackendDomain();
    
    async function sendImageToServer(imageBlob) {
        try {
            console.log("Sending image to server:", imageBlob);
            const formData = new FormData();
            formData.append("image", imageBlob, "uploaded_image.png");

            const response = await axios.post(api + '/upload', formData, { timeout: 5000 });

            console.log("Server Response:", response.data);

            if (response.data.faces_detected !== undefined) {
                faceCountText.textContent = `Faces detected: ${response.data.faces_detected}`;
                processedImage.src = response.data.processed_image; 
                processedImage.style.display = "block";
            }
        } catch (error) {
            console.error("Error:", error);
            faceCountText.textContent = "Error processing image!";
        }
    }
});
