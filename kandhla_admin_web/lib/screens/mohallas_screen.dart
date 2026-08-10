import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'dashboard_layout.dart';

class MohallasScreen extends StatefulWidget {
  const MohallasScreen({super.key});

  @override
  State<MohallasScreen> createState() => _MohallasScreenState();
}

class _MohallasScreenState extends State<MohallasScreen> {
  List<dynamic> _mohallas = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchMohallas();
  }

  Future<void> _fetchMohallas() async {
    setState(() => _isLoading = true);
    // TODO: implement ApiService.getMohallas()
    // final data = await ApiService.getMohallas();
    // For now mock data
    final data = {'success': true, 'mohallas': [{'id': '1', 'name': 'Kandhla North', 'city': 'Kandhla', 'population': 450}]};
    if (data['success'] == true) {
      setState(() {
        _mohallas = data['mohallas'] as List<dynamic>;
        _isLoading = false;
      });
    } else {
      setState(() => _isLoading = false);
    }
  }

  void _addMohalla() {
    final TextEditingController nameController = TextEditingController();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF111827),
        title: const Text('Add New Mohalla'),
        content: TextField(
          controller: nameController,
          decoration: const InputDecoration(hintText: 'Enter Mohalla Name'),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              if (nameController.text.isNotEmpty) {
                Navigator.pop(context);
                // TODO: implement ApiService.createMohalla
                _fetchMohallas();
              }
            },
            child: const Text('Create'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return DashboardLayout(
      title: 'Mohalla Management',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Mohallas (Colonies)',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              ElevatedButton.icon(
                icon: const Icon(Icons.add),
                label: const Text('Add Mohalla'),
                onPressed: _addMohalla,
              ),
            ],
          ),
          const SizedBox(height: 24),
          _isLoading
              ? const CircularProgressIndicator()
              : Expanded(
                  child: ListView.builder(
                    itemCount: _mohallas.length,
                    itemBuilder: (context, index) {
                      final mohalla = _mohallas[index];
                      return Card(
                        color: Colors.white10,
                        margin: const EdgeInsets.only(bottom: 12),
                        child: ListTile(
                          title: Text(mohalla['name'], style: const TextStyle(fontWeight: FontWeight.bold)),
                          subtitle: Text('City: ${mohalla['city']} | Users: ${mohalla['population']}'),
                          trailing: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              IconButton(icon: const Icon(Icons.edit, color: Colors.blueAccent), onPressed: () {}),
                              IconButton(icon: const Icon(Icons.delete, color: Colors.redAccent), onPressed: () {}),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),
        ],
      ),
    );
  }
}
