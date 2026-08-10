"""
Republic of Kandhla - Firebase Integration
REQUIREMENTS.md: 
- "Firebase Cloud Messaging (FCM) for targeted notifications (City/Mohalla topics)"
- "Firebase Real-time Database for instant Likes/Support counts without overloading Postgres"
"""

import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Firebase initialization flag
_firebase_initialized = False

def init_firebase():
    """Firebase SDK initialize karo."""
    global _firebase_initialized
    if _firebase_initialized:
        return True
        
    try:
        import firebase_admin
        from firebase_admin import credentials
        
        cred_path = settings.FIREBASE_CREDENTIALS_PATH
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': os.environ.get('FIREBASE_DATABASE_URL', 'https://kandhla-default-rtdb.firebaseio.com/')
            })
            _firebase_initialized = True
            logger.info("Firebase SDK initialized successfully.")
            return True
        else:
            logger.warning(f"Firebase credentials not found at {cred_path}. Firebase features will be disabled.")
            return False
    except ImportError:
        logger.warning("firebase-admin package not installed. Firebase features will be disabled.")
        return False
    except Exception as e:
        logger.error(f"Error initializing Firebase: {e}")
        return False


def send_fcm_notification(topic, title, body, data=None):
    """
    Topic (City ya Mohalla) based push notification send karo.
    """
    if not init_firebase():
        return False
        
    try:
        from firebase_admin import messaging
        
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            topic=topic,
        )
        
        response = messaging.send(message)
        logger.info(f"FCM notification sent to topic '{topic}': {response}")
        return True
    except Exception as e:
        logger.error(f"Failed to send FCM notification to '{topic}': {e}")
        return False


def sync_post_interactions_from_firebase():
    """
    Firebase Realtime Database se post interactions (likes/dislikes) read karke
    Postgres database mein sync karo.
    
    Ye function Celery task (sync_interaction_counts) se call hoga.
    """
    if not init_firebase():
        return False
        
    try:
        from firebase_admin import db
        from content.models import Post
        from django.db import transaction
        
        # Realtime DB structure: /interactions/posts/{post_id}/likes
        ref = db.reference('/interactions/posts')
        posts_data = ref.get()
        
        if not posts_data:
            return True
            
        updated = 0
        with transaction.atomic():
            for post_id, data in posts_data.items():
                try:
                    # Convert UUID string safely
                    likes = data.get('likes', 0)
                    dislikes = data.get('dislikes', 0)
                    
                    # Mass update query for efficiency
                    Post.objects.filter(id=post_id).update(
                        like_count=likes, 
                        dislike_count=dislikes
                    )
                    updated += 1
                except Exception as e:
                    logger.error(f"Failed to sync interactions for post {post_id}: {e}")
                    
        logger.info(f"Successfully synced interactions for {updated} posts from Firebase.")
        return True
    except Exception as e:
        logger.error(f"Firebase Realtime DB sync failed: {e}")
        return False
