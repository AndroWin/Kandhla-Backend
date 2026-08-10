import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import 'mod_queue_screen.dart';
import 'priority_room_screen.dart';
import 'broadcast_screen.dart';
import 'local_control_screen.dart';

class MantralayaDashboard extends StatelessWidget {
  final String role; // passed from provider/auth

  const MantralayaDashboard({super.key, required this.role});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('VIP Mantralaya'),
        backgroundColor: AppTheme.bgDark,
        elevation: 0,
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [AppTheme.bgDark, AppTheme.bgPanel],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            GlassContainer(
              borderColor: AppTheme.primaryGold.withValues(alpha: 0.5),
              backgroundColor: AppTheme.primaryGold.withValues(alpha: 0.1),
              child: Column(
                children: [
                  const Icon(Icons.shield, color: AppTheme.primaryGold, size: 48),
                  const SizedBox(height: 12),
                  const Text('Ministerial Access Granted', style: TextStyle(color: AppTheme.primaryGold, fontWeight: FontWeight.bold, fontSize: 18)),
                  const SizedBox(height: 4),
                  Text('Role: ${role.replaceAll('_', ' ').toUpperCase()}', style: const TextStyle(color: Colors.white)),
                ],
              ),
            ),
            const SizedBox(height: 24),
            const Text('Modules', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 20)),
            const SizedBox(height: 12),
            _buildModuleCard(
              context,
              title: 'Mod Queue',
              subtitle: 'Review reported content and flag citizens',
              icon: Icons.gavel,
              color: AppTheme.primaryRed,
              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ModQueueScreen())),
              hasAccess: role == 'home_minister' || role == 'supreme_minister' || role == 'admin',
            ),
            _buildModuleCard(
              context,
              title: 'Priority Room',
              subtitle: 'Manage Vikas requests and allocate resources',
              icon: Icons.construction,
              color: AppTheme.primaryBlue,
              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const PriorityRoomScreen())),
              hasAccess: role == 'vikas_minister' || role == 'supreme_minister' || role == 'admin',
            ),
            _buildModuleCard(
              context,
              title: 'Broadcast Network',
              subtitle: 'Send official alerts to all citizens',
              icon: Icons.campaign,
              color: AppTheme.primaryGold,
              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const BroadcastScreen())),
              hasAccess: role == 'ib_minister' || role == 'supreme_minister' || role == 'admin',
            ),
            _buildModuleCard(
              context,
              title: 'Local Control',
              subtitle: 'Manage Mohalla specific events',
              icon: Icons.location_city,
              color: AppTheme.primaryGreen,
              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const LocalControlScreen())),
              hasAccess: role == 'mohalla_minister' || role == 'admin',
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildModuleCard(BuildContext context, {required String title, required String subtitle, required IconData icon, required Color color, required VoidCallback onTap, required bool hasAccess}) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Opacity(
        opacity: hasAccess ? 1.0 : 0.4,
        child: GlassContainer(
          borderColor: hasAccess ? color.withValues(alpha: 0.5) : AppTheme.glassBorder,
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: color.withValues(alpha: 0.2),
              child: Icon(icon, color: color),
            ),
            title: Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
            subtitle: Text(subtitle, style: const TextStyle(color: AppTheme.textMuted, fontSize: 12)),
            trailing: hasAccess ? const Icon(Icons.arrow_forward_ios, color: Colors.white, size: 16) : const Icon(Icons.lock, color: AppTheme.textMuted),
            onTap: hasAccess ? onTap : () {
              ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Access Denied. Insufficient clearance.')));
            },
          ),
        ),
      ),
    );
  }
}
