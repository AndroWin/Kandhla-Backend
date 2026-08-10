"""
Republic of Kandhla - Election Celery Tasks
REQUIREMENTS.md ke mutabiq automated workflows:
- Election phase auto-shifts (Nomination → Allocation → Campaign → ... → Completed)
- Achaar Sanhita (Code of Conduct) enforcement — posting auto-disable
- Vote queue processing from Redis
- City election: 3 months cycle, Mohalla election: 1 month cycle
"""

import json
import logging
from datetime import timedelta
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.db.models import F

logger = logging.getLogger(__name__)


# ============================================================
# ELECTION PHASE AUTO-SHIFT TASKS
# ============================================================

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def advance_election_phase(self, election_id):
    """
    Election ko next phase mein automatically shift karo.
    REQUIREMENTS.md ke mutabiq phase timeline:
    
    City Election (Supreme Minister - Every 3 Months):
    Day 1-5: Nomination → Day 6: Allocation → Day 6-10: Campaign →
    Day 11: Achaar Sanhita → Day 12-13: Voting → Day 14: Counting → Completed
    
    Mohalla Election (Mohalla Minister - Every 1 Month):
    Day 1-2: Nomination → Day 3: Allocation → Day 4-8: Campaign →
    Day 9: Achaar Sanhita → Day 10: Voting/Counting → Completed
    """
    from election.models import Election

    try:
        election = Election.objects.select_related('city', 'mohalla').get(id=election_id)
    except Election.DoesNotExist:
        logger.error(f"Election {election_id} not found for phase advance.")
        return f"Election {election_id} not found."

    if election.phase == Election.Phase.COMPLETED:
        logger.info(f"Election {election_id} already completed. Skipping.")
        return f"Election {election_id} already completed."

    old_phase = election.phase
    new_phase = _get_next_phase(old_phase)

    if not new_phase:
        logger.warning(f"No next phase defined for {old_phase}.")
        return f"No next phase for {old_phase}."

    with transaction.atomic():
        election.phase = new_phase
        election.save(update_fields=['phase'])

        # Achaar Sanhita activation/deactivation
        if new_phase == Election.Phase.CODE_OF_CONDUCT:
            _activate_achaar_sanhita(election)
        elif old_phase == Election.Phase.CODE_OF_CONDUCT:
            # Achaar Sanhita se voting mein shift — sanhita active rahegi voting tak
            pass
        elif new_phase == Election.Phase.COMPLETED:
            _deactivate_achaar_sanhita(election)
            _declare_results(election)

    logger.info(
        f"Election {election_id} phase shifted: {old_phase} → {new_phase}"
    )

    # Next phase shift schedule karo
    if new_phase != Election.Phase.COMPLETED:
        delay_seconds = _get_phase_duration_seconds(
            new_phase, election.election_type
        )
        advance_election_phase.apply_async(
            args=[str(election_id)],
            countdown=delay_seconds,
        )
        logger.info(
            f"Next phase shift scheduled in {delay_seconds}s for election {election_id}"
        )

    return f"Election {election_id}: {old_phase} → {new_phase}"


def _get_next_phase(current_phase):
    """Current phase se next phase return karo."""
    from election.models import Election
    phase_order = [
        Election.Phase.NOMINATION,
        Election.Phase.ALLOCATION,
        Election.Phase.CAMPAIGN,
        Election.Phase.CODE_OF_CONDUCT,
        Election.Phase.VOTING,
        Election.Phase.COUNTING,
        Election.Phase.COMPLETED,
    ]
    try:
        current_index = phase_order.index(current_phase)
        if current_index < len(phase_order) - 1:
            return phase_order[current_index + 1]
    except ValueError:
        pass
    return None


