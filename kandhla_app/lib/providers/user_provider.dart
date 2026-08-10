import 'package:flutter/foundation.dart';

class UserProvider extends ChangeNotifier {
  String _name = 'Citizen';
  String _mohalla = 'Mohalla X';
  String _role = 'citizen'; // citizen, mohalla_minister, city_minister, supreme_minister
  int _credibilityScore = 100;
  final String _profileImage = '';

  // Getters
  String get name => _name;
  String get mohalla => _mohalla;
  String get role => _role;
  int get credibilityScore => _credibilityScore;
  String get profileImage => _profileImage;
  
  bool get isVIP => _role != 'citizen';
  bool get isSupreme => _role == 'supreme_minister';

  // For testing purposes, we add setters. In production, this data comes from API.
  void loadUserData({
    required String name,
    required String mohalla,
    required String role,
    required int credibilityScore,
  }) {
    _name = name;
    _mohalla = mohalla;
    _role = role;
    _credibilityScore = credibilityScore;
    notifyListeners();
  }

  void updateCredibility(int score) {
    _credibilityScore = score;
    notifyListeners();
  }
}
