"""
Republic of Kandhla - Content Serializers
Post aur Concern ke DRF serializers.
Feed system, content creation, aur interaction handling.
"""

from rest_framework import serializers
from content.models import Post, Concern
from accounts.serializers import UserMinimalSerializer


class PostSerializer(serializers.ModelSerializer):
    """
    Post read serializer — feed display ke liye.
    Anonymous posts mein author info hidden hota hai.
    """
    author = serializers.SerializerMethodField()
    mohalla_name = serializers.CharField(source='mohalla.name', read_only=True)
    post_type_display = serializers.CharField(source='get_post_type_display', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'mohalla',
            'mohalla_name',
            'content_text',
            'image_url',
            'post_type',
            'post_type_display',
            'is_anonymous',
            'created_at',
        ]
        read_only_fields = fields

    def get_author(self, obj):
        """
        Anonymous posts mein author info hide karo.
        REQUIREMENTS.md: "Option to report illegal activities anonymously
        (visible as anonymous post to public, tracked by Admin/SM)"
        """
        request = self.context.get('request')
        if obj.is_anonymous:
            # Admin aur Supreme Minister ko actual author dikhega
            if request and request.user.is_authenticated:
                from accounts.models import User
                if request.user.is_staff or request.user.role == User.Role.SUPREME_MINISTER:
                    user_data = UserMinimalSerializer(obj.user).data
                    user_data['_note'] = 'Anonymous post — sirf Admin/SM ko visible'
                    return user_data
            return {
                'id': None,
                'name': 'Anonymous Whistleblower',
                'avatar_url': '',
                'role': 'anonymous',
                'role_display': 'Anonymous',
                'credibility_score': None,
            }
        return UserMinimalSerializer(obj.user).data


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Post create serializer.
    SCHEMA.md: POST /api/posts/create/
    REQUIREMENTS.md: "Validates against profanity filter and checks
    minister permissions for official orders."
    """

    class Meta:
        model = Post
        fields = [
            'mohalla',
            'content_text',
            'image_url',
            'post_type',
            'is_anonymous',
        ]

    def validate_content_text(self, value):
        """
        Profanity filter check.
        REQUIREMENTS.md: "Regex-based bad-word block list managed via Admin panel."
        """
        if value:
            from kandhla.profanity import check_profanity
            is_profane, matched_words = check_profanity(value)
            if is_profane:
                raise serializers.ValidationError(
                    f'Content mein inappropriate words detected: {", ".join(matched_words)}. '
                    f'Isko hatao aur dobara try karo.'
                )
        return value

    def validate_post_type(self, value):
        """
        Official order aur announcement sirf ministers post kar sakte hain.
        REQUIREMENTS.md: "checks minister permissions for official orders."
        """
        request = self.context.get('request')
        if not request:
            return value

        user = request.user
        from accounts.models import User

        if value == Post.PostType.OFFICIAL_ORDER:
            if user.role not in (User.Role.SUPREME_MINISTER, User.Role.CITY_MINISTER, User.Role.MOHALLA_MINISTER):
                raise serializers.ValidationError(
                    'Official Orders sirf Ministers post kar sakte hain.'
                )

        if value == Post.PostType.ANNOUNCEMENT:
            if not user.is_staff and user.role != User.Role.SUPREME_MINISTER:
                raise serializers.ValidationError(
                    'Announcements sirf Admin ya Supreme Minister pin kar sakta hai.'
                )

        if value == Post.PostType.AD:
            if not user.is_staff:
                raise serializers.ValidationError(
                    'Ads sirf Admin panel se create hote hain.'
                )

        return value

    def validate(self, data):
        """
        Post mein kam se kam text ya image honi chahiye.
        Achaar Sanhita active hone par posting disabled.
        """
        content_text = data.get('content_text')
        image_url = data.get('image_url')

        if not content_text and not image_url:
            raise serializers.ValidationError(
                'Post mein kam se kam text ya image honi chahiye.'
            )

        # Achaar Sanhita check
        mohalla = data.get('mohalla')
        if mohalla and mohalla.city.is_code_of_conduct_active:
            request = self.context.get('request')
            user = request.user if request else None
            # Admin aur Supreme Minister exempt hain
            if user and not user.is_staff:
                from accounts.models import User
                if user.role != User.Role.SUPREME_MINISTER:
                    raise serializers.ValidationError(
                        'Achaar Sanhita (Code of Conduct) active hai — posting abhi disabled hai.'
                    )

        return data

    def create(self, validated_data):
        """Post create karte waqt user auto-set hoga."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ConcernSerializer(serializers.ModelSerializer):
    """
    Concern (Samasya) read serializer — issue display ke liye.
    """
    raised_by = UserMinimalSerializer(source='user', read_only=True)
    mohalla_name = serializers.CharField(source='mohalla.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    net_support = serializers.IntegerField(read_only=True)

    class Meta:
        model = Concern
        fields = [
            'id',
            'raised_by',
            'mohalla',
            'mohalla_name',
            'image_url',
            'description',
            'status',
            'status_display',
            'support_count',
            'do_not_support_count',
            'net_support',
            'created_at',
        ]
        read_only_fields = fields


class ConcernCreateSerializer(serializers.ModelSerializer):
    """
    Concern create serializer.
    REQUIREMENTS.md: "Users can raise issues with images and details."
    Image zaroori hai concern mein.
    """

    class Meta:
        model = Concern
        fields = ['mohalla', 'image_url', 'description']

    def validate_description(self, value):
        """Profanity filter on description."""
        if value:
            from kandhla.profanity import check_profanity
            is_profane, matched_words = check_profanity(value)
            if is_profane:
                raise serializers.ValidationError(
                    f'Description mein inappropriate words detected: {", ".join(matched_words)}. '
                    f'Isko hatao aur dobara try karo.'
                )
        return value

    def create(self, validated_data):
        """Concern create karte waqt user auto-set hoga."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class InteractionSerializer(serializers.Serializer):
    """
    Like/Dislike/Support interaction serializer.
    SCHEMA.md: POST /api/interactions/vote/
    REQUIREMENTS.md: Cross-Mohalla users can Like/Dislike/Support
    but Commenting is strictly blocked.
    """
    INTERACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('support', 'Support'),
        ('do_not_support', 'Do Not Support'),
    ]
    TARGET_TYPE_CHOICES = [
        ('post', 'Post'),
        ('concern', 'Concern'),
    ]

    target_type = serializers.ChoiceField(
        choices=TARGET_TYPE_CHOICES,
        help_text='Post ya Concern pe interaction',
    )
    target_id = serializers.UUIDField(
        help_text='Post/Concern ka UUID',
    )
    action = serializers.ChoiceField(
        choices=INTERACTION_CHOICES,
        help_text='Like, Dislike, Support, ya Do Not Support',
    )

    def validate(self, data):
        """Target exist karta hai ya nahi check karo."""
        target_type = data['target_type']
        target_id = data['target_id']

        if target_type == 'post':
            if not Post.objects.filter(id=target_id).exists():
                raise serializers.ValidationError({'target_id': 'Post not found.'})
            # Support/Do Not Support sirf Concern ke liye
            if data['action'] in ('support', 'do_not_support'):
                raise serializers.ValidationError({
                    'action': 'Support/Do Not Support sirf Concerns ke liye hai.'
                })
        elif target_type == 'concern':
            if not Concern.objects.filter(id=target_id).exists():
                raise serializers.ValidationError({'target_id': 'Concern not found.'})
            # Like/Dislike sirf Post ke liye
            if data['action'] in ('like', 'dislike'):
                raise serializers.ValidationError({
                    'action': 'Like/Dislike sirf Posts ke liye hai.'
                })

        return data
