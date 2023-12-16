from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post, LikePost, FollowersCount, ChatMessage, Files
from django.contrib.auth.decorators import login_required
from itertools import chain 
from .forms import ChatMessageForm
import random, json, os

# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_following_list = []
    feed = []

    all_users = User.objects.all()
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    
    for users in user_following:                                                                   
        user_following_list.append(users.user)


    # if len(user_following_list) > 10:
    #     for usernames in user_following_list:
    #         feed_lists = Post.objects.filter(user=usernames)
    #         feed.append(feed_lists)
    # else:    
    #     for usernames in user_following_list:
    #         feed_lists = Post.objects.filter(user=usernames)
    #         feed.append(feed_lists)
    #     for user in all_users:
    #         feed_lists = Post.objects.filter(user=user)
    #         feed.append(feed_lists)
            
    # current_user_post = Post.objects.filter(user=request.user.username)
    # feed.append(current_user_post)
    
    for user in all_users:
            feed_lists = Post.objects.filter(user=user)
            feed.append(feed_lists)
        
    feed_list = list(chain(*feed))

    # user suggestion 
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))                             

    return render(request, 'discover.html', {'user_profile': user_profile, 'posts':feed_list[:], 'suggestions_username_profile_list': suggestions_username_profile_list[:3]})


@login_required(login_url='signin')
def home(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    all_user = Profile.objects.all()
    if request.method == 'POST':
        searched_user = request.POST['username']
        gender = request.POST.get('gender')
        department = request.POST.get('department')
        batch = request.POST.get('batch')
        print(gender)
        if searched_user != '' and searched_user is not None:
            all_user = all_user.filter(fullname__icontains=searched_user)
        if gender != '' and gender is not None:
            all_user = all_user.filter(gender__icontains=gender)
        if department != '' and department is not None:
            all_user = all_user.filter(department__icontains=department)
        if batch != '' and batch is not None:
            all_user = all_user.filter(batch__icontains=batch)    
    
    all_user_list = [u for u in list(all_user)]
    random.shuffle(all_user_list)
    
    context = {'user_profile': user_profile, 'all_user': all_user_list}
    return render(request, 'home.html', context)


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            fullname = request.POST['fullname']
            phonenumber = request.POST['phonenumber']
            idcard = request.POST['idcard']
            batch = request.POST.get('batch')
            gender = request.POST.get('gender')
            department = request.POST.get('department')
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.fullname = fullname
            user_profile.phonenumber = phonenumber
            user_profile.idcard = idcard
            user_profile.batch = batch
            user_profile.gender = gender
            user_profile.department = department
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            fullname = request.POST['fullname']
            phonenumber = request.POST['phonenumber']
            idcard = request.POST['idcard']
            batch = request.POST.get('batch')
            gender = request.POST.get('gender')
            department = request.POST.get('department')

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.fullname = fullname
            user_profile.phonenumber = phonenumber
            user_profile.idcard = idcard
            user_profile.batch = batch
            user_profile.gender = gender
            user_profile.department = department
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'additional-info.html', {'user_profile': user_profile})


def signup(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
  

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                
                #create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')
    else:
        return render(request, 'SignUp_Page.html')
    
    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credential is Invalid')
            return redirect('signin')
    else:        
        return render(request, 'Signin_Page.html')    
    

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')    


@login_required(login_url='signin')
def upload(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        new_post = Post.objects.create(profile=user_profile, user=user, image=image, caption=caption)
        new_post.save()
        
        return redirect('/')
    else:
        return redirect('/')
        

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.is_liked = 'True'
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.is_liked = 'False'
        post.save()
        return redirect('/')
    
    
    
@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    current_object = User.objects.get(username=request.user.username)
    current_profile = Profile.objects.get(user=current_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)  
    
    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow' 
        
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))    
    
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'current_object': current_object,
        'current_profile': current_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following
    }
    return render(request, 'profilePage.html', context)




@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')
    
    
@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})    



#Message Interpritation
@login_required(login_url='signin')
def chat(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    all_users = User.objects.all()
    
    new_suggestions_list = [x for x in list(all_users)]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    # random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))    
    
    context = {"user_profile": user_profile, "followings_list": suggestions_username_profile_list}
    return render(request, "ind_msg.html", context)


@login_required(login_url='signin')
def uog_chat(request, pk):
    user_object = User.objects.get(username=pk)
    friend = Profile.objects.get(user=user_object)
    
    user_object_current = User.objects.get(username=request.user.username)
    user_profile_sender = Profile.objects.get(user=user_object_current)
    
    form = ChatMessageForm()
    chats = ChatMessage.objects.all()
    rec_chats = ChatMessage.objects.filter(msg_sender=friend, msg_receiver=user_profile_sender)
    rec_chats.update(seen=True)
    
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user_profile_sender
            chat_message.msg_receiver = friend
            chat_message.save()
            return redirect("uog_chat", pk=friend)

    context = {"friend": friend, "form": form, "user":user_profile_sender, 
               "profile":profile, "chats": chats, "num": rec_chats.count()}

    return render(request, "detail_msg.html", context)


@login_required(login_url='signin')
def sentMessages(request, pk):
    user_object = User.objects.get(username=pk)
    friend = Profile.objects.get(user=user_object)
    
    user_object_current = User.objects.get(username=request.user.username)
    user_profile_sender = Profile.objects.get(user=user_object_current)
    
    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user_profile_sender, msg_receiver=friend, seen=False )
    return JsonResponse(new_chat_message.body, safe=False)


@login_required(login_url='signin')
def receivedMessages(request, pk):
    user_object = User.objects.get(username=pk)
    friend = Profile.objects.get(user=user_object)
    
    user_object_current = User.objects.get(username=request.user.username)
    user_profile_sender = Profile.objects.get(user=user_object_current)
    
    arr = []
    chats = ChatMessage.objects.filter(msg_sender=friend, msg_receiver=user_profile_sender)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr, safe=False)


@login_required(login_url='signin')
def chatNotification(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    all_users = User.objects.all()
    new_suggestions_list = [x for x in list(all_users)]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    
    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
    arr = []
    for friend in suggestions_username_profile_list:
        chats = ChatMessage.objects.filter(msg_sender__id=friend.id, msg_receiver=user_profile, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)
    

@login_required(login_url='signin')
def files(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
   
    files = Files.objects.all()
    
    if request.method == "POST":
        user = request.user.username
        pdf = request.FILES.get('pdf_file')
        title = request.POST['title']
        batch = request.POST.get('batch')
        department = request.POST.get('department')
        
        new_file = Files.objects.create(contributer=user_profile, user=user, pdf=pdf, title=title, batch=batch, department=department)
        new_file.save()
        
        return redirect('/files')
    
    
   
    context = {'user_profile': user_profile, 'files':files}
    return render(request, 'files.html', context)
    
    
def show(request, id):
    files = Files.objects.get(id=id)
    file_name = files.pdf
    return FileResponse(file_name, content_type='application/pdf') 
    
    