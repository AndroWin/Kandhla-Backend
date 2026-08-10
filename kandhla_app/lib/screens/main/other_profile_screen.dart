import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';

import '../../utilities/report_modal.dart';

class OtherProfileScreen extends StatelessWidget {
  final String userId;
  final String name;
  final int credibilityScore;
  final String role;
  
  const OtherProfileScreen({
    super.key,
    required this.userId,
    required this.name,
    required this.credibilityScore,
    required this.role,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        actions: [
          IconButton(
            icon: const Icon(Icons.flag, color: AppTheme.primaryRed),
            tooltip: 'Report Citizen',
            onPressed: () {
              ReportModal.show(context, targetId: userId, type: 'citizen');
            },
          ),
        ],
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                width: 80,
                height: 80,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(
                    color: _getRoleColor(role),
                    width: 3,
                  ),
                  color: Colors.grey.shade800,
                ),
                child: const Icon(Icons.person, color: Colors.white, size: 40),
              ),
              const SizedBox(height: 16),
              Text(name, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 24)),
              const SizedBox(height: 4),
              Text(
                role.replaceAll('_', ' ').toUpperCase(),
                style: TextStyle(color: _getRoleColor(role), fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Column(
                    children: [
                      Text(credibilityScore.toString(), style: const TextStyle(fontWeight: FontWeight.bold, color: AppTheme.primaryBlue, fontSize: 20)),
                      const Text('Credibility', style: TextStyle(color: AppTheme.textMuted, fontSize: 12)),
                    ],
                  ),
                ],
              ),
              const SizedBox(height: 32),
              ElevatedButton(
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Viewing past posts is coming soon.')),
                  );
                },
                child: const Text('View Posts'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getRoleColor(String role) {
    if (role == 'supreme_minister' || role == 'city_minister') return AppTheme.primaryGold;
    if (role == 'mohalla_minister') return AppTheme.primaryPurple;
    return AppTheme.textMuted;
  }
}
