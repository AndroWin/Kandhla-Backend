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
}
