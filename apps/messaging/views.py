from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Conversation, Message
from .forms import MessageForm

User = get_user_model()

@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')
    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.order_by('created_at')
    
    # Determine the conversation title
    if conversation.job:
        conversation_title = f"Job: {conversation.job.title}"
    else:
        other_participant = conversation.participants.exclude(id=request.user.id).first()
        conversation_title = f"Chat with {other_participant.username}"
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            conversation.save()  # Update the 'updated_at' field
            return redirect('messaging:conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form,
        'conversation_title': conversation_title
    })

# If you're used to the other perspective I'm sorry :)
@login_required
def start_conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    
    # Check if there's an existing conversation without a job associated
    conversation = Conversation.objects.filter(
        participants=request.user,
        job__isnull=True
    ).filter(
        participants=other_user
    ).first()
    
    if not conversation:
        # If no existing conversation found, create a new one
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
    
    return redirect('messaging:conversation_detail', conversation_id=conversation.id)

