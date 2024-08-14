from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import time
from UserManagement.models import CustomUser
# Create your views here.


def getToken(request) :
    appId = 'ae631a91619147b59ff5c37edd22e36d'
    appCertificate = 'f69738ab92864236b7a61f79a4df8552'
    channelName = request.GET.get('channel')
    uid = request.user.id
    name = request.user.first_name + ' ' + request.user.last_name 
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role =  1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token , 'uid':uid , 'name':name} , safe=False)


def create_token(channel_name, uid, first_name) :
    appId = 'ae631a91619147b59ff5c37edd22e36d'
    appCertificate = 'f69738ab92864236b7a61f79a4df8552'
    channelName = channel_name
    uid = uid
    name = first_name
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role =  1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return True


def interview_home(request) :
    return render (request , 'video_chat/interview_home.html')


def interview(request) :
    return render (request , 'video_chat/interview.html')


def get_user(request) :
    id = request.GET.get('user')
    user = CustomUser.objects.get(id=id)
    name = user.first_name + ' ' + user.last_name
    return JsonResponse({'name':name} , safe=False)   
