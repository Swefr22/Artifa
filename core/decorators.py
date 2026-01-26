"""
Authentication decorators for student access control
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import Team, Participant


def student_login_required(view_func):
    """Decorator to ensure user is a logged-in student"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to continue.')
            return redirect('student_login')
        
        try:
            # Check if user has a participant profile
            request.user.participant_profile
        except Participant.DoesNotExist:
            messages.error(request, 'Your participant profile is not found.')
            return redirect('student_login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def team_leader_required(view_func):
    """Decorator to ensure user is the team leader"""
    @wraps(view_func)
    def wrapper(request, team_id, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to continue.')
            return redirect('student_login')
        
        try:
            team = Team.objects.get(id=team_id)
            participant = request.user.participant_profile
            
            if team.created_by != participant:
                messages.error(request, 'You do not have permission to manage this team.')
                return redirect('view_team', team_id=team_id)
        
        except (Team.DoesNotExist, Participant.DoesNotExist):
            messages.error(request, 'Team or participant not found.')
            return redirect('student_dashboard')
        
        return view_func(request, team_id, *args, **kwargs)
    
    return wrapper
