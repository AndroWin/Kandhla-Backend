import '../models/ecosystem_model.dart';
import 'api_service.dart';

class EcosystemService {
  final ApiService _apiService = ApiService();

  Future<List<CityModel>> fetchCities() async {
    try {
      final response = await _apiService.client.get('cities/');
      if (response.statusCode == 200) {
        final List<dynamic> data = response.data['results'] ?? response.data;
        return data.map((json) => CityModel.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  Future<List<MohallaModel>> fetchMohallas(String cityId) async {
    try {
      final response = await _apiService.client.get('cities/$cityId/mohallas/');
      if (response.statusCode == 200) {
        final List<dynamic> data = response.data['results'] ?? response.data;
        return data.map((json) => MohallaModel.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }
}
