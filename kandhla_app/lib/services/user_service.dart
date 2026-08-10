import 'api_service.dart';

class UserProfile {
  final String id;
  final String name;
  final String role;
  final int credibilityScore;
  final String? profileImage;
  final int postsCount;
  final int supportedCount;

  UserProfile({
    required this.id,
    required this.name,
    required this.role,
    required this.credibilityScore,
    this.profileImage,
    required this.postsCount,
    required this.supportedCount,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      id: json['id'] ?? '',
      name: json['name'] ?? 'Citizen',
      role: json['role'] ?? 'citizen',
      credibilityScore: json['credibility_score'] ?? 0,
      profileImage: json['profile_image'],
      postsCount: json['posts_count'] ?? 0,
      supportedCount: json['supported_count'] ?? 0,
    );
  }
}

class UserService {
  final ApiService _apiService = ApiService();

  Future<UserProfile?> fetchMyProfile() async {
    try {
      final response = await _apiService.client.get('auth/profile/');
      if (response.statusCode == 200) {
        return UserProfile.fromJson(response.data);
      }
      return null;
    } catch (e) {
      return null;
    }
  }
}
