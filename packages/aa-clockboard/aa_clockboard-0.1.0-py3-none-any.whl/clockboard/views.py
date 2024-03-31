from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.db import transaction
from django.template.loader import render_to_string

from .models import Clock, ClockLog
from .forms import ResetClockForm, NewClockForm


def dashboard_clocks(request):
    clocks = (
        Clock.objects
        .filter(is_active=True)
        .select_related('last_reset_by__profile__main_character')
    )

    context = {
        'clocks': clocks,
    }

    return render_to_string('clockboard/dashboard_panel.html', context=context, request=request)


@login_required
@permission_required('clockboard.can_see_clocks')
def index(request):
    return redirect('clockboard:dashboard')


@login_required
@permission_required('clockboard.can_see_clocks')
def dashboard(request):
    clocks = (
        Clock.objects
        .filter(is_active=True)
        .select_related('last_reset_by__profile__main_character')
    )

    context = {
        'clocks': clocks,
    }

    return render(request, 'clockboard/clock_board.html', context=context)


@login_required
@permission_required('clockboard.can_see_clocks')
def reset_clock(request, clock_id: int):
    clock = get_object_or_404(Clock, pk=clock_id)

    if request.method == 'POST':
        form = ResetClockForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                clock.last_reset_by = request.user
                clock.last_reset = timezone.now()
                clock.save()

                ClockLog.objects.create(
                    clock=clock,
                    reset_by=request.user,
                    comment=form.cleaned_data['comment'],
                    num_involved=form.cleaned_data['num_involved'],
                    timestamp=clock.last_reset,
                )

            return redirect('clockboard:dashboard')
    else:
        form = ResetClockForm()

    context = {
        'form': form,
    }

    return render(request, 'clockboard/reset_clock.html', context=context)


@login_required
@permission_required('clockboard.can_add_clocks')
def new_clock(request):
    if request.method == 'POST':
        form = NewClockForm(request.POST)
        if form.is_valid():
            clock = form.save(commit=False)
            clock.last_reset_by = request.user
            clock.save()

            return redirect('clockboard:dashboard')
    else:
        form = NewClockForm()

    context = {
        'form': form,
    }

    return render(request, 'clockboard/new_clock.html', context=context)
