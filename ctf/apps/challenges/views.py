from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from .models import Challenge, CATEGORY_CHOICES, CATEGORY_COLORS
from ctf.apps.submissions.models import Submission
from ctf.context_processors import CATEGORY_META
import json


@login_required
def challenge_list(request):
    challenges = Challenge.objects.filter(is_active=True)
    solved_ids = set(
        Submission.objects.filter(player=request.user, is_correct=True)
        .values_list('challenge_id', flat=True)
    )

    active_category = request.GET.get('category', '').strip().lower()
    valid_keys = [k for k, _ in CATEGORY_CHOICES]
    if active_category not in valid_keys:
        active_category = ''

    categories = {}
    for cat_key, cat_label in CATEGORY_CHOICES:
        cat_challenges = []
        for ch in challenges.filter(category=cat_key):
            cat_challenges.append({'obj': ch, 'solved': ch.id in solved_ids})
        if cat_challenges:
            meta = CATEGORY_META.get(cat_key, {})
            categories[cat_label] = {
                'key':         cat_key,
                'challenges':  cat_challenges,
                'color':       meta.get('color', '#888'),
                'icon':        meta.get('icon', ''),
                'description': meta.get('description', ''),
                'solved':      sum(1 for c in cat_challenges if c['solved']),
                'total':       len(cat_challenges),
            }

    filtered_categories = {}
    if active_category:
        for label, data in categories.items():
            if data['key'] == active_category:
                filtered_categories[label] = data
                break
    else:
        filtered_categories = categories

    active_category_label = ''
    active_category_color = ''
    if active_category:
        meta = CATEGORY_META.get(active_category, {})
        active_category_label = meta.get('label', active_category.title())
        active_category_color = meta.get('color', '#888')

    return render(request, 'challenges/list.html', {
        'categories':            filtered_categories,
        'all_categories':        categories,
        'active_category':       active_category,
        'active_category_label': active_category_label,
        'active_category_color': active_category_color,
        'total_solved':          len(solved_ids),
        'total_challenges':      challenges.count(),
    })


@login_required
def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk, is_active=True)
    is_solved = challenge.is_solved_by(request.user)
    attempts  = Submission.objects.filter(player=request.user, challenge=challenge).count()
    unlocked_hints = cache.get(f'hints:{request.user.id}:{pk}', [])

    return render(request, 'challenges/detail.html', {
        'challenge':      challenge,
        'is_solved':      is_solved,
        'attempts':       attempts,
        'unlocked_hints': unlocked_hints,
        'first_blood':    Submission.objects.filter(challenge=challenge, is_correct=True).order_by('submitted_at').first(),
    })


@login_required
@require_POST
def submit_flag(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk, is_active=True)

    if challenge.is_solved_by(request.user):
        return JsonResponse({'status': 'already_solved', 'message': 'You already solved this!'})

    rate_key = f'rate:{request.user.id}:{pk}'
    attempts_in_window = cache.get(rate_key, 0)
    if attempts_in_window >= settings.SUBMISSION_RATE_LIMIT:
        return JsonResponse({'status': 'rate_limited', 'message': f'Too many attempts. Wait {settings.SUBMISSION_RATE_WINDOW}s.'}, status=429)

    cooldown_key = f'cooldown:{request.user.id}:{pk}'
    if cache.get(cooldown_key):
        return JsonResponse({'status': 'cooldown', 'message': f'Wait {settings.SUBMISSION_COOLDOWN}s between submissions.'}, status=429)

    if challenge.max_attempts > 0:
        total_attempts = Submission.objects.filter(player=request.user, challenge=challenge).count()
        if total_attempts >= challenge.max_attempts:
            return JsonResponse({'status': 'max_attempts', 'message': 'Maximum attempts reached for this challenge.'})

    try:
        data = json.loads(request.body)
        submitted_flag = data.get('flag', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    if not submitted_flag:
        return JsonResponse({'status': 'error', 'message': 'Flag cannot be empty'})

    cache.set(rate_key, attempts_in_window + 1, timeout=settings.SUBMISSION_RATE_WINDOW)
    cache.set(cooldown_key, True, timeout=settings.SUBMISSION_COOLDOWN)

    is_correct = challenge.check_flag(submitted_flag)

    Submission.objects.create(
        player=request.user,
        challenge=challenge,
        submitted_flag=submitted_flag,
        is_correct=is_correct,
        ip_address=get_client_ip(request),
    )

    if is_correct:
        request.user.score += challenge.points
        request.user.last_solve_time = timezone.now()
        request.user.save(update_fields=['score', 'last_solve_time'])
        request.user.refresh_from_db()

        try:
            from ctf.apps.scoreboard.tasks import broadcast_scoreboard_update
            broadcast_scoreboard_update.delay()
        except Exception:
            pass

        return JsonResponse({'status': 'correct', 'message': f'Correct! +{challenge.points} points', 'points': challenge.points, 'new_score': request.user.score})
    else:
        return JsonResponse({'status': 'wrong', 'message': 'Wrong flag. Keep trying!'})


@login_required
@require_POST
def unlock_hint(request, pk, hint_index):
    challenge = get_object_or_404(Challenge, pk=pk, is_active=True)
    hints = challenge.hints

    if hint_index >= len(hints):
        return JsonResponse({'status': 'error', 'message': 'Hint not found'}, status=404)

    hint = hints[hint_index]
    cache_key = f'hints:{request.user.id}:{pk}'
    unlocked = cache.get(cache_key, [])

    if hint_index in unlocked:
        return JsonResponse({'status': 'already_unlocked', 'text': hint['text']})

    unlocked.append(hint_index)
    cache.set(cache_key, unlocked, timeout=None)
    return JsonResponse({'status': 'unlocked', 'text': hint['text'], 'cost': 0})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')
