import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';

class PrivacyScreen extends StatelessWidget {
  const PrivacyScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Privacy & T&C'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: GlassContainer(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: const [
              Text('1. Data Collection', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 16)),
              SizedBox(height: 8),
              Text('We collect basic details like name, email, and device ID strictly for anti-fraud mechanisms (1 device = 1 vote).', style: TextStyle(color: AppTheme.textMuted)),
              SizedBox(height: 24),
              Text('2. Usage & Ecosystem', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 16)),
              SizedBox(height: 8),
              Text('This is a simulated democratic ecosystem. Your data is used exclusively to facilitate voting, credibility scores, and feed personalization.', style: TextStyle(color: AppTheme.textMuted)),
              SizedBox(height: 24),
              Text('3. Data Retention', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 16)),
              SizedBox(height: 8),
              Text('All accounts can be permanently deleted upon request. Votes are cryptographically hashed and cannot be linked back to a user profile after an election.', style: TextStyle(color: AppTheme.textMuted)),
            ],
          ),
        ),
      ),
    );
  }
}