def _get_phase_duration_seconds(phase, election_type):
    """
    Phase ki duration seconds mein return karo.
    REQUIREMENTS.md ke mutabiq timeline.
    """
    from election.models import Election

    # City Election durations (in seconds)
    city_durations = {
        Election.Phase.NOMINATION: 5 * 24 * 3600,       # 5 days
        Election.Phase.ALLOCATION: 1 * 24 * 3600,       # 1 day
        Election.Phase.CAMPAIGN: 4 * 24 * 3600,          # 4 days
        Election.Phase.CODE_OF_CONDUCT: 1 * 24 * 3600,  # 1 day
        Election.Phase.VOTING: 2 * 24 * 3600,            # 2 days
        Election.Phase.COUNTING: 1 * 24 * 3600,          # 1 day
    }

    # Mohalla Election durations (in seconds)
    mohalla_durations = {
        Election.Phase.NOMINATION: 2 * 24 * 3600,       # 2 days
        Election.Phase.ALLOCATION: 1 * 24 * 3600,       # 1 day
        Election.Phase.CAMPAIGN: 4 * 24 * 3600,          # 4 days (Day 4-8, so ~5 but overlap)
        Election.Phase.CODE_OF_CONDUCT: 1 * 24 * 3600,  # 1 day
        Election.Phase.VOTING: 1 * 24 * 3600,            # 1 day (voting + counting same day)
        Election.Phase.COUNTING: 4 * 3600,               # 4 hours (quick counting)
    }

    if election_type == Election.ElectionType.CITY:
        return city_durations.get(phase, 24 * 3600)
    else:
        return mohalla_durations.get(phase, 24 * 3600)


# ============================================================
# ACHAAR SANHITA (CODE OF CONDUCT) TASKS
# ============================================================

@shared_task(bind=True)
def activate_achaar_sanhita_task(self, city_id):
    """
    Achaar Sanhita (Code of Conduct) activate karo — posting disabled.
    REQUIREMENTS.md: "Code of Conduct applied automatically by Celery (Posting disabled)."
    """
    _activate_achaar_sanhita_by_city(city_id)
    return f"Achaar Sanhita activated for city {city_id}"


@shared_task(bind=True)
def deactivate_achaar_sanhita_task(self, city_id):
    """
    Achaar Sanhita deactivate karo — posting re-enabled.
    REQUIREMENTS.md: "Results declared, feed unlocked."
    """
    _deactivate_achaar_sanhita_by_city(city_id)
    return f"Achaar Sanhita deactivated for city {city_id}"


def _activate_achaar_sanhita(election):
    """Election ke city pe Achaar Sanhita laga do."""
    from ecosystem.models import City
    city = election.city
    city.is_code_of_conduct_active = True
    city.save(update_fields=['is_code_of_conduct_active'])
    logger.info(f"Achaar Sanhita ACTIVATED for {city.name}")


def _deactivate_achaar_sanhita(election):
    """Election complete hone par Achaar Sanhita hata do."""
    from ecosystem.models import City
    city = election.city
    # Check karo ki koi aur active election toh nahi hai
    from election.models import Election
    other_active = Election.objects.filter(
        city=city,
    ).exclude(
        id=election.id,
    ).exclude(
        phase=Election.Phase.COMPLETED,
    ).exists()

    if not other_active:
        city.is_code_of_conduct_active = False
        city.save(update_fields=['is_code_of_conduct_active'])
        logger.info(f"Achaar Sanhita DEACTIVATED for {city.name}")
    else:
        logger.info(
            f"Achaar Sanhita still active for {city.name} — "
            f"other active elections exist."
        )


def _activate_achaar_sanhita_by_city(city_id):
    """City ID se Achaar Sanhita activate karo."""
    from ecosystem.models import City
    try:
        city = City.objects.get(id=city_id)
        city.is_code_of_conduct_active = True
        city.save(update_fields=['is_code_of_conduct_active'])
        logger.info(f"Achaar Sanhita ACTIVATED for {city.name}")
    except City.DoesNotExist:
        logger.error(f"City {city_id} not found for Achaar Sanhita activation.")


