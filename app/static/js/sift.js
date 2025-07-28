//* Urls
const urlDefaultImage = "{{ url_for('static', filename='img/selectImage.jpg') }}";
const urlStreamingDesktop = '/video_stream_local';

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

const loadingCamera = document.getElementById('loading-camera')


// Image
const streamingImage = document.getElementById('streaming_image')

//* Events
// Buttons
btLocal.addEventListener('click', () => setUrlStreaming(urlStreamingDesktop))

//btMobile.addEventListener('click', () => setUrlStreaming('set-operation',urlStreamingEsp32))


//* Functions
const setUrlStreaming = (urlStreaming) => {
    console.log('Setting streaming URL:', urlStreaming);
    loadingCamera.className = loadingCameraClass.show;
    fetch('/set_operation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            operation: operations.SIFT
        })
        
    }).then(() => {
        console.log('Setting streaming URL:', urlStreaming);
        streamingImage.src = urlStreaming;
        loadingCamera.className = loadingCameraClass.hide;
    })
}