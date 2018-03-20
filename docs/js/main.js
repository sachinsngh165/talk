document.getElementById('join').onclick = joinRoom;
var init = false;

var mediaConstraints = { 
    video:true,
    audio:true,
   }
$("#remote").css({"height":screen.height,"width":screen.width});
function joinRoom()
{
    var roomId = document.getElementById('roomId').value;
    window.mySocket = new WebSocket("wss://35.229.213.23:443/ws"+"?"+"roomID="+roomId);

    // Connection opened
    window.mySocket.addEventListener('open', function (event) {
        
        window.mySocket.onmessage  = function(event){
            if (event.data==='initiator') {
                log("You've successfully joined !")
                init = true;
                initiate()
            }else if(event.data=='not initiator'){
                log("You've successfully joined !")
                init = false;
                initiate()
            }else{
                window.alert('Only 2 users can connect at a time');
                log("Unable to join you")
            }
        }
    });

    // Connetion closed
    window.mySocket.addEventListener('close',function(event){
        document.getElementById('response').innerText = "Unable to join";
    });
    
}

function initiate(){
    navigator.mediaDevices.getUserMedia(mediaConstraints)
    .then(function(stream) {
        connect(stream)
        })
    .catch(function(reason) {
            log(reason)
          });
}


function connect(stream){

    pc = RTCPeerConnection(configuration = {
      'iceServers': [{
        'urls': 'stun:stun.l.google.com:19302'
      }]
    });


    if(stream){
        var local = document.querySelector('#local');
        local.srcObject = stream;
        // pc.addStream(stream)
        stream.getTracks().forEach(track => pc.addTrack(track, stream));
    }

    // if media available on connection just grab it and show it
    pc.ontrack = function(event){
        console.log("stream added");
        var remote = document.querySelector('#remote');
        remote.srcObject = event.streams[0];
    }

    pc.onicecandidate = function(event) {
        if (event.candidate) {
            console.log("onicecandidate triggred")
            window.mySocket.send(JSON.stringify(event.candidate));
        }
    };

    window.mySocket.onmessage = function(event){
        var signal = JSON.parse(event.data);
        if (signal.sdp) {
            if(init){
                log('received offer...');
                pc.setRemoteDescription(new RTCSessionDescription(signal))
                    .then(function(){
                        pc.createAnswer()
                        .then(function(answer) {
                            log('created answer...');
                            return pc.setLocalDescription(answer);
                        })
                        .then(function() {
                            log('sent answer');
                            window.mySocket.send(JSON.stringify(pc.localDescription));
                         })  
                        .catch(function(reason) {
                            log(reason)
                          });
                    })
                    .catch(function(reason) {
                            log(reason)
                          });
            }else{
                log('received offer...');
                pc.setRemoteDescription(signal)
            }
        }else if(signal.candidate){
            pc.addIceCandidate(new RTCIceCandidate(signal));
        }
        
    }



    if (!init) {
        pc.createOffer().then(function(offer) {
            log("offer created! ")
            return pc.setLocalDescription(offer);
        })
        .then(function() {
            log("offer send! ")
            window.mySocket.send(JSON.stringify(pc.localDescription));
        })
        .catch(function(reason) {
            log(reason)
        }); 
    }


}

function log() {
    $('#status').text(Array.prototype.join.call(arguments, ' '));
    console.log.apply(console, arguments);
}