def _deactivate_achaar_sanhita_by_city(city_id):
    """City ID se Achaar Sanhita deactivate karo."""
    from ecosystem.models import City
    try:
        city = City.objects.get(id=city_id)
        city.is_code_of_conduct_active = False
        city.save(update_fields=['is_code_of_conduct_active'])
        logger.info(f"Achaar Sanhita DEACTIVATED for {city.name}")
    except City.DoesNotExist:
        logger.error(f"City {city_id} not found for Achaar Sanhita deactivation.")


# ============================================================
# ELECTION RESULTS & POST-ELECTION TASKS
# ============================================================

@shared_task(bind=True)
def declare_election_results(self, election_id):
    """
    Election results declare karo — winner determine, role assign.
    REQUIREMENTS.md:
    - Supreme Minister forms Cabinet of max 11 members
    - Mohalla Minister forms Cabinet of max 5 members
    """
    from election.models import Election
    try:
        election = Election.objects.get(id=election_id)
    except Election.DoesNotExist:
        logger.error(f"Election {election_id} not found for results declaration.")
        return

    _declare_results(election)
    return f"Results declared for election {election_id}"


def _declare_results(election):
    """
    Election ka winner determine karo aur role assign karo.
    """
    from accounts.models import User
    from election.models import Election

    # Top candidate (most votes) = winner
    winner_candidate = election.candidates.filter(
        is_approved=True,
    ).order_by('-vote_count').first()

    if not winner_candidate:
        logger.warning(f"No approved candidates in election {election.id}")
        return

    winner_user = winner_candidate.user

    with transaction.atomic():
        # Previous minister ka role reset karo
        if election.election_type == Election.ElectionType.CITY:
            # Purane Supreme Minister ko citizen banao
            User.objects.filter(
                city=election.city,
                role=User.Role.SUPREME_MINISTER,
            ).update(role=User.Role.CITIZEN)

            # Purane City Ministers ko bhi citizen banao
            User.objects.filter(
                city=election.city,
                role=User.Role.CITY_MINISTER,
            ).update(role=User.Role.CITIZEN)

            # Purana city cabinet deactivate karo
            from ecosystem.models import Cabinet
            Cabinet.objects.filter(
                city=election.city,
                is_active=True,
                mohalla__isnull=True,
            ).update(is_active=False)

            # Naye winner ko Supreme Minister banao
            winner_user.role = User.Role.SUPREME_MINISTER
            winner_user.save(update_fields=['role'])

            logger.info(
                f"🏛️ NEW SUPREME MINISTER: {winner_user.name} "
                f"for {election.city.name} with {winner_candidate.vote_count} votes!"
            )

        elif election.election_type == Election.ElectionType.MOHALLA:
            # Purane Mohalla Minister ko citizen banao
            User.objects.filter(
                mohalla=election.mohalla,
                role=User.Role.MOHALLA_MINISTER,
            ).update(role=User.Role.CITIZEN)

            # Purana mohalla cabinet deactivate karo
            from ecosystem.models import Cabinet
            Cabinet.objects.filter(
                mohalla=election.mohalla,
                is_active=True,
                city__isnull=True,
            ).update(is_active=False)

            # Naye winner ko Mohalla Minister banao
            winner_user.role = User.Role.MOHALLA_MINISTER
            winner_user.save(update_fields=['role'])

            logger.info(
                f"🏘️ NEW MOHALLA MINISTER: {winner_user.name} "
                f"for {election.mohalla.name} with {winner_candidate.vote_count} votes!"
            )


# ============================================================
# VOTE QUEUE PROCESSING (REDIS)
# ============================================================

@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def process_vote_queue(self):
    """
    Redis queue se vote payloads process karo.
    REQUIREMENTS.md: "routed via Redis queue to prevent traffic crashes"
    Ye task periodically Redis se votes read karke database mein confirm karta hai.
    """
    try:
        import redis
    except ImportError:
        logger.warning("Redis library not installed. Vote queue processing skipped.")
        return "Redis not available."

    try:
        redis_client = redis.from_url(settings.CELERY_BROKER_URL)
        queue_key = settings.KANDHLA_SETTINGS['VOTE_QUEUE_REDIS_KEY']

        processed = 0
        max_batch = 100  # Ek batch mein max 100 votes process karo

        while processed < max_batch:
            vote_data = redis_client.lpop(queue_key)
            if not vote_data:
                break

            try:
                payload = json.loads(vote_data)
                _process_single_vote(payload)
                processed += 1
            except (json.JSONDecodeError, Exception) as e:
                logger.error(f"Vote processing failed: {e}, payload: {vote_data}")
                continue

        if processed > 0:
            logger.info(f"Vote queue: {processed} votes processed successfully.")

        return f"Processed {processed} votes from queue."

    except redis.ConnectionError as e:
        logger.error(f"Redis connection failed: {e}")
        raise self.retry(exc=e)


