import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';

class LocalControlScreen extends StatelessWidget {
  const LocalControlScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Local Control')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.location_city, size: 64, color: AppTheme.primaryGreen),
            SizedBox(height: 16),
            Text('Local Control', style: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Text('Manage Mohalla specifics (Coming Soon)', style: TextStyle(color: AppTheme.textMuted)),
          ],
        ),
      ),
    );
  }
}
