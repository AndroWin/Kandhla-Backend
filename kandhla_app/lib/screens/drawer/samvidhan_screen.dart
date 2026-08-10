import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';

class SamvidhanScreen extends StatelessWidget {
  const SamvidhanScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('City Samvidhan', style: TextStyle(fontFamily: 'Georgia', color: AppTheme.primaryGold)),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: const Color(0xFF14141E).withValues(alpha: 0.9),
            border: Border.all(color: AppTheme.primaryGold, width: 1.5),
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              BoxShadow(
                color: AppTheme.primaryGold.withValues(alpha: 0.05),
                blurRadius: 20,
                spreadRadius: 5,
              )
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Center(
                child: Text(
                  '"Hum, Nagrik..."',
                  style: TextStyle(
                    fontFamily: 'Georgia',
                    fontSize: 20,
                    fontStyle: FontStyle.italic,
                    color: AppTheme.primaryGold.withValues(alpha: 0.8),
                  ),
                ),
              ),
              const SizedBox(height: 24),
              const Text(
                'Act 1: Nagriko ke Mool Adhikar',
                style: TextStyle(color: AppTheme.primaryBlue, fontWeight: FontWeight.bold, fontSize: 18),
              ),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.only(left: 12),
                decoration: BoxDecoration(
                  border: Border(left: BorderSide(color: AppTheme.primaryGold.withValues(alpha: 0.5), width: 2)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('Clause 1.1: Post karne ki azadi', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                    SizedBox(height: 8),
                    Text('Sub-clause 1.1(a): Koi bhi user achaar sanhita ke alawa kabhi bhi apne mohalle me post kar sakta he.', style: TextStyle(color: AppTheme.textMuted, fontSize: 13)),
                    SizedBox(height: 4),
                    Text('Sub-clause 1.1(b): Cross-mohalla interactions me keval like/dislike/support anumanya hoga.', style: TextStyle(color: AppTheme.textMuted, fontSize: 13)),
                  ],
                ),
              ),
              const SizedBox(height: 32),
              const Text(
                'Act 2: Chunavi Niyam',
                style: TextStyle(color: AppTheme.primaryBlue, fontWeight: FontWeight.bold, fontSize: 18),
              ),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.only(left: 12),
                decoration: BoxDecoration(
                  border: Border(left: BorderSide(color: AppTheme.primaryGold.withValues(alpha: 0.5), width: 2)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('Clause 2.1: Chunav Prakriya', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                    SizedBox(height: 8),
                    Text('Sub-clause 2.1(a): Voting puri tarah gupt (secret ballot) aur internal system par aadharit hogi. Koi digital voter slip pradan nahi ki jayegi.', style: TextStyle(color: AppTheme.textMuted, fontSize: 13)),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
