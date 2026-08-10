import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';

class EngineeredByScreen extends StatelessWidget {
  const EngineeredByScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Mocking data based on screensui.html
    final team = [
      {'name': 'Arqum Siddiqui', 'role': 'CEO'},
      {'name': 'Shaghil Siddiqui', 'role': 'Operations'},
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Engineered By'),
        centerTitle: true,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: team.length,
        itemBuilder: (context, index) {
          final member = team[index];
          return Padding(
            padding: const EdgeInsets.only(bottom: 12.0),
            child: GlassContainer(
              child: Column(
                children: [
                  Container(
                    width: 60,
                    height: 60,
                    margin: const EdgeInsets.only(bottom: 12),
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(color: AppTheme.primaryBlue, width: 2),
                      color: Colors.grey.shade800,
                    ),
                    child: const Icon(Icons.person, color: Colors.white, size: 30),
                  ),
                  Text(member['name']!, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 18)),
                  const SizedBox(height: 4),
                  Text(member['role']!, style: const TextStyle(color: AppTheme.primaryGold, fontSize: 14)),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
