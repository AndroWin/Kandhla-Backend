import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';

class NotificationsScreen extends StatelessWidget {
  const NotificationsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Mock notifications list based on blueprint
    final List<Map<String, dynamic>> notifications = [
      {
        'title': 'Election Comm. announced dates!',
        'time': '2m ago',
        'isUnread': true,
        'type': 'system',
      },
      {
        'title': 'Citizen B liked your post.',
        'time': '1 hr ago',
        'isUnread': false,
        'type': 'interaction',
      },
      {
        'title': 'Your Mohalla has a new Priority Samasya.',
        'time': '2 days ago',
        'isUnread': false,
        'type': 'alert',
      }
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Notifications'),
        actions: [
          IconButton(
            icon: const Icon(Icons.done_all),
            tooltip: 'Mark all as read',
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('All marked as read.')),
              );
            },
          ),
        ],
      ),
      body: notifications.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Icon(Icons.notifications_off, size: 64, color: AppTheme.glassBorder),
                  SizedBox(height: 16),
                  Text('All caught up!', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                  SizedBox(height: 8),
                  Text('No new notifications.', style: TextStyle(color: AppTheme.textMuted)),
                ],
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: notifications.length,
              itemBuilder: (context, index) {
                final notif = notifications[index];
                
                IconData icon;
                Color iconColor;
                if (notif['type'] == 'system') {
                  icon = Icons.campaign;
                  iconColor = AppTheme.primaryGold;
                } else if (notif['type'] == 'interaction') {
                  icon = Icons.thumb_up;
                  iconColor = AppTheme.primaryBlue;
                } else {
                  icon = Icons.warning;
                  iconColor = AppTheme.primaryRed;
                }

                return Padding(
                  padding: const EdgeInsets.only(bottom: 12.0),
                  child: GlassContainer(
                    borderColor: notif['isUnread'] ? AppTheme.primaryBlue.withValues(alpha: 0.5) : AppTheme.glassBorder,
                    backgroundColor: notif['isUnread'] ? AppTheme.primaryBlue.withValues(alpha: 0.1) : AppTheme.glassBg,
                    child: ListTile(
                      leading: CircleAvatar(
                        backgroundColor: iconColor.withValues(alpha: 0.2),
                        child: Icon(icon, color: iconColor, size: 20),
                      ),
                      title: Text(
                        notif['title'],
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: notif['isUnread'] ? FontWeight.bold : FontWeight.normal,
                        ),
                      ),
                      subtitle: Text(
                        notif['time'],
                        style: TextStyle(
                          color: notif['isUnread'] ? AppTheme.primaryBlue : AppTheme.textMuted,
                          fontSize: 12,
                        ),
                      ),
                      trailing: notif['isUnread'] 
                          ? const Icon(Icons.circle, color: AppTheme.primaryBlue, size: 10) 
                          : null,
                    ),
                  ),
                );
              },
            ),
    );
  }
}
