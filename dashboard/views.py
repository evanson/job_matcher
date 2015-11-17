from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings

from forms import LoginForm


def server_error(request, msg=None):
    if msg is None:
        msg = "Sorry! We screwed up. We're looking into it"
    print "server_error: %s" %(msg)
    messages.error(request, msg)
    tmpl_messages = messages.get_messages(request)
    return render_to_response('500.html', {'messages': tmpl_messages})

    
def index(request):
    try:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('profile'))
        else:
            if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                    username = form.data['username']
                    password = form.data['password']
                    
                    print "index: Login: Authenticating User [%s] ..." %(username)
                    user = authenticate(username=username, password=password)
                    print "index: Login: User [%s] successfully authenticated." %(username)
                
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            print "index: Login: User [%s] successfully logged in." %(username)
                            return HttpResponseRedirect(reverse('profile'))
                        else:
                            messages.error(request,
                                            "Login Account for User [%s] is currently disabled." %(username))
                            form = LoginForm()
                            return render_to_response('index.html',
                                                        {'form': form, },
                                                        context_instance=RequestContext(request))
                    else:
                        messages.error(request, "Incorrect username (%s) or password." %(username))
                        form = LoginForm()
                        return render_to_response('index.html', {'form': form},
                                                  context_instance=RequestContext(request))
            else:
                logout(request)
                form = LoginForm()
            return render_to_response('index.html', {'form': form},
                                        context_instance=RequestContext(request))
    except Exception,e:
        print str(e)
        screenmessage = "Sorry! We screwed up. We're looking into it"
        return server_error(request, screenmessage)
