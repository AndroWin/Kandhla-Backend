import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';

class EditProfileScreen extends StatefulWidget {
  const EditProfileScreen({super.key});

  @override
  State<EditProfileScreen> createState() => _EditProfileScreenState();
}

class _EditProfileScreenState extends State<EditProfileScreen> {
  final TextEditingController _nameController = TextEditingController(text: 'Current Name');
  final TextEditingController _bioController = TextEditingController(text: 'Working hard for our Mohalla.');

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Edit Profile'),
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
            Center(
              child: Stack(
                clipBehavior: Clip.none,
                children: [
                  Container(
                    width: 100,
                    height: 100,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(color: AppTheme.glassBorder, width: 3),
                      color: AppTheme.bgPanel,
                    ),
                    child: const Center(child: Text('👤', style: TextStyle(fontSize: 40))),
                  ),
                  Positioned(
                    bottom: -5,
                    right: -5,
                    child: CircleAvatar(
                      backgroundColor: AppTheme.primaryBlue,
                      radius: 16,
                      child: IconButton(
                        icon: const Icon(Icons.edit, size: 16, color: Colors.white),
                        onPressed: () {
                          // Pick image logic
                        },
                      ),
                    ),
                  )
                ],
              ),
            ),
            const SizedBox(height: 32),
            GlassContainer(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Display Name', style: TextStyle(color: AppTheme.textMuted)),
                  const SizedBox(height: 8),
                  TextField(
                    controller: _nameController,
                    style: const TextStyle(color: Colors.white),
                    decoration: const InputDecoration(
                      enabledBorder: UnderlineInputBorder(borderSide: BorderSide(color: AppTheme.glassBorder)),
                      focusedBorder: UnderlineInputBorder(borderSide: BorderSide(color: AppTheme.primaryGold)),
                    ),
                  ),
                  const SizedBox(height: 24),
                  const Text('Bio / Manifesto Summary', style: TextStyle(color: AppTheme.textMuted)),
                  const SizedBox(height: 8),
                  TextField(
                    controller: _bioController,
                    maxLines: 3,
                    style: const TextStyle(color: Colors.white),
                    decoration: const InputDecoration(
                      enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: AppTheme.glassBorder)),
                      focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: AppTheme.primaryGold)),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 32),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Profile Updated Successfully!'), backgroundColor: AppTheme.primaryGreen));
                  Navigator.pop(context);
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.primaryGold,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: const Text('Save Changes', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 16)),
              ),
            )
          ],
        ),
      ),
    );
  }
}
