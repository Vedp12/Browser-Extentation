const camera = document.getElementById("camera");
        const cameraScreen = document.getElementById("camera-screen");
        const toggleBtn = document.getElementById("toggle-camera");
        const takePhotoBtn = document.getElementById("take-photo");
        const savePhotoBtn = document.getElementById("save-photo");
        const retakeBtn = document.getElementById("retake-photo");
        const closeBtn = document.getElementById("close-camera");
        const closeBtnfirst = document.getElementById("close-camera-first");
        const photo = document.getElementById("photo");
        const canvas = document.getElementById("canvas");
        const status = document.getElementById("status");

        let stream = null;
        let cameraOpening = false;

        async function showCamera() {
            if (cameraOpening || stream) return;

            cameraOpening = true;
            toggleBtn.disabled = true;
            status.textContent = "Requesting camera permission...";

            try {
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    throw new Error("Camera access requires HTTPS or localhost.");
                }

                // Reveal the camera screen only after the user clicks.
                cameraScreen.hidden = false;
                resetPhoto();

                const newStream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: "environment" },
                    audio: false,
                });

                stream = newStream;
                camera.srcObject = stream;

                await camera.play();

                // toggleBtn.textContent = "Close Camera";
                status.textContent = "Camera is ready. Take a photo.";
            } catch (error) {
                console.error("Camera error:", error);

                cameraScreen.hidden = true;

                if (error.name === "NotAllowedError") {
                    status.textContent = "Camera permission denied. Allow camera access in your browser.";
                } else if (error.name === "NotFoundError") {
                    status.textContent = "No camera was found on this device.";
                } else if (error.name === "NotReadableError") {
                    status.textContent = "Camera is busy. Close other apps using it.";
                } else {
                    status.textContent = "Unable to start camera: " + error.message;
                }

                stopCameraStream();
            } finally {
                cameraOpening = false;
                toggleBtn.disabled = false;
            }
        }

        function stopCameraStream() {
            if (stream) {
                stream.getTracks().forEach((track) => track.stop());
                stream = null;
            }

            camera.pause();
            camera.srcObject = null;
        }

        function closeCamera() {
            stopCameraStream();

            resetPhoto();
            cameraScreen.hidden = true;
            // toggleBtn.textContent = "Show Camera";
            // status.textContent = "Camera closed.";
        }

        function resetPhoto() {
            capturedDataUrl = null;
            photo.removeAttribute("src");
            photo.hidden = true;
            closeBtn.hidden = true;
            // closeBtnfirst.hidden = false;
            savePhotoBtn.hidden = true;
            retakeBtn.hidden = true;
            takePhotoBtn.hidden = false;
        }

        let capturedDataUrl = null;

        function savePhoto() {
            if (!capturedDataUrl) {
                status.textContent = "Take a photo first.";
                return;
            }

            const link = document.createElement("a");
            link.href = capturedDataUrl;
            link.download = "photo-" + Date.now() + ".jpg";
            document.body.appendChild(link);
            link.click();
            link.remove();

            status.textContent = "Photo saved to your downloads.";
        }

        function takePhoto() {
            if (!stream || !camera.videoWidth || !camera.videoHeight) {
                status.textContent = "Camera is not ready. Please wait a moment.";
                return;
            }

            // Match the canvas dimensions to the camera frame.
            canvas.width = camera.videoWidth;
            canvas.height = camera.videoHeight;

            const context = canvas.getContext("2d");

            context.drawImage(camera, 0, 0, canvas.width, canvas.height);

            // Show the captured frame directly over the video preview.
            capturedDataUrl = canvas.toDataURL("image/jpeg", 0.92);
            photo.src = capturedDataUrl;
            photo.hidden = false;

            // Photo actions appear once, right after the photo is taken.
            closeBtn.hidden = false;
            savePhotoBtn.hidden = false;
            retakeBtn.hidden = false;
            takePhotoBtn.hidden = true;

            status.textContent = "Photo captured. Save it or retake.";
        }

        toggleBtn.addEventListener("click", () => {
            if (stream) {
                closeCamera();
            } else {
                showCamera();
            }
        });

        closeBtn.addEventListener("click", closeCamera);
        // closeBtnfirst.addEventListener("click", closeCamera);

        takePhotoBtn.addEventListener("click", takePhoto);

        savePhotoBtn.addEventListener("click", savePhoto);

        retakeBtn.addEventListener("click", () => {
            resetPhoto();
            status.textContent = "Retake your photo.";
        });
