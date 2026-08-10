import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';

class ModQueueScreen extends StatelessWidget {
  const ModQueueScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Mod Queue')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.gavel, size: 64, color: AppTheme.primaryRed),
            SizedBox(height: 16),
            Text('Mod Queue', style: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Text('No reported content at this time.', style: TextStyle(color: AppTheme.textMuted)),
          ],
        ),
      ),
    );
  }
}
