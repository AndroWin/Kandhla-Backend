import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kandhla.settings")
django.setup()

from ecosystem.models import City, Mohalla
from accounts.models import User
from content.models import Post, Concern
from election.models import Election

def seed():
    print("Seeding database...")

    # Create City
    city, created = City.objects.get_or_create(
        name="Kandhla",
        defaults={
            "state": "Uttar Pradesh",
            "samvidhan_content": "<h1>Constitution of Kandhla</h1><p>Welcome to our city.</p>"
        }
    )
    if created:
        print(f"Created City: {city.name}")

    # Create Mohallas
    mohallas = ["Mohalla Qazi", "Mohalla Mirdgan", "Mohalla Sheikhzada"]
    for m_name in mohallas:
        mohalla, created = Mohalla.objects.get_or_create(
            name=m_name,
            city=city,
            defaults={"population_count": 500}
        )
        if created:
            print(f"Created Mohalla: {mohalla.name}")
            
    mohalla_qazi = Mohalla.objects.get(name="Mohalla Qazi")

    # Create Superuser (Supreme Minister)
    if not User.objects.filter(email="admin@kandhla.com").exists():
        admin = User.objects.create_superuser(
            email="admin@kandhla.com",
            name="City Admin",
            password="adminpassword123",
            city=city,
            mohalla=mohalla_qazi,
            role=User.Role.SUPREME_MINISTER,
        )
        print("Created Superuser: admin@kandhla.com")
    else:
        admin = User.objects.get(email="admin@kandhla.com")

    # Create a regular user
    if not User.objects.filter(email="citizen@kandhla.com").exists():
        citizen = User.objects.create_user(
            email="citizen@kandhla.com",
            name="Aam Aadmi",
            city=city,
            mohalla=mohalla_qazi,
            google_id="dummy_google_123"
        )
        print("Created Citizen: citizen@kandhla.com")
    else:
        citizen = User.objects.get(email="citizen@kandhla.com")

    # Create dummy post
    if not Post.objects.filter(mohalla=mohalla_qazi).exists():
        Post.objects.create(
            user=admin,
            mohalla=mohalla_qazi,
            content_text="Welcome to the digital Republic of Kandhla! This is our first post.",
            post_type=Post.PostType.ANNOUNCEMENT
        )
        Post.objects.create(
            user=citizen,
            mohalla=mohalla_qazi,
            content_text="Hello everyone! Excited to join this platform.",
            post_type=Post.PostType.NORMAL
        )
        print("Created Initial Posts.")

    # Create dummy concern
    if not Concern.objects.filter(mohalla=mohalla_qazi).exists():
        Concern.objects.create(
            user=citizen,
            mohalla=mohalla_qazi,
            image_url="https://via.placeholder.com/400x300.png?text=Broken+Road",
            description="The main road in Mohalla Qazi has huge potholes. Needs immediate attention.",
            support_count=5,
            do_not_support_count=1
        )
        print("Created Initial Concern.")
        
    print("Seeding complete! Database is populated with dummy data.")

if __name__ == "__main__":
    seed()
