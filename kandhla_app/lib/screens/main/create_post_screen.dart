import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import '../../services/feed_service.dart';

class CreatePostScreen extends StatefulWidget {
  const CreatePostScreen({super.key});

  @override
  State<CreatePostScreen> createState() => _CreatePostScreenState();
}

class _CreatePostScreenState extends State<CreatePostScreen> {
  int _selectedTab = 0; // 0: Normal, 1: Concern, 2: Whistleblower
  final _contentController = TextEditingController();
  bool _isPinned = false;
  bool _isLoading = false;
  final FeedService _feedService = FeedService();

  @override
  void dispose() {
    _contentController.dispose();
    super.dispose();
  }

  void _submitPost() async {
    final content = _contentController.text.trim();
    if (content.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Content cannot be empty')));
      return;
    }

    setState(() => _isLoading = true);

    bool success = false;
    
    if (_selectedTab == 1) {
      // It's a Concern
      // For title, we can extract the first few words of content, or add a title field.
      // Since we don't have a title field in UI yet, let's use the first 20 chars of content as title.
      String title = content.length > 20 ? '${content.substring(0, 20)}...' : content;
      success = await _feedService.createConcern(title, content, 'general');
    } else {
      String type = 'normal';
      if (_selectedTab == 2) type = 'whistleblower';

      success = await _feedService.createPost(content, type, _isPinned);
    }

    if (!mounted) return;
    setState(() => _isLoading = false);

    if (success) {
      _contentController.clear();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(_selectedTab == 1 ? 'Concern Raised!' : 'Post published!'), backgroundColor: AppTheme.primaryGreen),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(_selectedTab == 1 ? 'Failed to raise concern.' : 'Failed to publish post.'), backgroundColor: AppTheme.primaryRed),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Create Post'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildTab(0, 'Normal'),
                _buildTab(1, 'Concern'),
                _buildTab(2, 'Whistleblower'),
              ],
            ),
          ),
          const Divider(color: AppTheme.glassBorder),
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  TextField(
                    controller: _contentController,
                    maxLines: 5,
                    decoration: InputDecoration(
                      hintText: _selectedTab == 1 
                          ? 'Describe the issue...' 
                          : _selectedTab == 2 
                              ? 'Report anonymously...' 
                              : 'What\'s happening?',
                    ),
                  ),
                  const SizedBox(height: 16),
                  GlassContainer(
                    width: double.infinity,
                    padding: const EdgeInsets.all(20),
                    child: const Center(
                      child: Text('📷 Add Image', style: TextStyle(color: AppTheme.textMuted)),
                    ),
                  ),
                  const SizedBox(height: 16),
                  if (_selectedTab == 0) ...[
                    Row(
                      children: [
                        Checkbox(
                          value: _isPinned,
                          onChanged: (v) => setState(() => _isPinned = v ?? false),
                          activeColor: AppTheme.primaryBlue,
                        ),
                        const Text('Mark as Official Order (Ministers Only)', style: TextStyle(fontSize: 12, color: AppTheme.textMuted)),
                      ],
                    ),
                  ],
                  const SizedBox(height: 24),
                  SizedBox(
                    width: double.infinity,
                    height: 50,
                    child: ElevatedButton(
                      onPressed: _isLoading ? null : _submitPost,
                      child: _isLoading
                          ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.white))
                          : const Text('Post'),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTab(int index, String title) {
    final isSelected = _selectedTab == index;
    return GestureDetector(
      onTap: () => setState(() => _selectedTab = index),
      child: Container(
        padding: const EdgeInsets.only(bottom: 4),
        decoration: BoxDecoration(
          border: Border(
            bottom: BorderSide(
              color: isSelected ? AppTheme.primaryBlue : Colors.transparent,
              width: 2,
            ),
          ),
        ),
        child: Text(
          title,
          style: TextStyle(
            color: isSelected ? AppTheme.primaryBlue : AppTheme.textMuted,
            fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
            fontSize: 14,
          ),
        ),
      ),
    );
  }
}
