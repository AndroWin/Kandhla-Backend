import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';

class PriorityRoomScreen extends StatelessWidget {
  const PriorityRoomScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Priority Room')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.construction, size: 64, color: AppTheme.primaryBlue),
            SizedBox(height: 16),
            Text('Priority Room', style: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Text('No active Vikas requests.', style: TextStyle(color: AppTheme.textMuted)),
          ],
        ),
      ),
    );
  }
}
