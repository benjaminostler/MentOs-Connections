from django.shortcuts import render, redirect
from .forms import UpdateProfileForm, CreateAccountForm, UpdateAccountForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.conf import settings


@login_required
def home(request):
    user_objs = Profile.objects.all()
    current_user = request.user  
       
    # Suggested Connections
    suggested_connections = []
    for u in user_objs:
        # if user has matching interest, is not current user, 
        # & status is open for connections(aka True),
        # add user to suggested contacts list
        if u.interest == current_user.profile.interest: 
            if current_user.username != u.user.username and u.status == True:
                if u.user.username not in current_user.profile.blocked_users:
                    if u.user.username not in current_user.profile.current_connections:
                        if current_user.username not in u.pending_connections and u.user.username not in current_user.profile.pending_connections:
                            # print(f'{u.user.username}')
                            suggested_connections.append(u)

    # Request Connection Button Functionality
    if request.method == 'POST' and 'request_connection' in request.POST:   
        other_user_profile = User.objects.get(username=request.POST["request_connection"])
        if current_user.username not in other_user_profile.profile.current_connections and other_user_profile.username not in current_user.profile.current_connections:
            if current_user.username not in other_user_profile.profile.pending_connections:
                # Add Current user to other user's pending_connections list
                other_user_profile.profile.pending_connections += f' {current_user.username}'
                # Remove from Current User's Suggested Connections
                suggested_connections.remove(other_user_profile.profile)
                other_user_profile.profile.save()
                current_user.profile.save()
    
    context = {
        'title': 'Home',
        'suggested_connections': suggested_connections,
        'pending_connections':  current_user.profile.pending_connections,
        'blocked_users': current_user.profile.blocked_users
    }
    return render(request, 'MentOS_app/index.html', context)


@login_required
def my_connections(request):
    
    current_user = request.user  
    
    # Pending Connections: Accept Connection Button Functionality
    if request.method == 'POST' and 'accept_connection' in request.POST:   
        other_user_profile = User.objects.get(username=request.POST["accept_connection"])
        if current_user.username not in other_user_profile.profile.current_connections and other_user_profile.username not in current_user.profile.current_connections:
            # 1) remove other user from current user's pending_connections list
            old_string = current_user.profile.pending_connections
            new_string = old_string.replace(other_user_profile.username, "")
            current_user.profile.pending_connections = new_string
            # 2) Add other user to current user's current_connections list
            current_user.profile.current_connections += f' {other_user_profile.username}'
            # 3) Add Current user to other user's current_connections list
            other_user_profile.profile.current_connections += f' {current_user.username}'
            other_user_profile.profile.save()
            current_user.profile.save()
    
    # Pending Connections: Cancel Request Button Functionality
    if request.method == 'POST' and 'cancel_request' in request.POST:
        other_user_profile = User.objects.get(username=request.POST["cancel_request"])
        if current_user.username not in other_user_profile.profile.current_connections: 
            # if other_user_profile.username in current_user.profile.pending_connections:
            # 1) remove current user from other user's pending_connections list
            old_string = other_user_profile.profile.pending_connections
            new_string = old_string.replace(current_user.username, "")
            other_user_profile.profile.pending_connections = new_string
            other_user_profile.profile.save()

    # Pending Connections: Decline Connection Button Functionality
    if request.method == 'POST' and 'decline_connection' in request.POST:   
        other_user_profile = User.objects.get(username=request.POST["decline_connection"])
        if  other_user_profile.username in current_user.profile.pending_connections:
            # 1) remove other user from current user's pending_connections list
            old_string = current_user.profile.pending_connections
            new_string = old_string.replace(other_user_profile.username, "")
            current_user.profile.pending_connections = new_string
            current_user.profile.save()

    # Current Connections: Disconnect Button Functionality
    if request.method == 'POST' and 'disconnect' in request.POST:   
        other_user_profile = User.objects.get(username=request.POST["disconnect"])
        if current_user.username in other_user_profile.profile.current_connections and other_user_profile.username in current_user.profile.current_connections:
            # 1) remove other user from current user's current_connections list
            old_string = current_user.profile.current_connections
            new_string = old_string.replace(other_user_profile.username, "")
            current_user.profile.current_connections = new_string
            # 2) remove current user from other user's current_connections list
            old_string_2 = other_user_profile.profile.current_connections
            new_string_2 = old_string_2.replace(current_user.username, "")
            other_user_profile.profile.current_connections = new_string_2
            other_user_profile.profile.save()
            current_user.profile.save()

    # Current Connections: Message Button Functionality
    if request.method == 'POST' and 'message' in request.POST:   
        other_user_profile = User.objects.get(username=request.POST["message"])
        return redirect(f"/send-email/{other_user_profile.username}/")

    user_objs = Profile.objects.all()
    # Current Connections: List for Display Purposes
    current_connections = []
    for u in user_objs:
        # if user is connected with current user, add to list
        if u.user.username in current_user.profile.current_connections:
            current_connections.append(u)

    # Pending Connections List for Display Purposes (Incoming Connection Requests)
    pending_connections = []
    for u in user_objs:
        # if current user has requested connection with user, add to list
        if u.user.username in current_user.profile.pending_connections:
            pending_connections.append(u)
        if current_user.username in u.pending_connections:
            pending_connections.append(u)
        
    context = {
        'title': 'My Connections', 
        'current_connections': current_connections,
        'pending_connections': pending_connections
    }
    return render(request, 'MentOS_app/my_connections.html', context)


