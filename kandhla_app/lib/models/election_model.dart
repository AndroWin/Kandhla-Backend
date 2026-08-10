class ElectionModel {
  final String id;
  final String name;
  final String level; // city or mohalla
  final String phase; // upcoming, nomination, allocation, campaigning, achaar_sanhita, voting, counting, completed
  final String startDate;
  final String endDate;
  final int totalVotesCast;

  ElectionModel({
    required this.id,
    required this.name,
    required this.level,
    required this.phase,
    required this.startDate,
    required this.endDate,
    required this.totalVotesCast,
  });

  factory ElectionModel.fromJson(Map<String, dynamic> json) {
    return ElectionModel(
      id: json['id'] ?? '',
      name: json['name'] ?? 'General Election',
      level: json['level'] ?? 'mohalla',
      phase: json['phase'] ?? 'upcoming',
      startDate: json['start_date'] ?? '',
      endDate: json['end_date'] ?? '',
      totalVotesCast: json['total_votes_cast'] ?? 0,
    );
  }
}

class CandidateModel {
  final String id;
  final String userProfileId;
  final String name;
  final String? profileImage;
  final String symbolUrl;
  final String manifesto;

  CandidateModel({
    required this.id,
    required this.userProfileId,
    required this.name,
    this.profileImage,
    required this.symbolUrl,
    required this.manifesto,
  });

  factory CandidateModel.fromJson(Map<String, dynamic> json) {
    return CandidateModel(
      id: json['id'] ?? '',
      userProfileId: json['user']?['id']?.toString() ?? '',
      name: json['user']?['name'] ?? 'Candidate',
      profileImage: json['user']?['profile_image'],
      symbolUrl: json['symbol_url'] ?? '',
      manifesto: json['manifesto'] ?? '',
    );
  }
}
