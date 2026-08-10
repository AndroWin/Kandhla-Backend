import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';

class LeaderboardScreen extends StatefulWidget {
  const LeaderboardScreen({super.key});

  @override
  State<LeaderboardScreen> createState() => _LeaderboardScreenState();
}

class _LeaderboardScreenState extends State<LeaderboardScreen> {
  // Using dummy data for now
  final List<Map<String, dynamic>> _topUsers = [
    {'name': 'Ravi Sharma', 'score': 980, 'role': 'mohalla_minister', 'avatar': ''},
    {'name': 'Amit Kumar', 'score': 850, 'role': 'citizen', 'avatar': ''},
    {'name': 'Sneha Gupta', 'score': 740, 'role': 'mohalla_cabinet', 'avatar': ''},
    {'name': 'Anil Verma', 'score': 620, 'role': 'citizen', 'avatar': ''},
    {'name': 'Pooja Singh', 'score': 590, 'role': 'citizen', 'avatar': ''},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Top Citizens'),
        centerTitle: true,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _topUsers.length,
        itemBuilder: (context, index) {
          final user = _topUsers[index];
          final isTop3 = index < 3;
          
          Color rankColor;
          if (index == 0) {
            rankColor = AppTheme.primaryGold;
          } else if (index == 1) {
            rankColor = Colors.grey.shade400; // Silver
          } else if (index == 2) {
            rankColor = Colors.orange.shade700; // Bronze
          } else {
            rankColor = Colors.transparent;
          }

          return Padding(
            padding: const EdgeInsets.only(bottom: 12.0),
            child: GlassContainer(
              borderColor: isTop3 ? rankColor.withValues(alpha: 0.5) : AppTheme.glassBorder,
              backgroundColor: isTop3 ? rankColor.withValues(alpha: 0.1) : AppTheme.glassBg,
              child: ListTile(
                leading: Stack(
                  clipBehavior: Clip.none,
                  children: [
                    CircleAvatar(
                      backgroundColor: isTop3 ? rankColor : Colors.grey.shade800,
                      child: Text(
                        '${index + 1}',
                        style: TextStyle(
                          color: isTop3 ? Colors.black : Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    if (user['role'] == 'mohalla_minister')
                      Positioned(
                        bottom: -4,
                        right: -4,
                        child: Container(
                          width: 14,
                          height: 14,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            gradient: AppTheme.rubyGreen,
                            border: Border.all(color: Colors.white, width: 1),
                          ),
                        ),
                      )
                    else if (user['role'] == 'mohalla_cabinet')
                      Positioned(
                        bottom: -4,
                        right: -4,
                        child: Container(
                          width: 14,
                          height: 14,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            gradient: AppTheme.rubyGrey,
                            border: Border.all(color: Colors.white, width: 1),
                          ),
                        ),
                      ),
                  ],
                ),
                title: Text(
                  user['name'],
                  style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                ),
                subtitle: Text(
                  'Credibility: ${user['score']}',
                  style: const TextStyle(color: AppTheme.textMuted, fontSize: 12),
                ),
                trailing: isTop3
                    ? Icon(Icons.emoji_events, color: rankColor)
                    : null,
              ),
            ),
          );
        },
      ),
    );
  }
}
