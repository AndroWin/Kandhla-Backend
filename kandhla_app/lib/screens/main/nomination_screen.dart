import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import '../../services/user_service.dart';

class NominationScreen extends StatefulWidget {
  const NominationScreen({super.key});

  @override
  State<NominationScreen> createState() => _NominationScreenState();
}

class _NominationScreenState extends State<NominationScreen> {
  final UserService _userService = UserService();
  final TextEditingController _manifestoController = TextEditingController();
  
  bool _isLoading = true;
  int _credibilityScore = 0;
  String _selectedSymbol = '🦁'; // default symbol

  final List<String> _symbols = ['🦁', '🦅', '⚖️', '⚙️', '📖', '🪔'];

  @override
  void initState() {
    super.initState();
    _checkEligibility();
  }

  Future<void> _checkEligibility() async {
    final profile = await _userService.fetchMyProfile();
    if (mounted) {
      setState(() {
        _credibilityScore = profile?.credibilityScore ?? 0;
        _isLoading = false;
      });
    }
  }

  @override
  void dispose() {
    _manifestoController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final isEligible = _credibilityScore >= 500;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Parcha Bharo (Nomination)'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            GlassContainer(
              borderColor: isEligible ? AppTheme.primaryGold : AppTheme.primaryRed,
              child: Column(
                children: [
                  Icon(isEligible ? Icons.verified : Icons.block, color: isEligible ? AppTheme.primaryGold : AppTheme.primaryRed, size: 48),
                  const SizedBox(height: 12),
                  Text('Credibility Score: $_credibilityScore / 500', style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Text(
                    isEligible 
                      ? 'You are eligible to contest in the upcoming elections.' 
                      : 'You need at least 500 Credibility to file a nomination. Keep participating in the ecosystem!',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: isEligible ? AppTheme.textMuted : AppTheme.primaryRed),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            if (isEligible) ...[
              const Align(alignment: Alignment.centerLeft, child: Text('Choose Election Symbol', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16))),
              const SizedBox(height: 12),
              Wrap(
                spacing: 12,
                runSpacing: 12,
                children: _symbols.map((symbol) {
                  final isSelected = _selectedSymbol == symbol;
                  return GestureDetector(
                    onTap: () {
                      setState(() {
                        _selectedSymbol = symbol;
                      });
                    },
                    child: Container(
                      width: 60,
                      height: 60,
                      decoration: BoxDecoration(
                        color: isSelected ? AppTheme.primaryGold.withValues(alpha: 0.2) : Colors.black26,
                        border: Border.all(color: isSelected ? AppTheme.primaryGold : AppTheme.glassBorder, width: 2),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Center(child: Text(symbol, style: const TextStyle(fontSize: 28))),
                    ),
                  );
                }).toList(),
              ),
              const SizedBox(height: 24),
              const Align(alignment: Alignment.centerLeft, child: Text('Manifesto / Parcha', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16))),
              const SizedBox(height: 12),
              TextField(
                controller: _manifestoController,
                maxLines: 6,
                style: const TextStyle(color: Colors.white),
                decoration: const InputDecoration(
                  hintText: 'What will you do for your Mohalla? (Minimum 50 words)...',
                  hintStyle: TextStyle(color: AppTheme.textMuted),
                ),
              ),
              const SizedBox(height: 32),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    if (_manifestoController.text.length < 50) {
                      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Manifesto is too short!'), backgroundColor: AppTheme.primaryRed));
                      return;
                    }
                    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Nomination filed successfully!'), backgroundColor: AppTheme.primaryGreen));
                    Navigator.pop(context);
                  },
                  style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGold, padding: const EdgeInsets.symmetric(vertical: 16)),
                  child: const Text('Submit Parcha', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 16)),
                ),
              )
            ]
          ],
        ),
      ),
    );
  }
}
