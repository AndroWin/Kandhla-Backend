import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'dashboard_layout.dart';

class ElectionsScreen extends StatefulWidget {
  const ElectionsScreen({super.key});

  @override
  State<ElectionsScreen> createState() => _ElectionsScreenState();
}

class _ElectionsScreenState extends State<ElectionsScreen> {
  bool _achaarSanhita = false;

  void _declareElection(String level) async {
    final result = await ApiService.declareElection(level);
    if (result['success'] == true) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$level Election Initialized successfully!')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return DashboardLayout(
      title: 'Election Commission (Supreme EC)',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Elections & Government',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Color(0xFF0EA5E9)),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: _achaarSanhita ? Colors.orange.withOpacity(0.2) : Colors.black26,
                  border: Border.all(color: _achaarSanhita ? Colors.orange : Colors.white10),
                  borderRadius: BorderRadius.circular(30),
                ),
                child: Row(
                  children: [
                    const Text('⚖️ Achaar Sanhita', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.orangeAccent)),
                    const SizedBox(width: 12),
                    Switch(
                      value: _achaarSanhita,
                      activeColor: Colors.orange,
                      onChanged: (val) {
                        setState(() {
                          _achaarSanhita = val;
                        });
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text(val ? 'Code of Conduct applied to app!' : 'Code of Conduct lifted.')),
                        );
                      },
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 32),
          Row(
            children: [
              _buildECActionCard(
                'Declare Global Election',
                'Supreme Minister & City Cabinet (11 roles)',
                Icons.account_balance,
                const Color(0xFF0EA5E9),
                () => _declareElection('global'),
              ),
              const SizedBox(width: 24),
              _buildECActionCard(
                'Declare Local Election',
                'Mohalla Minister & Local Cabinet (5 roles)',
                Icons.location_city,
                const Color(0xFF10B981),
                () => _declareElection('local'),
              ),
            ],
          ),
          const SizedBox(height: 32),
          const Text('Manage Nominations & Cabinet', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          Expanded(
            child: GridView.count(
              crossAxisCount: 3,
              crossAxisSpacing: 16,
              mainAxisSpacing: 16,
              children: [
                _buildSmallActionCard('Assign Symbols', Icons.stars),
                _buildSmallActionCard('Nomination Queue', Icons.how_to_reg),
                _buildSmallActionCard('Approve Cabinet Badges', Icons.verified),
                _buildSmallActionCard('Ban user from Elections', Icons.block),
                _buildSmallActionCard('Live Counting Control', Icons.poll),
                _buildSmallActionCard('Oath Management', Icons.auto_stories),
              ],
            ),
          )
        ],
      ),
    );
  }

  Widget _buildECActionCard(String title, String subtitle, IconData icon, Color color, VoidCallback onTap) {
    return Expanded(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Container(
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: color.withOpacity(0.5)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(icon, size: 48, color: color),
              const SizedBox(height: 16),
              Text(title, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: color)),
              const SizedBox(height: 8),
              Text(subtitle, style: const TextStyle(color: Colors.white70)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSmallActionCard(String title, IconData icon) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white10,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white24),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, size: 40, color: Colors.white70),
          const SizedBox(height: 12),
          Text(title, textAlign: TextAlign.center, style: const TextStyle(fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
