import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'dashboard_layout.dart';

class AdsScreen extends StatefulWidget {
  const AdsScreen({super.key});

  @override
  State<AdsScreen> createState() => _AdsScreenState();
}

class _AdsScreenState extends State<AdsScreen> {
  final TextEditingController _titleController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();
  String _adTarget = 'Whole City';

  Future<void> _pushAd() async {
    final adData = {
      'title': _titleController.text,
      'phone': _phoneController.text,
      'target': _adTarget,
    };
    final result = await ApiService.pushAd(adData);
    if (result['success'] == true) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Ad successfully deployed to users!')));
      _titleController.clear();
      _phoneController.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    return DashboardLayout(
      title: 'Monetization & Ads Network',
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Create Ad Form
          Expanded(
            flex: 1,
            child: Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: Colors.white10,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Push Local Ad', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Color(0xFFFBBF24))),
                  const SizedBox(height: 24),
                  TextField(
                    controller: _titleController,
                    decoration: const InputDecoration(labelText: 'Ad Title / Business Name', filled: true, fillColor: Colors.black26),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: _phoneController,
                    decoration: const InputDecoration(labelText: 'Call / WhatsApp Number', filled: true, fillColor: Colors.black26),
                  ),
                  const SizedBox(height: 16),
                  DropdownButtonFormField<String>(
                    value: _adTarget,
                    items: ['Whole City', 'Mohalla Specific', 'Global'].map((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(value),
                      );
                    }).toList(),
                    onChanged: (newValue) {
                      setState(() {
                        _adTarget = newValue!;
                      });
                    },
                    decoration: const InputDecoration(labelText: 'Target Audience', filled: true, fillColor: Colors.black26),
                  ),
                  const SizedBox(height: 32),
                  SizedBox(
                    width: double.infinity,
                    height: 50,
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFFFBBF24)),
                      onPressed: _pushAd,
                      child: const Text('Deploy Ad Now', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(width: 24),
          // Analytics Chart Placeholders
          Expanded(
            flex: 2,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Ad Performance Analytics', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                const SizedBox(height: 24),
                Row(
                  children: [
                    _buildStatCard('Total Ad Views', '142,593', Icons.visibility),
                    const SizedBox(width: 16),
                    _buildStatCard('Total Clicks/Calls', '12,405', Icons.touch_app),
                    const SizedBox(width: 16),
                    _buildStatCard('Revenue (₹)', '₹45,000', Icons.currency_rupee),
                  ],
                ),
                const SizedBox(height: 24),
                Expanded(
                  child: Container(
                    width: double.infinity,
                    decoration: BoxDecoration(
                      color: Colors.white10,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: const Center(
                      child: Text('Chart Placeholder: Revenue vs Time', style: TextStyle(color: Colors.white54)),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.white10,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: const Color(0xFFFBBF24).withOpacity(0.3)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: const Color(0xFFFBBF24)),
            const SizedBox(height: 12),
            Text(value, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            Text(title, style: const TextStyle(color: Colors.white70)),
          ],
        ),
      ),
    );
  }
}
