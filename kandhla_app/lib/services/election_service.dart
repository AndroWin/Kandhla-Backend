import '../models/election_model.dart';
import 'api_service.dart';

class ElectionService {
  final ApiService _apiService = ApiService();

  Future<List<ElectionModel>> fetchActiveElections() async {
    try {
      final response = await _apiService.client.get('elections/');
      if (response.statusCode == 200) {
        final List<dynamic> data = response.data['results'] ?? response.data;
        return data.map((json) => ElectionModel.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  Future<List<CandidateModel>> fetchCandidates(String electionId) async {
    try {
      final response = await _apiService.client.get('elections/$electionId/candidates/');
      if (response.statusCode == 200) {
        final List<dynamic> data = response.data['results'] ?? response.data;
        return data.map((json) => CandidateModel.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  Future<bool> castVote(String electionId, String candidateId, String deviceId) async {
    try {
      final response = await _apiService.client.post(
        'election/cast-vote/',
        data: {
          'election_id': electionId,
          'candidate_id': candidateId,
          'device_id': deviceId,
        },
      );
      return response.statusCode == 202; // Async accepted
    } catch (e) {
      return false;
    }
  }
}
