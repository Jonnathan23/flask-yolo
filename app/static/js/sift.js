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
const btStopStreaming = document.getElementById('btStopStream')

// Image
const streamingImage = document.getElementById('streaming_image')

//* Events
// Buttons
btLocal.addEventListener('click', () => setUrlStreaming(urlStreamingDesktop))
btStopStreaming.addEventListener('click', () => setUrlStreaming(urlDefaultImage))

//btMobile.addEventListener('click', () => setUrlStreaming('set-operation',urlStreamingEsp32))


//* Functions
const setUrlStreaming = async (urlStreaming) => {
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
    })

}