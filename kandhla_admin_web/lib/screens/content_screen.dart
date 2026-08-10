import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'dashboard_layout.dart';

class ContentScreen extends StatefulWidget {
  const ContentScreen({super.key});

  @override
  State<ContentScreen> createState() => _ContentScreenState();
}

class _ContentScreenState extends State<ContentScreen> {
  bool _isEmergencyRule = false;

  List<dynamic> _posts = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchPosts();
  }

  Future<void> _fetchPosts() async {
    setState(() => _isLoading = true);
    final data = await ApiService.getPosts();
    if (data['success'] == true) {
      setState(() {
        _posts = data['posts'];
        _isLoading = false;
      });
    } else {
      setState(() => _isLoading = false);
    }
  }

  void _deletePost(String postId) async {
    await ApiService.deletePost(postId);
    _fetchPosts();
  }

  void _toggleEmergencyRule(bool value) async {
    await ApiService.toggleEmergencyRule(value);
    setState(() {
      _isEmergencyRule = value;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(value ? '🚨 EMERGENCY RULE IMPOSED! App locked.' : '✅ Emergency Rule Lifted.'),
        backgroundColor: value ? Colors.red : Colors.green,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return DashboardLayout(
      title: 'Content & Master Controls',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Global Posts Feed',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: _isEmergencyRule ? Colors.red.withOpacity(0.2) : Colors.black26,
                  border: Border.all(color: _isEmergencyRule ? Colors.red : Colors.white10),
                  borderRadius: BorderRadius.circular(30),
                ),
                child: Row(
                  children: [
                    const Text('🚨 EMERGENCY RULE', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.redAccent)),
                    const SizedBox(width: 12),
                    Switch(
                      value: _isEmergencyRule,
                      activeColor: Colors.red,
                      onChanged: _toggleEmergencyRule,
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          const Text('Manage all user posts, delete inappropriate content, and oversee the city feed.', style: TextStyle(color: Colors.white70)),
          const SizedBox(height: 24),
          _isLoading 
            ? const CircularProgressIndicator()
            : Expanded(
            child: ListView.builder(
              itemCount: _posts.length,
              itemBuilder: (context, index) {
                final post = _posts[index];
                return Card(
                  color: Colors.white10,
                  margin: const EdgeInsets.only(bottom: 12),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            const CircleAvatar(backgroundColor: Colors.blueGrey, child: Icon(Icons.person)),
                            const SizedBox(width: 12),
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(post['author'], style: const TextStyle(fontWeight: FontWeight.bold)),
                                Text('Type: ${post['type']}', style: const TextStyle(fontSize: 12, color: Colors.white54)),
                              ],
                            ),
                            const Spacer(),
                            IconButton(
                              icon: const Icon(Icons.delete, color: Colors.redAccent),
                              onPressed: () => _deletePost(post['id']),
                              tooltip: 'Delete Post',
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                        Text(post['content'] ?? ''),
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
