//* Urls
const urlDefaultImage = "{{ url_for('static', filename='img/selectImage.jpg') }}";
const urlStreamingDesktop = '/video_stream_local';
const urlStreamingMobile = '/video_stream_mobile';

const operations = {
    LBP: "LBP",
    SIFT: "SIFT"
}

const loadingCameraClass = {
    show: 'message-show',
    hide: 'message-hide'
}

//* DOOM
// Botones
const btMobile = document.getElementById('btMobile')
const btLocal = document.getElementById('btLocal')
const btStopStreaming = document.getElementById('btStopStream')

const loadingCamera = document.getElementById('loading-camera')

const formIp = document.getElementById('form_ip')


// Image
const streamingImage = document.getElementById('streaming_image')

//* Events
// Buttons
btLocal.addEventListener('click', () => setUrlStreaming(urlStreamingDesktop))

formIp.addEventListener('submit', (e) => setIp(e))


btMobile.addEventListener('click', () => setUrlStreaming(urlStreamingMobile))


//* Functions
const setUrlStreaming = async (urlStreaming) => {
    console.log('Setting streaming URL:', urlStreaming);
    loadingCamera.className = loadingCameraClass.show;
    fetch('/set_operation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            operation: operations.LBP
        })

    }).then(() => {
        console.log('Setting streaming URL:', urlStreaming);
        streamingImage.src = urlStreaming;
        setTimeout(function () {
            loadingCamera.className = loadingCameraClass.hide;
            console.log('Streaming URL set successfully');
        }, 3000);
    })
}

const setIp = (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));
    const dataJson = JSON.stringify(data);
    console.log('Setting IP:', data.ip);
    loadingCamera.className = loadingCameraClass.show;
    fetch('/set_ip', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            ip: data.ip,
            operation: operations.LBP
        })
    }).then(() => {
        setTimeout(function () {
            streamingImage.src = urlStreamingDesktop;
            loadingCamera.className = loadingCameraClass.hide;
            console.log('Streaming URL set successfully');
        }, 3000);
    }).catch((error) => {
        alert('Error setting IP:', error);
    });
}