class PostModel {
  final int id;
  final String authorName;
  final String authorRole;
  final String authorAvatar;
  final String content;
  final String category;
  final String type; // normal, concern, whistleblower
  final String status;
  final int upvotes;
  final int downvotes;
  final int commentCount;
  final bool isPinned;
  final String createdAt;

  PostModel({
    required this.id,
    required this.authorName,
    required this.authorRole,
    required this.authorAvatar,
    required this.content,
    required this.category,
    required this.type,
    required this.status,
    required this.upvotes,
    required this.downvotes,
    required this.commentCount,
    this.isPinned = false,
    required this.createdAt,
  });

  factory PostModel.fromJson(Map<String, dynamic> json) {
    final authorInfo = json['author'] ?? {};
    return PostModel(
      id: json['id'] ?? 0,
      authorName: authorInfo['name'] ?? 'Unknown',
      authorRole: authorInfo['role'] ?? 'citizen',
      authorAvatar: authorInfo['avatar_url'] ?? '',
      content: json['content_text'] ?? '',
      category: json['category'] ?? '',
      type: json['post_type'] ?? 'normal',
      status: json['status'] ?? 'active',
      upvotes: json['upvotes'] ?? 0,
      downvotes: json['downvotes'] ?? 0,
      commentCount: json['comment_count'] ?? 0,
      isPinned: json['is_pinned'] ?? false,
      createdAt: json['created_at'] ?? '',
    );
  }
}
