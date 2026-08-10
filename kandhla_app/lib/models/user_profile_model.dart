class UserProfileModel {
  final int id;
  final String deviceId;
  final String name;
  final String bio;
  final String role;
  final int credibilityScore;
  final String? profileImage;
  final String mohalla;
  final String ward;

  UserProfileModel({
    required this.id,
    required this.deviceId,
    required this.name,
    required this.bio,
    required this.role,
    required this.credibilityScore,
    this.profileImage,
    required this.mohalla,
    required this.ward,
  });

  factory UserProfileModel.fromJson(Map<String, dynamic> json) {
    return UserProfileModel(
      id: json['id'] ?? 0,
      deviceId: json['device_id'] ?? '',
      name: json['name'] ?? 'Citizen',
      bio: json['bio'] ?? '',
      role: json['role'] ?? 'citizen',
      credibilityScore: json['credibility_score'] ?? 100,
      profileImage: json['profile_image'],
      mohalla: json['mohalla'] != null ? json['mohalla']['name'] ?? 'Unknown' : 'Unknown',
      ward: json['mohalla'] != null && json['mohalla']['ward'] != null 
          ? json['mohalla']['ward']['name'] ?? 'Unknown' 
          : 'Unknown',
    );
  }
}
