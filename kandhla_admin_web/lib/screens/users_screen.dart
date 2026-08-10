import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'dashboard_layout.dart';

class UsersScreen extends StatefulWidget {
  const UsersScreen({super.key});

  @override
  State<UsersScreen> createState() => _UsersScreenState();
}

class _UsersScreenState extends State<UsersScreen> {
  List<dynamic> _users = [];
  bool _isLoading = true;
  String _searchQuery = '';
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _fetchUsers();
  }

  Future<void> _fetchUsers() async {
    setState(() => _isLoading = true);
    final data = await ApiService.getUsers(_searchQuery);
    if (data['success'] == true) {
      setState(() {
        _users = data['users'];
        _isLoading = false;
      });
    } else {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _toggleBan(String userId, String action) async {
    final data = await ApiService.toggleBan(userId, action);
    if (data['success'] == true) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('User is now ${data['status']}')),
      );
      _fetchUsers();
    }
  }

  @override
  Widget build(BuildContext context) {
    return DashboardLayout(
      title: 'Users & Moderation',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Users Directory',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Color(0xFF0EA5E9)),
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _searchController,
            onChanged: (val) {
              _searchQuery = val;
              _fetchUsers();
            },
            decoration: InputDecoration(
              hintText: 'Search by Name or Email...',
              prefixIcon: const Icon(Icons.search),
              filled: true,
              fillColor: Colors.white10,
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide.none),
            ),
          ),
          const SizedBox(height: 24),
          _isLoading
              ? const CircularProgressIndicator()
              : Expanded(
                  child: SingleChildScrollView(
                    child: DataTable(
                      headingRowColor: MaterialStateProperty.all(Colors.white10),
                      columns: const [
                        DataColumn(label: Text('Name & ID')),
                        DataColumn(label: Text('Mohalla')),
                        DataColumn(label: Text('Status')),
                        DataColumn(label: Text('Actions')),
                      ],
                      rows: _users.map((u) {
                        bool isActive = u['status'] == 'Active';
                        return DataRow(
                          cells: [
                            DataCell(Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Text(u['name'], style: const TextStyle(fontWeight: FontWeight.bold)),
                                Text(u['id'], style: const TextStyle(fontSize: 10, color: Colors.white54)),
                              ],
                            )),
                            DataCell(Text(u['mohalla'])),
                            DataCell(Text(
                              u['status'],
                              style: TextStyle(color: isActive ? Colors.green : Colors.red, fontWeight: FontWeight.bold),
                            )),
                            DataCell(Row(
                              children: [
                                ElevatedButton(
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: isActive ? Colors.redAccent : Colors.green,
                                    padding: const EdgeInsets.symmetric(horizontal: 12),
                                  ),
                                  onPressed: () => _toggleBan(u['id'], isActive ? 'ban' : 'unban'),
                                  child: Text(isActive ? 'Ban' : 'Unban'),
                                ),
                              ],
                            )),
                          ],
                        );
                      }).toList(),
                    ),
                  ),
                ),
        ],
      ),
    );
  }
}
