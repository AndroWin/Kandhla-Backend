import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';

class BroadcastScreen extends StatelessWidget {
  const BroadcastScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Broadcast Network')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.campaign, size: 64, color: AppTheme.primaryGold),
            SizedBox(height: 16),
            Text('Broadcast Network', style: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Text('Send city-wide alerts (Coming Soon)', style: TextStyle(color: AppTheme.textMuted)),
          ],
        ),
      ),
    );
  }
}