def create_account(request):
    if request.method == 'POST':
        account_form = CreateAccountForm(request.POST)
        if account_form.is_valid():
            account_form.save()
            return redirect('/edit-profile')
    else:
        account_form = CreateAccountForm()
    context = {
        'title': 'MentOS - Create Mentor',
        'account_form': account_form,
    }
    return render(request, 'MentOS_app/create_account.html', context )


@login_required
def edit_profile(request):

    if request.method == 'POST':
        account_form = UpdateAccountForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, 
                                         request.FILES,
                                         instance=Profile.objects.get(user=request.user))
        if account_form.is_valid() and profile_form.is_valid():
            account_form.save()
            profile_form.save()
            return redirect('/')
    else:
        account_form = UpdateAccountForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    context = {
        'title': 'Edit Profile',
        'account_form': account_form,
        'profile_form': profile_form,
    }
    return render(request, 'MentOS_app/edit_profile.html', context)


@login_required
def delete_account(request):
    home_url = "{% url 'home' %}"
    if request.method == 'POST':
        print(f"\n\n\n\n{request.user}\n\n\n\n")
        request.user.delete()
        return redirect('/login/')
    context = {
        'title': 'Delete Account',
        'home': home_url,
    }
    return render(request, 'MentOS_app/delete_account.html', context)


