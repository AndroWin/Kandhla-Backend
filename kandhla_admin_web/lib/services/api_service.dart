import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // In production, this would point to the live Render backend
  static const String baseUrl = 'http://127.0.0.1:8000/dashboard/api';

  static Future<Map<String, dynamic>> getCities() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/cities/'));
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
    } catch (e) {
      print('Error fetching cities: $e');
    }
    return {'success': false, 'error': 'Failed to load cities'};
  }

  static Future<Map<String, dynamic>> createCity(String name, String state, String country) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/cities/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'name': name, 'state': state, 'country': country}),
      );
      return json.decode(response.body);
    } catch (e) {
      print('Error creating city: $e');
    }
    return {'success': false, 'error': 'Failed to create city'};
  }

  static Future<Map<String, dynamic>> getUsers(String query) async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/users/?q=$query'));
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
    } catch (e) {
      print('Error fetching users: $e');
    }
    return {'success': false, 'error': 'Failed to load users'};
  }

  static Future<Map<String, dynamic>> toggleBan(String userId, String action) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/users/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'user_id': userId, 'action': action}),
      );
      return json.decode(response.body);
    } catch (e) {
      print('Error updating user ban status: $e');
    }
    return {'success': false, 'error': 'Failed to update ban status'};
  }

  static Future<Map<String, dynamic>> getPosts() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/content/'));
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
    } catch (e) {
      print('Error fetching posts: $e');
    }
    return {'success': false, 'error': 'Failed to load posts'};
  }

  static Future<Map<String, dynamic>> deletePost(String postId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/content/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'post_id': postId}),
      );
      return json.decode(response.body);
    } catch (e) {
      print('Error deleting post: $e');
    }
    return {'success': false, 'error': 'Failed to delete post'};
  }

  static Future<Map<String, dynamic>> pushAd(Map<String, dynamic> adData) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/ads/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(adData),
      );
      return json.decode(response.body);
    } catch (e) {
      print('Error pushing ad: $e');
    }
    return {'success': false, 'error': 'Failed to push ad'};
  }

  static Future<Map<String, dynamic>> declareElection(String level, {bool? achaarSanhita}) async {
    try {
      final body = {'level': level};
      if (achaarSanhita != null) {
        body['achaar_sanhita'] = achaarSanhita;
      }
      final response = await http.post(
        Uri.parse('$baseUrl/elections/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(body),
      );
      return json.decode(response.body);
    } catch (e) {
      print('Error initializing election: $e');
    }
    return {'success': false, 'error': 'Failed to initialize election'};
  }

  static Future<Map<String, dynamic>> toggleEmergencyRule(bool isActive) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/content/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'emergency_rule': isActive}),
      );
      return json.decode(response.body);
    } catch (e) {
      print('Error updating emergency rule: $e');
    }
    return {'success': false, 'error': 'Failed to update emergency rule'};
  }
}
