import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import '../../services/api_service.dart';
import '../main/main_layout.dart';

class ProfileSetupScreen extends StatefulWidget {
  final String mohalla;
  
  const ProfileSetupScreen({super.key, required this.mohalla});

  @override
  State<ProfileSetupScreen> createState() => _ProfileSetupScreenState();
}

class _ProfileSetupScreenState extends State<ProfileSetupScreen> {
  final _nameController = TextEditingController();
  final _bioController = TextEditingController();
  bool isLoading = false;
  final ApiService _apiService = ApiService();

  void _submitProfile() async {
    if (_nameController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Name is required')),
      );
      return;
    }

    setState(() => isLoading = true);

    try {
      final response = await _apiService.client.put(
        'auth/profile/setup/',
        data: {
          'name': _nameController.text.trim(),
          'bio': _bioController.text.trim(),
          'city_id': 1, // Defaulting for now
          'mohalla_id': 1, // Defaulting for now
        },
      );

      if (response.statusCode == 200) {
        if (!mounted) return;
        
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const MainLayout()));
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Profile Setup Complete!'), backgroundColor: AppTheme.primaryGreen),
        );
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed: $e'), backgroundColor: AppTheme.primaryRed),
      );
    } finally {
      if (mounted) setState(() => isLoading = false);
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    _bioController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Complete Profile'),
        automaticallyImplyLeading: false,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          children: [
            const SizedBox(height: 20),
            Center(
              child: Stack(
                children: [
                  Container(
                    width: 100,
                    height: 100,
                    decoration: BoxDecoration(
                      color: AppTheme.bgPanel,
                      shape: BoxShape.circle,
                      border: Border.all(color: AppTheme.primaryBlue, width: 2),
                    ),
                    child: const Center(
                      child: Text('📷', style: TextStyle(fontSize: 40)),
                    ),
                  ),
                  Positioned(
                    bottom: 0,
                    right: 0,
                    child: Container(
                      padding: const EdgeInsets.all(4),
                      decoration: const BoxDecoration(
                        color: AppTheme.primaryBlue,
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(Icons.add, color: Colors.white, size: 20),
                    ),
                  )
                ],
              ),
            ),
            const SizedBox(height: 40),
            
            GlassContainer(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Mohalla (Locked)', style: TextStyle(color: AppTheme.textMuted)),
                  const SizedBox(height: 8),
                  TextFormField(
                    initialValue: widget.mohalla,
                    enabled: false,
                    style: const TextStyle(color: Colors.grey),
                  ),
                  
                  const SizedBox(height: 20),
                  const Text('Full Name', style: TextStyle(color: AppTheme.textMuted)),
                  const SizedBox(height: 8),
                  TextFormField(
                    controller: _nameController,
                    style: const TextStyle(color: Colors.white),
                    decoration: const InputDecoration(
                      hintText: 'e.g. Arqum Siddiqui',
                    ),
                  ),
                  
                  const SizedBox(height: 20),
                  const Text('Bio (Optional)', style: TextStyle(color: AppTheme.textMuted)),
                  const SizedBox(height: 8),
                  TextFormField(
                    controller: _bioController,
                    style: const TextStyle(color: Colors.white),
                    maxLines: 3,
                    decoration: const InputDecoration(
                      hintText: 'Software Developer',
                    ),
                  ),
                ],
              ),
            ),
            
            const SizedBox(height: 40),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: isLoading ? null : _submitProfile,
                child: isLoading 
                    ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.white))
                    : const Text('Complete Profile', style: TextStyle(fontSize: 16)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
