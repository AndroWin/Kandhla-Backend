class CityModel {
  final String id;
  final String name;
  final String state;
  final int populationCount;

  CityModel({
    required this.id,
    required this.name,
    required this.state,
    required this.populationCount,
  });

  factory CityModel.fromJson(Map<String, dynamic> json) {
    return CityModel(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      state: json['state'] ?? '',
      populationCount: json['population_count'] ?? 0,
    );
  }
}

class MohallaModel {
  final String id;
  final String name;
  final int populationCount;
  final bool hasCabinet;

  MohallaModel({
    required this.id,
    required this.name,
    required this.populationCount,
    this.hasCabinet = false,
  });

  factory MohallaModel.fromJson(Map<String, dynamic> json) {
    return MohallaModel(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      populationCount: json['population_count'] ?? 0,
      hasCabinet: json['has_active_cabinet'] ?? false,
    );
  }
}
