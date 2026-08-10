# Republic of City - Database Schema (PostgreSQL) & API Contract

## 1. PostgreSQL Database Models (Django ORM)

### User Table (`accounts_user`)
* `id` (UUID, Primary Key)
* `google_id` (String, Unique)
* `device_id` (String, Indexed - for anti-fraud voting)
* `email` (String, Unique)
* `name` (String)
* `avatar_url` (String)
* `city_id` (ForeignKey -> City)
* `mohalla_id` (ForeignKey -> Mohalla)
* `credibility_score` (Integer, Default: 100)
* `role` (String, Choices: `citizen`, `city_minister`, `mohalla_minister`, `supreme_minister`)
* `strike_count` (Integer, Default: 0)
* `ban_until` (DateTime, Nullable)
* `is_active` (Boolean, Default: True)
* `created_at` (DateTime)

### City Table (`ecosystem_city`)
* `id` (UUID, Primary Key)
* `name` (String, Unique - e.g., "Kandhla")
* `state` (String)
* `samvidhan_content` (HTML/RichText - managed via Django Admin)
* `is_code_of_conduct_active` (Boolean, Default: False)

### Mohalla Table (`ecosystem_mohalla`)
* `id` (UUID, Primary Key)
* `city_id` (ForeignKey -> City, Cascade)
* `name` (String - e.g., "Mohalla X")
* `population_count` (Integer, Default: 0)

### MohallaChangeRequest Table (`ecosystem_mohallarequest`)
* `id` (UUID, Primary Key)
* `user_id` (ForeignKey -> User)
* `target_mohalla_id` (ForeignKey -> Mohalla)
* `reason` (Text)
* `status` (String, Choices: `pending`, `approved`, `rejected`)
* `created_at` (DateTime)

### Post Table (`content_post`)
* `id` (UUID, Primary Key)
* `user_id` (ForeignKey -> User)
* `mohalla_id` (ForeignKey -> Mohalla)
* `content_text` (Text, Nullable)
* `image_url` (String, Nullable)
* `post_type` (String, Choices: `normal`, `announcement`, `ad`, `official_order`)
* `is_anonymous` (Boolean, Default: False)
* `created_at` (DateTime)

### Concern Table (`content_concern`)
* `id` (UUID, Primary Key)
* `user_id` (ForeignKey -> User)
* `mohalla_id` (ForeignKey -> Mohalla)
* `image_url` (String)
* `description` (Text)
* `status` (String, Choices: `pending`, `city_priority`, `resolved`)
* `support_count` (Integer, Default: 0)
* `do_not_support_count` (Integer, Default: 0)

### Election Table (`election_election`)
* `id` (UUID, Primary Key)
* `city_id` (ForeignKey -> City)
* `election_type` (String, Choices: `city`, `mohalla`)
* `phase` (String, Choices: `nomination`, `allocation`, `campaign`, `code_of_conduct`, `voting`, `counting`, `completed`)
* `start_date` (DateTime)
* `end_date` (DateTime)

### Candidate Table (`election_candidate`)
* `id` (UUID, Primary Key)
* `election_id` (ForeignKey -> Election)
* `user_id` (ForeignKey -> User)
* `manifesto` (Text)
* `symbol` (String - e.g., '🚲')
* `vote_count` (Integer, Default: 0)
* `is_approved` (Boolean, Default: False)

### Vote Table (`election_vote`) - *Strict Security*
* `id` (UUID, Primary Key)
* `election_id` (ForeignKey -> Election)
* `device_id` (String - ensures 1 device = 1 vote)
* `hashed_token` (String, Unique - prevents double voting)
* `created_at` (DateTime)

### Cabinet Table (`ecosystem_cabinet`)
* `id` (UUID, Primary Key)
* `user_id` (ForeignKey -> User)
* `city_id` (ForeignKey -> City, Nullable)
* `mohalla_id` (ForeignKey -> Mohalla, Nullable)
* `department_name` (String - e.g., "Home Minister", "Infra Head")
* `ruby_color` (String - e.g., "violet", "grey")
* `is_active` (Boolean, Default: True)

---

## 2. Core REST API Endpoints (Django REST Framework)

* **POST `/api/auth/google/`** -> Verifies Google token, checks device ID, returns JWT session token and user profile.
* **GET `/api/feed/{mohalla_id}/`** -> Fetches paginated posts for a specific mohalla (Pins admin announcements/ads at top).
* **POST `/api/posts/create/`** -> Creates a new post or concern. Validates against profanity filter and checks minister permissions for official orders.
* **POST `/api/interactions/vote/`** -> Handles Like/Dislike/Support updates.
* **POST `/api/election/nominate/`** -> Submits election nomination form (checks user Credibility Score >= 500).
* **POST `/api/ election/cast-vote/`** -> Pushes secure vote payload into Redis queue for backend processing.
* **GET `/api/system/samvidhan/{city_id}/`** -> Returns HTML content of the city's constitution.
* **GET `/api/team/engineered-by/`** -> Returns dynamic JSON array of core development team members for the 'Engineered By' screen.