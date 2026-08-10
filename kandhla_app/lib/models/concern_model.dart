class ConcernModel {
  final int id;
  final String authorName;
  final String title;
  final String description;
  final String category;
  final String status;
  final int supportCount;
  final int doNotSupportCount;
  final bool escalatedToCity;
  final String createdAt;
  final String? imageUrl;

  ConcernModel({
    required this.id,
    required this.authorName,
    required this.title,
    required this.description,
    required this.category,
    required this.status,
    required this.supportCount,
    required this.doNotSupportCount,
    this.escalatedToCity = false,
    required this.createdAt,
    this.imageUrl,
  });

  factory ConcernModel.fromJson(Map<String, dynamic> json) {
    final raisedBy = json['raised_by'] ?? {};
    return ConcernModel(
      id: json['id'] ?? 0,
      authorName: raisedBy['name'] ?? 'Citizen',
      title: json['title'] ?? 'Untitled',
      description: json['description'] ?? '',
      category: json['category'] ?? 'general',
      status: json['status'] ?? 'pending',
      supportCount: json['support_count'] ?? 0,
      doNotSupportCount: json['do_not_support_count'] ?? 0,
      escalatedToCity: json['escalated_to_city'] ?? false,
      createdAt: json['created_at'] ?? '',
      imageUrl: json['image_url'],
    );
  }
}
