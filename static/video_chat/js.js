const APP_ID = 'ae631a91619147b59ff5c37edd22e36d'



const CHANNEL = sessionStorage.getItem('RoomName')
const TOKEN = sessionStorage.getItem('Token')
let UID = Number(sessionStorage.getItem('UID'))
let name = sessionStorage.getItem('Name')

const client = AgoraRTC.createClient()

let localTrack = []
let remoteUsers = {}


let joinAndDisplayLocalStream = async () => {
   document.getElementById('room-name').innerText = CHANNEL

   client.on('user-published' , handleUserJoined)
   client.on('user-left' , handleUserLeft)

   try {
    await client.join(APP_ID , CHANNEL , TOKEN , UID)
   } catch (error) {
    console.log(error)
    window.open('/interview/interview_home' , '_self' )   
   }

   

   localTrack = await AgoraRTC.createMicrophoneAndCameraTracks()

   let player =  `
                   <div class="col-md  card border" id="user-container-${UID}">
                               <p> ${name} </p>
                               <div style="height: 600px; width: 100%;" class=""embed-responsive-item p-3" id="user-${UID}"></div>
                              
                    </div>
   `
   document.getElementById('video_streams').insertAdjacentHTML('beforeend' , player)

   localTrack[1].play(`user-${UID}`)

   await client.publish([localTrack[0] , localTrack[1]])
}



let handleUserJoined = async (user , mediaType) => {
          remoteUsers[user.uid] = user
          await client.subscribe(user , mediaType)

          let response = await fetch(`/interview/get_user?user=${user.uid}`)
          let data = await response.json()
          let user_name = data.name


          if(mediaType === 'video'){
            let player =  document.getElementById(`user-container-${user.uid}`)
            if (player != null) {
                player.remove()
            }
            player =  `
            <div class="col-md  card border" id="user-container-${user.uid}">
                        <p> ${user_name} </p>
                        <div style="height: 600px; width: 100%;" class=""embed-responsive-item p-3" id="user-${user.uid}"></div>
                        
            </div>


            `
            document.getElementById('video_streams').insertAdjacentHTML('beforeend' , player)
            user.videoTrack.play(`user-${user.uid}`)
          }
          if(mediaType === 'audio'){
            user.audioTrack.play()
          }

}



let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()
}


let leaveAndRemoveLocalStream = async () => {
    for (let i = 0; localTrack.length > i  ; i++) {
        localTrack[i].stop()
        localTrack[i].close()
    }
    await client.leave()
    window.open('/' , '_self')
}

let toggleCamera = async (e) => {
    if (localTrack[1].muted) {
        await localTrack[1].setMuted(false)
        e.target.classList.add('btn-danger')
    }
    else {
        await localTrack[1].setMuted(true)
        e.target.classList.remove('btn-danger')
    }
}


let toggleMic = async (e) => {
    if (localTrack[0].muted) {
        await localTrack[0].setMuted(false)
        e.target.style.add()
    }
    else {
        await localTrack[0].setMuted(true)
        e.target.classList.remove('btn-danger')
    }
}

joinAndDisplayLocalStream()


try {
    document.getElementById('leave-btn').addEventListener('click' , leaveAndRemoveLocalStream)
    document.getElementById('video-btn').addEventListener('click' , toggleCamera)
    document.getElementById('mic-btn').addEventListener('click' , toggleMic)
} catch {
    console.log('error')
}