def _process_single_vote(payload):
    """
    Single vote payload process karo — confirmation aur audit logging.
    Vote already database mein create ho chuka hai (CastVoteView mein),
    ye sirf confirmation aur additional processing ke liye hai.
    """
    vote_id = payload.get('vote_id')
    logger.debug(f"Vote {vote_id} confirmed via queue processing.")


# ============================================================
# SCHEDULED ELECTION CREATION
# ============================================================

@shared_task(bind=True)
def schedule_next_elections(self):
    """
    Automatically next election cycle schedule karo.
    REQUIREMENTS.md:
    - City Election: Every 3 months
    - Mohalla Election: Every 1 month
    
    Ye task Celery Beat se daily run hoga.
    """
    from election.models import Election
    from ecosystem.models import City, Mohalla

    now = timezone.now()
    created_elections = []

    # Saari cities check karo
    for city in City.objects.all():
        # City election check — kya last 90 din mein koi city election hui?
        last_city_election = Election.objects.filter(
            city=city,
            election_type=Election.ElectionType.CITY,
        ).order_by('-start_date').first()

        cycle_days = settings.KANDHLA_SETTINGS['CITY_ELECTION_CYCLE_DAYS']

        if not last_city_election or (
            last_city_election.phase == Election.Phase.COMPLETED
            and last_city_election.end_date
            and (now - last_city_election.end_date).days >= cycle_days
        ):
            # Nayi city election create karo
            new_election = Election.objects.create(
                city=city,
                election_type=Election.ElectionType.CITY,
                phase=Election.Phase.NOMINATION,
                start_date=now,
                end_date=now + timedelta(days=15),  # ~15 din ka cycle
            )
            created_elections.append(f"City: {city.name}")

            # Phase shift schedule karo
            advance_election_phase.apply_async(
                args=[str(new_election.id)],
                countdown=_get_phase_duration_seconds(
                    Election.Phase.NOMINATION,
                    Election.ElectionType.CITY,
                ),
            )

        # Mohalla elections check — har mohalla ke liye
        mohalla_cycle = settings.KANDHLA_SETTINGS['MOHALLA_ELECTION_CYCLE_DAYS']

        for mohalla in city.mohallas.all():
            last_mohalla_election = Election.objects.filter(
                city=city,
                mohalla=mohalla,
                election_type=Election.ElectionType.MOHALLA,
            ).order_by('-start_date').first()

            if not last_mohalla_election or (
                last_mohalla_election.phase == Election.Phase.COMPLETED
                and last_mohalla_election.end_date
                and (now - last_mohalla_election.end_date).days >= mohalla_cycle
            ):
                new_election = Election.objects.create(
                    city=city,
                    mohalla=mohalla,
                    election_type=Election.ElectionType.MOHALLA,
                    phase=Election.Phase.NOMINATION,
                    start_date=now,
                    end_date=now + timedelta(days=11),  # ~11 din ka cycle
                )
                created_elections.append(f"Mohalla: {mohalla.name}")

                advance_election_phase.apply_async(
                    args=[str(new_election.id)],
                    countdown=_get_phase_duration_seconds(
                        Election.Phase.NOMINATION,
                        Election.ElectionType.MOHALLA,
                    ),
                )

    if created_elections:
        logger.info(f"New elections scheduled: {', '.join(created_elections)}")

    return f"Scheduled {len(created_elections)} new elections."
