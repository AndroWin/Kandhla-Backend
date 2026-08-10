import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../screens/drawer/samvidhan_screen.dart';
import '../screens/drawer/leaderboard_screen.dart';
import '../screens/drawer/settings_screen.dart';
import '../screens/drawer/privacy_screen.dart';
import '../screens/drawer/disclaimer_screen.dart';
import '../screens/drawer/dev_info_screen.dart';
import '../screens/drawer/engineered_by_screen.dart';

class CustomDrawer extends StatelessWidget {
  const CustomDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: AppTheme.bgDark.withValues(alpha: 0.95),
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          DrawerHeader(
            decoration: BoxDecoration(
              border: const Border(bottom: BorderSide(color: AppTheme.glassBorder)),
              gradient: LinearGradient(
                colors: [AppTheme.bgPanel, AppTheme.bgDark],
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                const Text('🏛️', style: TextStyle(fontSize: 40)),
                const SizedBox(height: 8),
                const Text(
                  'Republic of Kandhla',
                  style: TextStyle(color: AppTheme.primaryGold, fontSize: 18, fontWeight: FontWeight.bold, fontFamily: 'Georgia'),
                ),
                Text(
                  'Digital Ecosystem',
                  style: TextStyle(color: AppTheme.textMuted, fontSize: 12),
                ),
              ],
            ),
          ),
          ListTile(
            leading: const Icon(Icons.menu_book, color: AppTheme.primaryGold),
            title: const Text('City Samvidhan', style: TextStyle(color: Colors.white)),
            subtitle: const Text('Read the constitution', style: TextStyle(color: AppTheme.textMuted, fontSize: 10)),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (_) => const SamvidhanScreen()));
            },
          ),
          const Divider(color: AppTheme.glassBorder),
          ListTile(
            leading: const Icon(Icons.leaderboard, color: AppTheme.primaryBlue),
            title: const Text('Leaderboard', style: TextStyle(color: Colors.white)),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (_) => const LeaderboardScreen()));
            },
          ),
          const Divider(color: AppTheme.glassBorder),
          ListTile(
            leading: const Icon(Icons.settings, color: Colors.grey),
            title: const Text('Settings', style: TextStyle(color: Colors.white)),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (_) => const SettingsScreen()));
            },
          ),
          ListTile(
            leading: const Icon(Icons.privacy_tip, color: Colors.grey),
            title: const Text('Privacy & T&C', style: TextStyle(color: Colors.white)),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (_) => const PrivacyScreen()));
            },
          ),
          ListTile(
            leading: const Icon(Icons.warning, color: Colors.orange),
            title: const Text('Disclaimer', style: TextStyle(color: Colors.white)),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (_) => const DisclaimerScreen()));
            },
          ),
          ListTile(
            leading: const Icon(Icons.info_outline, color: Colors.grey),
            title: const Text('Developer Info', style: TextStyle(color: Colors.white)),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (_) => const DevInfoScreen()));
            },
          ),
          ListTile(
            leading: const Icon(Icons.code, color: AppTheme.primaryBlue),
            title: const Text('Engineered By', style: TextStyle(color: Colors.white)),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder: (_) => const EngineeredByScreen()));
            },
          ),
          const Divider(color: AppTheme.glassBorder),
          ListTile(
            leading: const Icon(Icons.logout, color: AppTheme.primaryRed),
            title: const Text('Logout', style: TextStyle(color: AppTheme.primaryRed)),
            onTap: () {
              // Call Global logout in API Service in production
            },
          ),
        ],
      ),
    );
  }
}
