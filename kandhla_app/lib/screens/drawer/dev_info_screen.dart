import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';

class DevInfoScreen extends StatelessWidget {
  const DevInfoScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Developer Info'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: GlassContainer(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text('Diamondz Technologiez', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 20)),
                const SizedBox(height: 4),
                const Text('HQ: Kandhla', style: TextStyle(color: AppTheme.textMuted)),
                const SizedBox(height: 24),
                const Divider(color: AppTheme.glassBorder),
                const SizedBox(height: 24),
                const Text('Hina Digital Solutions', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 20)),
                const SizedBox(height: 4),
                const Text('Design Partner', style: TextStyle(color: AppTheme.textMuted)),
                const SizedBox(height: 32),
                const Text('Proudly Made in 🇮🇳 with ❤️', style: TextStyle(color: Colors.white, fontStyle: FontStyle.italic)),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