@login_required
def view_other_profiles(request, username_parameter):
    user_obj = User.objects.get(username=username_parameter)
    other_user_profile = Profile.objects.get(user=user_obj)
    request_user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST' and 'rate_user' in request.POST:
        current_user = request.user
        rating = int(request.POST['star'])
        if current_user.username not in other_user_profile.list_of_raters:
            other_user_profile.total_rating += rating
            other_user_profile.number_of_raters += 1
            other_user_profile.list_of_raters += f" {current_user.username}"
            other_user_profile.save()
        return redirect(f"/view-other-profiles/{other_user_profile.user.username}/")
    
    if request.method == 'POST' and 'block_or_unblock_user' in request.POST:
        # Unblock
        if other_user_profile.user.username in request.user.profile.blocked_users:
            old_string = request_user_profile.blocked_users
            new_string = old_string.replace(other_user_profile.user.username, "")
            request_user_profile.blocked_users = new_string
            request_user_profile.save()
        # Block
        else: 
            request_user_profile.blocked_users += f" {other_user_profile.user.username}"
            request_user_profile.save()
        return redirect(f"/view-other-profiles/{other_user_profile.user.username}/")

    if request.method == 'POST' and 'connect_user' in request.POST:
        # Disconnect 
        if other_user_profile.user.username in request.user.profile.current_connections and request.user.username in other_user_profile.current_connections:
            # 1) remove other user from current user's current_connections list
            old_string = request_user_profile.current_connections
            new_string = old_string.replace(other_user_profile.user.username, "")
            request_user_profile.current_connections = new_string
            # 2) remove current user from other user's current_connections list
            old_string_2 = other_user_profile.current_connections
            new_string_2 = old_string_2.replace(request_user_profile.user.username, "")
            other_user_profile.current_connections = new_string_2
            other_user_profile.save()
            request_user_profile.save()
        # Accept Connection Request or Decline Connection Request
        elif other_user_profile.user.username not in request.user.profile.current_connections and request.user.username not in other_user_profile.current_connections and other_user_profile.user.username in request.user.profile.pending_connections:
            accept = request.POST['connect_user']
            print(f'\n\n\n{type(accept)}\n\n')
            # Accept
            if accept == '1':
                # 1) remove other user from current user's pending_connections list
                old_string = request_user_profile.pending_connections
                new_string = old_string.replace(other_user_profile.user.username, "")
                request_user_profile.pending_connections = new_string
                # 2) Add other user to current user's current_connections list
                request_user_profile.current_connections += f' {other_user_profile.user.username}'
                # 3) Add Current user to other user's current_connections list
                other_user_profile.current_connections += f' {request_user_profile.user.username}'
                other_user_profile.save()
                request_user_profile.save()
            elif accept == '0': 
                # 1) remove other user from current user's pending_connections list
                old_string = request_user_profile.pending_connections
                new_string = old_string.replace(other_user_profile.user.username, "")
                request_user_profile.pending_connections = new_string
                request_user_profile.save()
        # Cancel Connection Request
        elif other_user_profile.user.username not in request.user.profile.current_connections and request.user.username not in other_user_profile.current_connections and request.user.username in other_user_profile.pending_connections:
            old_string = other_user_profile.pending_connections
            new_string = old_string.replace(request_user_profile.user.username, "")
            other_user_profile.pending_connections = new_string
            other_user_profile.save()
        # Connect
        elif other_user_profile.status == True: 
            # Add Current user to other user's pending_connections list
            other_user_profile.pending_connections += f' {request_user_profile.user.username}'
            other_user_profile.save()
        return redirect(f"/view-other-profiles/{other_user_profile.user.username}/")

    try:
        rating_score = other_user_profile.total_rating / other_user_profile.number_of_raters
    except ZeroDivisionError:
        rating_score = 0
    
    context = {
        'title': 'View Other Users',
        'other_user_profile': other_user_profile,
        'rating_score': round(rating_score, 1),
    }
    return render(request, 'MentOS_app/view_other_profiles.html', context)


@login_required
def tips(request):
    context = {
        'title': 'Tips', 
    }
    return render(request, 'MentOS_app/tips.html', context)

@login_required
def room(request, room_name):
    context = {
        'title': 'Chat Room',
        'room_name': room_name
    }
    return render(request, 'MentOS_app/room.html', context)

@login_required
def send_email_to_user(request, username_parameter):
    user_obj = User.objects.get(username=username_parameter)
    other_user_profile = Profile.objects.get(user=user_obj)
    request_user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        subject = request.POST['emailSubject']
        body = request.POST['emailBody']
        subject = f"MentOS {request.user.username}: {subject}"
        body = f"You have a new email from the user: {request.user.first_name} {request.user.last_name}\n\n{body}"
        emailHost = settings.EMAIL_HOST_USER
        emailTo = other_user_profile.user.email

        send_mail(subject, body, emailHost, [emailTo], fail_silently=False)

        return redirect('/')

    context = {
        'title': f'Send Email To {username_parameter}',
        'other_user_profile': other_user_profile,
    }
    return render(request, 'MentOS_app/send_email.html', context)

@login_required
def select_chat_room(request):
    if request.method == 'POST':
        room_name = request.POST['room-name']
        return redirect(f'chat/{room_name}/')

    context = {
        'title': 'Select A Chat Room',
    }
    return render(request, 'MentOS_app/select_chat_room.html', context)
