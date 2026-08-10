import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import 'package:shared_preferences/shared_preferences.dart';

class DisclaimerScreen extends StatelessWidget {
  const DisclaimerScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Disclaimer'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: GlassContainer(
          borderColor: AppTheme.primaryRed.withValues(alpha: 0.5),
          backgroundColor: AppTheme.primaryRed.withValues(alpha: 0.1),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Notice', style: TextStyle(color: AppTheme.primaryRed, fontWeight: FontWeight.bold, fontSize: 20)),
              const SizedBox(height: 12),
              const Text('This app is a VIRTUAL SIMULATION ecosystem created for the citizens of Kandhla. It is NOT affiliated with any official Government entity, Election Commission, or State apparatus.', style: TextStyle(color: Colors.white, height: 1.5)),
              const SizedBox(height: 16),
              const Text('All roles, elections, and polling functionalities within this app are strictly for the digital simulation and hold no legal or real-world validity.', style: TextStyle(color: AppTheme.textMuted, height: 1.5)),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryRed),
                  onPressed: () async {
                    final prefs = await SharedPreferences.getInstance();
                    await prefs.setBool('disclaimer_acknowledged', true);
                    if (context.mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Disclaimer Acknowledged')),
                      );
                      Navigator.pop(context);
                    }
                  },
                  child: const Text('I Understand'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
