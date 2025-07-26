//* Urls
const urlDefaultImage = "{{ url_for('static', filename='img/selectImage.jpg') }}";
const urlStreamingDesktop = '/video_stream_local';

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
    console.log('Setting streaming URL:', urlStreaming);
    streamingImage.src = urlStreaming;
}