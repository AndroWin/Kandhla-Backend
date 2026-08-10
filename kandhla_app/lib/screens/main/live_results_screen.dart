import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import 'dart:math';

class LiveResultsScreen extends StatefulWidget {
  final String electionName;
  const LiveResultsScreen({super.key, required this.electionName});

  @override
  State<LiveResultsScreen> createState() => _LiveResultsScreenState();
}

class _LiveResultsScreenState extends State<LiveResultsScreen> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  
  // Dummy candidate results
  final List<Map<String, dynamic>> _results = [
    {'name': 'Arif Khan', 'symbol': '🦁', 'votes': 420},
    {'name': 'Rahul Sharma', 'symbol': '🦅', 'votes': 310},
    {'name': 'Zaid Ali', 'symbol': '⚖️', 'votes': 150},
  ];

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Live Results & Oath')),
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
            const Center(
              child: Text(
                'ELECTION RESULTS',
                style: TextStyle(color: AppTheme.primaryGold, fontSize: 24, fontWeight: FontWeight.bold, letterSpacing: 2),
              ),
            ),
            const SizedBox(height: 8),
            Center(
              child: Text(
                widget.electionName,
                style: const TextStyle(color: Colors.white, fontSize: 16),
              ),
            ),
            const SizedBox(height: 32),
            ...List.generate(_results.length, (index) {
              final candidate = _results[index];
              final isWinner = index == 0;
              final maxVotes = _results[0]['votes'];
              final percentage = candidate['votes'] / maxVotes;

              return Padding(
                padding: const EdgeInsets.only(bottom: 24.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            Text(candidate['symbol'], style: const TextStyle(fontSize: 24)),
                            const SizedBox(width: 8),
                            Text(
                              candidate['name'],
                              style: TextStyle(
                                color: isWinner ? AppTheme.primaryGold : Colors.white,
                                fontWeight: FontWeight.bold,
                                fontSize: 18,
                              ),
                            ),
                          ],
                        ),
                        Text(
                          '${candidate['votes']} Votes',
                          style: TextStyle(
                            color: isWinner ? AppTheme.primaryGold : AppTheme.textMuted,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    AnimatedBuilder(
                      animation: _controller,
                      builder: (context, child) {
                        return FractionallySizedBox(
                          widthFactor: max(0.05, percentage * _controller.value),
                          child: Container(
                            height: 12,
                            decoration: BoxDecoration(
                              color: isWinner ? AppTheme.primaryGold : AppTheme.primaryBlue,
                              borderRadius: BorderRadius.circular(6),
                            ),
                          ),
                        );
                      },
                    ),
                  ],
                ),
              );
            }),
            const SizedBox(height: 40),
            GlassContainer(
              borderColor: AppTheme.primaryGold,
              backgroundColor: AppTheme.primaryGold.withValues(alpha: 0.1),
              child: Column(
                children: [
                  const Icon(Icons.star, color: AppTheme.primaryGold, size: 48),
                  const SizedBox(height: 16),
                  const Text(
                    'WINNER DECLARED',
                    style: TextStyle(color: AppTheme.primaryGold, fontWeight: FontWeight.bold, fontSize: 20),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '${_results[0]['name']} is the new leader!',
                    style: const TextStyle(color: Colors.white, fontSize: 16),
                  ),
                  const SizedBox(height: 24),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () {
                        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Oath Ceremony Initiated.')));
                      },
                      style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGold),
                      child: const Text('Proceed to Oath Taking', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
                    ),
                  ),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}
