"""
PyCon Togo 2025 - Schedule Data Handler
Processes JSON schedule data for display
"""

import json
import os
from datetime import datetime
from pathlib import Path
from app.utils.logger import setup_logger

logger = setup_logger()

DATA_DIR = Path('app/database')  # Directory where schedule.json is located

SCHEDULE_FILE_PATH = DATA_DIR / 'schedule.json'


logger.info(f"Loading schedule data from: {SCHEDULE_FILE_PATH}")


def load_schedule_json():
    """Load schedule data from external JSON file"""
    try:

        with open(SCHEDULE_FILE_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(
            f"schedule.json not found at {SCHEDULE_FILE_PATH}. Returning empty schedule.")

        return {"schedule": []}
    except json.JSONDecodeError as e:

        logger.error(f"Error parsing JSON: {e}")
        return {"schedule": []}
    except Exception as e:
        logger.error(f"Error loading schedule data: {e}")
        return {"schedule": []}


def calculate_duration(start_time, end_time):
    """Calculate duration in minutes from start and end times"""
    try:
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0


def get_fallback_description(item, description_type='short'):
    """Generate fallback descriptions when not provided in JSON"""
    fallbacks = {
        'talks': {
            'short': f"Présentation technique sur {item.get('title', 'Python')}",
            'full': f"Présentation technique détaillée sur {item.get('title', 'les technologies Python')}."
        },
        'lightning_talks': {
            'short': f"Lightning talk de 5 minutes",
            'full': f"Présentation courte et dynamique de 5 minutes."
        },
        'keynote': {
            'short': f"Conférence d'ouverture par {item.get('speaker', 'Invité spécial')}",
            'full': f"Conférence d'ouverture présentée par {item.get('speaker', 'Invité spécial')}."
        },
        'sponsor_session': {
            'short': f"Présentation de nos sponsors et partenaires",
            'full': f"Session dédiée à nos sponsors et partenaires qui soutiennent PyCon Togo 2025."
        },
        'break': {
            'short': f"Temps de pause pour se restaurer et échanger",
            'full': f"Moment convivial pour se détendre et échanger avec les autres participants."
        },
        'opening': {
            'short': f"Ouverture officielle par {item.get('speaker', 'l\'équipe organisatrice')}",
            'full': f"Ouverture officielle de PyCon Togo 2025 par {item.get('speaker', 'l\'équipe organisatrice')}."
        },
        'closing': {
            'short': f"Clôture officielle par {item.get('speaker', 'l\'équipe organisatrice')}",
            'full': f"Clôture officielle de PyCon Togo 2025 par {item.get('speaker', 'l\'équipe organisatrice')}."
        }
    }

    session_type = item.get('type', 'session')
    return fallbacks.get(session_type, {}).get(description_type, f"Session {item.get('title', 'sans titre')}")


def create_individual_talk_session(talk, parent_session, talk_index):
    """Create an individual session for a single talk"""
    start_time = talk.get('start', parent_session.get('start', ''))
    end_time = talk.get('end', parent_session.get('end', ''))

    # Calculate duration for individual talk
    if start_time and end_time:
        duration = calculate_duration(start_time, end_time)
    elif talk.get('duration'):
        # Extract minutes from duration string like "5min"
        duration_str = talk.get('duration', '20min')
        duration = int(''.join(filter(str.isdigit, duration_str))
                       ) if duration_str else 20
    else:
        duration = 20  # Default duration

    session_id = f"{start_time.replace(':', '') if start_time else parent_session['start'].replace(':', '')}-talk-{talk_index}"

    # Use talk description if available, otherwise create fallback
    description_full = talk.get(
        'description', f"Présentation '{talk['title']}' par {talk['speaker']}.")
    description_short = description_full[:150] + \
        "..." if len(description_full) > 150 else description_full

    session_data = {
        'id': session_id,
        'title': talk['title'],
        'subtitle': f"par {talk['speaker']}",
        'start_time': start_time,
        'end_time': end_time,
        'duration': duration,
        'type': 'session',
        'description_short': description_short,
        'description_full': description_full,
        'speakers': [talk['speaker']],
        'participant_count': 1,
        'participant_label': 'speaker',
        'talks': [talk],  # Keep the talk data for modal
        'parent_session_type': parent_session.get('type', 'talks'),
        # CORRECTION: Ajout de l'avatar_url
        'avatar_url': talk.get('avatar_url'),
        'language': talk.get('language', parent_session.get('language', []))
    }

    return session_data


def handle_panel_session(item, session_id, duration):
    """Handle panel sessions with multiple speakers"""
    speakers_list = []
    avatar_urls = []
    speaker_details = []

    if isinstance(item.get('speaker'), list):
        # Panel with multiple speakers
        for speaker_info in item['speaker']:
            if isinstance(speaker_info, dict):
                speakers_list.append(speaker_info.get('name', ''))
                avatar_url = speaker_info.get('avatar_url')
                avatar_urls.append(avatar_url if avatar_url else None)
                # Stocker les détails complets du speaker
                speaker_details.append({
                    'name': speaker_info.get('name', ''),
                    'avatar_url': avatar_url,
                    'title': speaker_info.get('title', ''),
                    'description': speaker_info.get('description', '')
                })
            else:
                speakers_list.append(str(speaker_info))
                avatar_urls.append(None)
                speaker_details.append({
                    'name': str(speaker_info),
                    'avatar_url': None,
                    'title': '',
                    'description': ''
                })

    participant_count = len(speakers_list)
    participant_label = 'panelistes'

    # Use first avatar for display, or None if no avatars
    main_avatar = avatar_urls[0] if avatar_urls else None

    return speakers_list, participant_count, participant_label, main_avatar, avatar_urls, speaker_details


def transform_json_to_schedule_format(json_data):
    """Transform JSON schedule data to the format expected by the template"""
    schedule_items = []

    for item in json_data.get('schedule', []):
        # Handle sessions with multiple talks - break them down into individual sessions
        if item.get('type') in ['talks', 'lightning_talks'] and item.get('talks'):
            talks = item.get('talks', [])

            # Create individual session for each talk
            for i, talk in enumerate(talks):
                individual_session = create_individual_talk_session(
                    talk, item, i)
                schedule_items.append(individual_session)

        else:
            # Handle single sessions (breaks, keynotes, opening, closing, sponsor sessions, panels)
            session_id = f"{item['start'].replace(':', '')}-{item.get('type', 'session')}"
            duration = calculate_duration(item['start'], item['end'])

            # Handle panel sessions specially
            if item.get('type') == 'panel':
                speakers, participant_count, participant_label, main_avatar, all_avatars, speaker_details = handle_panel_session(
                    item, session_id, duration)
                session_type = 'session'
            else:
                # Initialize default values
                all_avatars = []
                speaker_details = []

                # Determine session type and styling for other sessions
                if item.get('type') == 'break':
                    session_type = 'break'
                    participant_count = 0
                    speakers = []
                    participant_label = ''
                    main_avatar = None
                elif item.get('type') in ['opening', 'closing']:
                    session_type = 'compact'
                    participant_count = 1 if item.get('speaker') else 0
                    speakers = [item.get('speaker', '')] if item.get(
                        'speaker') else []
                    participant_label = 'speaker' if item.get(
                        'speaker') else ''
                    main_avatar = item.get('avatar_url')
                elif item.get('type') == 'keynote':
                    session_type = 'session'
                    participant_count = 1
                    speakers = [item.get('speaker', 'Keynote Speaker')]
                    participant_label = 'speaker'
                    main_avatar = item.get('avatar_url')
                elif item.get('type') == 'sponsor_session':
                    session_type = 'session'
                    participants = item.get('participants', [])
                    participant_count = len(participants)
                    speakers = participants
                    participant_label = 'participants'
                    main_avatar = item.get('avatar_url')
                elif item.get('type') in ['lightning', 'standard', 'deep-dive']:
                    # CORRECTION: Gestion des sessions avec multiples speakers (pas seulement panels)
                    session_type = 'session'

                    # Vérifier si c'est un array de speakers (comme pour les panels mais sans être panel)
                    if isinstance(item.get('speaker'), list):
                        speakers_list = []
                        avatar_urls = []
                        speaker_details_list = []

                        for speaker_info in item['speaker']:
                            if isinstance(speaker_info, dict):
                                speakers_list.append(
                                    speaker_info.get('name', ''))
                                avatar_url = speaker_info.get('avatar_url')
                                avatar_urls.append(
                                    avatar_url if avatar_url else None)
                                # Stocker les détails complets du speaker
                                speaker_details_list.append({
                                    'name': speaker_info.get('name', ''),
                                    'avatar_url': avatar_url,
                                    'title': speaker_info.get('title', ''),
                                    'description': speaker_info.get('description', '')
                                })
                            else:
                                speakers_list.append(str(speaker_info))
                                avatar_urls.append(None)
                                speaker_details_list.append({
                                    'name': str(speaker_info),
                                    'avatar_url': None,
                                    'title': '',
                                    'description': ''
                                })

                        speakers = speakers_list
                        participant_count = len(speakers_list)
                        participant_label = 'speakers' if len(
                            speakers_list) > 1 else 'speaker'
                        main_avatar = avatar_urls[0] if avatar_urls else None
                        all_avatars = avatar_urls
                        speaker_details = speaker_details_list
                    else:
                        # Un seul speaker
                        participant_count = 1 if item.get('speaker') else 0
                        speakers = [item.get('speaker')] if item.get(
                            'speaker') else []
                        participant_label = 'speaker'
                        main_avatar = item.get('avatar_url')
                else:
                    session_type = 'session'

                    # Gestion générale des multiples speakers pour tous les autres types
                    if isinstance(item.get('speaker'), list):
                        speakers_list = []
                        avatar_urls = []
                        speaker_details_list = []

                        for speaker_info in item['speaker']:
                            if isinstance(speaker_info, dict):
                                speakers_list.append(
                                    speaker_info.get('name', ''))
                                avatar_url = speaker_info.get('avatar_url')
                                avatar_urls.append(
                                    avatar_url if avatar_url else None)
                                speaker_details_list.append({
                                    'name': speaker_info.get('name', ''),
                                    'avatar_url': avatar_url,
                                    'title': speaker_info.get('title', ''),
                                    'description': speaker_info.get('description', '')
                                })
                            else:
                                speakers_list.append(str(speaker_info))
                                avatar_urls.append(None)
                                speaker_details_list.append({
                                    'name': str(speaker_info),
                                    'avatar_url': None,
                                    'title': '',
                                    'description': ''
                                })

                        speakers = speakers_list
                        participant_count = len(speakers_list)
                        participant_label = 'speakers' if len(
                            speakers_list) > 1 else 'speaker'
                        main_avatar = avatar_urls[0] if avatar_urls else None
                        all_avatars = avatar_urls
                        speaker_details = speaker_details_list
                    else:
                        participant_count = 1 if item.get('speaker') else 0
                        speakers = [item.get('speaker')] if item.get(
                            'speaker') else []
                        participant_label = 'speaker'
                        main_avatar = item.get('avatar_url')

            # Use JSON description if available, otherwise use fallback
            description_full = item.get(
                'description', get_fallback_description(item, 'full'))

            # Create short description (truncate full description or use fallback)
            if item.get('description'):
                description_short = item['description'][:150] + "..." if len(
                    item['description']) > 150 else item['description']
            else:
                description_short = get_fallback_description(item, 'short')

            session_data = {
                'id': session_id,
                'title': item.get('title', 'Session sans titre'),
                'subtitle': item.get('subtitle', ''),
                'start_time': item.get('start', ''),
                'end_time': item.get('end', ''),
                'duration': duration,
                'type': session_type,
                'description_short': description_short,
                'description_full': description_full,
                'speakers': speakers,
                'participant_count': participant_count,
                'participant_label': participant_label,
                # Keep original talks data for modal
                'talks': item.get('talks', []),
                'avatar_url': main_avatar,  # CORRECTION: Ajout de l'avatar_url principal
                # Pour tous les types de sessions avec multiples speakers
                'panel_avatars': all_avatars if all_avatars else [],
                # CORRECTION: Détails complets des speakers pour tous types
                'speaker_details': speaker_details if speaker_details else [],
                'language': item.get('language', [])
            }

            schedule_items.append(session_data)

    return schedule_items


def get_schedule():
    """Return the complete schedule data in the expected format"""
    json_data = load_schedule_json()
    return transform_json_to_schedule_format(json_data)


def get_speaker_images():
    """Return speaker images mapping from avatar URLs in JSON"""
    json_data = load_schedule_json()
    speaker_images = {}

    # Extract avatar URLs from JSON data
    for item in json_data.get('schedule', []):
        if 'talks' in item:
            for i, talk in enumerate(item['talks']):
                if talk.get('avatar_url'):
                    # Create unique keys for each speaker
                    start_time = talk.get('start', item.get('start', ''))
                    speaker_key = f"speaker_{start_time.replace(':', '')}_{i}"
                    speaker_images[speaker_key] = talk['avatar_url']

        # Handle single speaker sessions (keynotes, opening, closing, lightning, standard, deep-dive)
        if item.get('speaker') and item.get('avatar_url'):
            speaker_key = f"speaker_{item['start'].replace(':', '')}_main"
            speaker_images[speaker_key] = item['avatar_url']

    return speaker_images


def get_event_info():
    """Return general event information from JSON"""
    json_data = load_schedule_json()
    return {
        'event': json_data.get('event', 'PyCon Togo 2025'),
        'date': json_data.get('date', '2025-08-20'),
        'location': json_data.get('location', 'Lomé, Togo'),
        'timezone': json_data.get('timezone', 'GMT')
    }
