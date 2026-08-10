import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'dashboard_layout.dart';

class CitiesScreen extends StatefulWidget {
  const CitiesScreen({super.key});

  @override
  State<CitiesScreen> createState() => _CitiesScreenState();
}

class _CitiesScreenState extends State<CitiesScreen> {
  List<dynamic> _cities = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchCities();
  }

  Future<void> _fetchCities() async {
    setState(() => _isLoading = true);
    final data = await ApiService.getCities();
    if (data['success'] == true) {
      setState(() {
        _cities = data['cities'];
        _isLoading = false;
      });
    } else {
      setState(() => _isLoading = false);
    }
  }

  void _addCity() {
    final TextEditingController nameController = TextEditingController();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF111827),
        title: const Text('Add New City Ecosystem'),
        content: TextField(
          controller: nameController,
          decoration: const InputDecoration(hintText: 'Enter City Name'),
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
                await ApiService.createCity(nameController.text, 'Unknown', 'India');
                _fetchCities();
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
      title: 'City Management (Root)',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Manage Cities Ecosystem',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              ElevatedButton.icon(
                icon: const Icon(Icons.add),
                label: const Text('Add City'),
                onPressed: _addCity,
              ),
            ],
          ),
          const SizedBox(height: 24),
          _isLoading
              ? const CircularProgressIndicator()
              : Expanded(
                  child: ListView.builder(
                    itemCount: _cities.length,
                    itemBuilder: (context, index) {
                      final city = _cities[index];
                      return Card(
                        color: Colors.white10,
                        margin: const EdgeInsets.only(bottom: 12),
                        child: ListTile(
                          title: Text(city['name'], style: const TextStyle(fontWeight: FontWeight.bold)),
                          subtitle: Text('${city['mohalla_count']} Mohallas'),
                          trailing: ElevatedButton(
                            style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF334155)),
                            onPressed: () {},
                            child: const Text('Enter Ecosystem'),
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
