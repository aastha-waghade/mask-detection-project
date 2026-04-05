/* =========================
   🔥 HAMBURGER MENU
========================= */
function toggleMenu() {
    const nav = document.getElementById("navLinks");
    nav.classList.toggle("active");
}

document.addEventListener("click", function(e) {
    const nav = document.getElementById("navLinks");
    const hamburger = document.querySelector(".hamburger");

    if (!nav || !hamburger) return;

    if (!nav.contains(e.target) && !hamburger.contains(e.target)) {
        nav.classList.remove("active");
    }
});


/* =========================
   📱 USER CAMERA
========================= */

let userStream = null;
let userInterval = null;

function startUserCamera() {

    const video = document.getElementById("userVideo");
    const canvas = document.getElementById("canvas");
    const loader = document.getElementById("loader");
    const processed = document.getElementById("processedVideo");

    if (!video || !canvas || !processed) return;

    // 🔥 FIX: reset camera before start
    if (userStream) {
        userStream.getTracks().forEach(track => track.stop());
        userStream = null;
    }

    if (userInterval) {
        clearInterval(userInterval);
        userInterval = null;
    }

    video.style.display = "none";

    if (loader) loader.style.display = "flex";

    navigator.mediaDevices.getUserMedia({
        video: {
            width: { ideal: 1280 },
            height: { ideal: 720 },
            facingMode: "user"
        }
    })
    .then(stream => {

        console.log("Camera started");

        userStream = stream;
        video.srcObject = stream;

        video.onloadedmetadata = () => {
            video.play();
        };

        if (loader) loader.style.display = "none";

        const ctx = canvas.getContext("2d");

        let initialized = false; // 🔥 FIX

        userInterval = setInterval(() => {

            if (video.readyState !== 4) return;

            const width = video.videoWidth;
            const height = video.videoHeight;

            if (!width || !height) return;

            // 🔥 set canvas size only once
            if (!initialized) {
                canvas.width = width;
                canvas.height = height;
                initialized = true;
            }

            ctx.drawImage(video, 0, 0, width, height);

            // 🔥 better quality image
            const image = canvas.toDataURL("image/jpeg", 0.8);

            fetch("/detect_frame", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ image: image })
            })
            .then(res => res.json())
            .then(data => {

                console.log("DATA:", data);

                if (!data || data.error) return;

                if (data.image) {
                    processed.src = "data:image/jpeg;base64," + data.image;
                    processed.style.display = "block";
                }

                updateStats(data.mask, data.no_mask);

            })
            .catch(err => console.log("Error:", err));

        }, 800); // 🔥 faster + smoother

    })
    .catch(err => {
        console.log("CAMERA ERROR:", err);
        alert("Camera not working: " + err.message);

        if (loader) loader.style.display = "none";
    });
}


function stopUserCamera() {

    const video = document.getElementById("userVideo");
    const processed = document.getElementById("processedVideo");
    const loader = document.getElementById("loader");

    if (userStream) {
        userStream.getTracks().forEach(track => track.stop());
        userStream = null;
    }

    if (userInterval) {
        clearInterval(userInterval);
        userInterval = null;
    }

    if (video) {
        video.srcObject = null;
        video.style.display = "none";
    }

    if (processed) {
        processed.style.display = "none";
        processed.src = "";
    }

    if (loader) loader.style.display = "none";
}


/* =========================
   📊 UPDATE UI
========================= */

function updateStats(mask, noMask) {

    mask = Number(mask) || 0;
    noMask = Number(noMask) || 0;

    document.getElementById("maskCount").innerText = mask;
    document.getElementById("noMaskCount").innerText = noMask;

    let total = mask + noMask;
    let percent = total ? ((mask / total) * 100).toFixed(1) : 0;

    document.getElementById("compliance").innerText = percent + "%";
    document.getElementById("totalCount").innerText = total;
}