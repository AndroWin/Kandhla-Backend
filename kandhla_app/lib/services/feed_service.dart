import '../models/post_model.dart';
import '../models/concern_model.dart';
import 'api_service.dart';

class FeedService {
  final ApiService _apiService = ApiService();

  Future<List<PostModel>> fetchMohallaFeed(String mohallaId) async {
    try {
      final response = await _apiService.client.get('feed/$mohallaId/');
      
      if (response.statusCode == 200) {
        final List<dynamic> data = response.data['results'] ?? response.data;
        return data.map((json) => PostModel.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  Future<bool> createPost(String content, String type, bool isPinned) async {
    try {
      String postType = 'normal';
      bool isAnonymous = false;
      
      if (type == 'whistleblower') {
        isAnonymous = true;
      } else if (isPinned) {
        postType = 'official_order';
      }

      final response = await _apiService.client.post(
        'posts/create/',
        data: {
          'content_text': content,
          'post_type': postType,
          'is_anonymous': isAnonymous,
          // Sending dummy UUID for now until auth is fully hooked up
          'mohalla': '7bcd20c2-d2fb-4646-b494-0de36159491a',
        },
      );
      
      return response.statusCode == 201;
    } catch (e) {
      return false;
    }
  }

  Future<List<ConcernModel>> fetchConcerns(String mohallaId) async {
    try {
      final response = await _apiService.client.get('concerns/$mohallaId/');
      if (response.statusCode == 200) {
        final List<dynamic> data = response.data['results'] ?? response.data;
        return data.map((json) => ConcernModel.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  Future<bool> createConcern(String title, String description, String category) async {
    try {
      final response = await _apiService.client.post(
        'concerns/create/',
        data: {
          'description': '$title\n\n$description',
          // Dummy mohalla ID for now
          'mohalla': '7bcd20c2-d2fb-4646-b494-0de36159491a',
          'image_url': 'https://example.com/dummy.jpg', // Required by serializer
        },
      );
      return response.statusCode == 201;
    } catch (e) {
      return false;
    }
  }

  Future<bool> submitInteraction(int objectId, String modelType, String actionType) async {
    try {
      final response = await _apiService.client.post(
        'interactions/vote/',
        data: {
          'object_id': objectId,
          'model_type': modelType, // 'post' or 'concern'
          'action_type': actionType, // 'upvote', 'downvote', 'support', 'do_not_support'
        },
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}

