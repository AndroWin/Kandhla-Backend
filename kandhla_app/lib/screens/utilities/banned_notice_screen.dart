import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';

class BannedNoticeScreen extends StatelessWidget {
  const BannedNoticeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF3f0f14), AppTheme.bgDark],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.gavel_rounded, size: 100, color: AppTheme.primaryRed),
            const SizedBox(height: 24),
            const Text(
              'Account Suspended',
              style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white),
            ),
            const SizedBox(height: 16),
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 32.0),
              child: Text(
                'Your account has been permanently banned due to severe violations of the Code of Conduct. You have accumulated 4 strikes.',
                textAlign: TextAlign.center,
                style: TextStyle(color: AppTheme.textMuted, fontSize: 16),
              ),
            ),
            const SizedBox(height: 40),
            GlassContainer(
              borderColor: AppTheme.primaryRed.withValues(alpha: 0.5),
              backgroundColor: AppTheme.primaryRed.withValues(alpha: 0.1),
              child: const Padding(
                padding: EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
                child: Text(
                  'Featured Banned Profile',
                  style: TextStyle(color: AppTheme.primaryRed, fontWeight: FontWeight.bold),
                ),
              ),
            ),
            const SizedBox(height: 40),
            TextButton(
              onPressed: () {
                // Implement Logout
              },
              child: const Text('Logout', style: TextStyle(color: Colors.white, decoration: TextDecoration.underline)),
            ),
          ],
        ),
      ),
    );
  }
}
