import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _isDarkMode = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          GlassContainer(
            child: ListTile(
              leading: const Icon(Icons.dark_mode, color: Colors.white),
              title: const Text('Dark Mode', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
              trailing: Switch(
                value: _isDarkMode,
                activeTrackColor: AppTheme.primaryBlue,
                onChanged: (val) {
                  setState(() {
                    _isDarkMode = val;
                  });
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Theme settings will be saved locally.')),
                  );
                },
              ),
            ),
          ),
          const SizedBox(height: 12),
          GlassContainer(
            child: ListTile(
              leading: const Icon(Icons.location_on, color: AppTheme.primaryBlue),
              title: const Text('Request Mohalla Change', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
              trailing: const Icon(Icons.chevron_right, color: Colors.white),
              onTap: () {
                _showMohallaChangeDialog();
              },
            ),
          ),
        ],
      ),
    );
  }

  void _showMohallaChangeDialog() {
    final TextEditingController reasonController = TextEditingController();
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          backgroundColor: AppTheme.bgPanel,
          title: const Text('Change Mohalla', style: TextStyle(color: Colors.white)),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                'Changing your Mohalla requires Admin approval and may take up to 48 hours.',
                style: TextStyle(color: AppTheme.textMuted, fontSize: 12),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: reasonController,
                style: const TextStyle(color: Colors.white),
                maxLines: 3,
                decoration: const InputDecoration(
                  hintText: 'Reason for change...',
                  hintStyle: TextStyle(color: AppTheme.textMuted),
                  filled: true,
                  fillColor: Colors.black26,
                  border: OutlineInputBorder(),
                ),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel', style: TextStyle(color: AppTheme.textMuted)),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Mohalla change request submitted.')),
                );
              },
              style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryBlue),
              child: const Text('Submit Request'),
            ),
          ],
        );
      },
    );
  }
}
