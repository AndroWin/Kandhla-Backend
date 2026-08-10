import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:sign_in_with_apple/sign_in_with_apple.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import '../../services/api_service.dart';
import 'profile_setup_screen.dart';
import '../main/main_layout.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  String? selectedMohalla;
  // TODO: Fetch Mohallas dynamically from API instead of mock
  final List<String> mockMohallas = ['1', '2', '3']; // IDs for now
  bool isLoading = false;
  final ApiService _apiService = ApiService();

  void _handleGoogleLogin() async {
    setState(() => isLoading = true);

    try {
      // 1. Trigger Google Sign-In
      final GoogleSignIn googleSignIn = GoogleSignIn(scopes: ['email']);
      final GoogleSignInAccount? googleUser = await googleSignIn.signIn();
      if (googleUser == null) {
        // User canceled
        if (mounted) setState(() => isLoading = false);
        return;
      }

      // 2. Get Google ID Token
      final GoogleSignInAuthentication googleAuth = await googleUser.authentication;
      final String? idToken = googleAuth.idToken;

      if (idToken == null) {
        throw Exception('Failed to get Google ID token');
      }

      // 3. Get FCM Token as Device ID
      String? fcmToken = await FirebaseMessaging.instance.getToken();
      final String deviceId = fcmToken ?? 'device_${DateTime.now().millisecondsSinceEpoch}';

      final response = await _apiService.client.post(
        'auth/google/',
        data: {
          'google_token': idToken,
          'device_id': deviceId,
        },
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        final data = response.data;
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('access_token', data['tokens']['access']);
        
        if (!mounted) return;
        
        bool isNewUser = data['is_new_user'] ?? false;
        
        if (isNewUser) {
           Navigator.pushReplacement(
             context,
             MaterialPageRoute(
               builder: (_) => ProfileSetupScreen(mohalla: 'New Mohalla'),
             ),
           );
        } else {
           Navigator.pushReplacement(
             context,
             MaterialPageRoute(builder: (_) => const MainLayout()),
           );
        }
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Login Failed: $e'), backgroundColor: AppTheme.primaryRed),
      );
    } finally {
      if (mounted) setState(() => isLoading = false);
    }
  }

  void _handleAppleLogin() async {
    setState(() => isLoading = true);

    try {
      final credential = await SignInWithApple.getAppleIDCredential(
        scopes: [
          AppleIDAuthorizationScopes.email,
          AppleIDAuthorizationScopes.fullName,
        ],
      );

      final String? identityToken = credential.identityToken;
      if (identityToken == null) {
        throw Exception('Failed to get Apple identity token');
      }

      String? fcmToken = await FirebaseMessaging.instance.getToken();
      final String deviceId = fcmToken ?? 'device_${DateTime.now().millisecondsSinceEpoch}';
      
      // Extract name if provided (only available on first sign-in)
      String providedName = '';
      if (credential.givenName != null || credential.familyName != null) {
        providedName = '${credential.givenName ?? ''} ${credential.familyName ?? ''}'.trim();
      }

      final response = await _apiService.client.post(
        'auth/apple/',
        data: {
          'apple_token': identityToken,
          'device_id': deviceId,
          'name': providedName,
        },
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        final data = response.data;
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('access_token', data['tokens']['access']);
        
        if (!mounted) return;
        
        bool isNewUser = data['is_new_user'] ?? false;
        
        if (isNewUser) {
           Navigator.pushReplacement(
             context,
             MaterialPageRoute(
               builder: (_) => ProfileSetupScreen(mohalla: 'New Mohalla'),
             ),
           );
        } else {
           Navigator.pushReplacement(
             context,
             MaterialPageRoute(builder: (_) => const MainLayout()),
           );
        }
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Apple Login Failed: $e'), backgroundColor: AppTheme.primaryRed),
      );
    } finally {
      if (mounted) setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.bgDark,
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [AppTheme.bgDark, Color(0xFF1e1b4b)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SafeArea(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Welcome Citizen',
                      style: TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      'Join the digital ecosystem.',
                      style: TextStyle(color: AppTheme.textMuted, fontSize: 16),
                    ),
                    const SizedBox(height: 32),
                    
                    GlassContainer(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Select Mohalla',
                            style: TextStyle(color: AppTheme.primaryBlue, fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 8),
                          DropdownButtonFormField<String>(
                            initialValue: selectedMohalla,
                            dropdownColor: AppTheme.bgPanel,
                            hint: const Text('Select your Mohalla', style: TextStyle(color: AppTheme.textMuted)),
                            items: mockMohallas.map((String value) {
                              return DropdownMenuItem<String>(
                                value: value,
                                child: Text(value, style: const TextStyle(color: Colors.white)),
                              );
                            }).toList(),
                            onChanged: (newValue) {
                              setState(() {
                                selectedMohalla = newValue;
                              });
                            },
                          ),
                          const SizedBox(height: 8),
                          const Text(
                            '*Cannot be changed later. Requires Admin approval.',
                            style: TextStyle(color: AppTheme.primaryRed, fontSize: 11),
                          ),
                        ],
                      ),
                    ),
                    
                    const SizedBox(height: 24),
                    const Center(
                      child: Text(
                        'By continuing, I pledge to the Samvidhan.',
                        style: TextStyle(color: AppTheme.textMuted, fontSize: 12),
                      ),
                    ),
                    const SizedBox(height: 16),
                    
                    SizedBox(
                      width: double.infinity,
                      height: 50,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.white,
                          foregroundColor: Colors.black,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(25),
                          ),
                        ),
                        onPressed: isLoading ? null : _handleGoogleLogin,
                        child: isLoading
                            ? const SizedBox(
                                height: 24,
                                width: 24,
                                child: CircularProgressIndicator(color: Colors.black, strokeWidth: 2),
                              )
                            : const Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(
                                    'G ',
                                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                                  ),
                                  Text('Continue with Google'),
                                ],
                              ),
                      ),
                    ),
                    if (defaultTargetPlatform == TargetPlatform.iOS) ...[
                      const SizedBox(height: 16),
                      SizedBox(
                        width: double.infinity,
                        height: 50,
                        child: SignInWithAppleButton(
                          onPressed: isLoading ? () {} : _handleAppleLogin,
                          borderRadius: const BorderRadius.all(Radius.circular(25)),
                          style: SignInWithAppleButtonStyle.black,
                        ),
                      ),
                    ],
                    const SizedBox(height: 32),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
