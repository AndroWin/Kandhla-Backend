import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter/material.dart';
import '../main.dart';
import '../screens/auth/login_screen.dart';
import '../screens/utilities/offline_error_screen.dart';
import '../screens/utilities/banned_notice_screen.dart';

class ApiService {
  late final Dio _dio;
  
  // Update this to your local network IP if testing on an actual physical device
  // 10.0.2.2 is used for Android emulator to access host localhost
  static const String baseUrl = 'http://10.0.2.2:8000/api/';

  ApiService() {
    _dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 10),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          // Fetch token from SharedPreferences and attach to headers
          final prefs = await SharedPreferences.getInstance();
          final token = prefs.getString('access_token');
          if (token != null && token.isNotEmpty) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          return handler.next(options);
        },
        onError: (DioException e, handler) async {
          // Global error handling, e.g. token expiration, bans, network errors
          if (e.type == DioExceptionType.connectionTimeout || 
              e.type == DioExceptionType.receiveTimeout || 
              e.type == DioExceptionType.connectionError ||
              e.error != null && e.error.toString().contains('SocketException')) {
            if (navigatorKey.currentContext != null) {
              Navigator.push(
                navigatorKey.currentContext!,
                MaterialPageRoute(
                  builder: (_) => OfflineErrorScreen(
                    onRetry: () {
                      Navigator.pop(navigatorKey.currentContext!);
                    },
                  ),
                ),
              );
            }
          }

          if (e.response?.statusCode == 401) {
            final prefs = await SharedPreferences.getInstance();
            await prefs.remove('access_token');
            
            if (navigatorKey.currentContext != null) {
              Navigator.pushAndRemoveUntil(
                navigatorKey.currentContext!,
                MaterialPageRoute(builder: (_) => const LoginScreen()),
                (route) => false,
              );
            }
          } else if (e.response?.statusCode == 403) {
            // Assume 403 could be a Ban
            if (navigatorKey.currentContext != null) {
              Navigator.pushAndRemoveUntil(
                navigatorKey.currentContext!,
                MaterialPageRoute(builder: (_) => const BannedNoticeScreen()),
                (route) => false,
              );
            }
          }
          return handler.next(e);
        },
      ),
    );
  }

  Dio get client => _dio;
}
