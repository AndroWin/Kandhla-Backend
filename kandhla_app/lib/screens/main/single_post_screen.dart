import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import '../../models/post_model.dart';

class SinglePostScreen extends StatefulWidget {
  final PostModel post;
  
  const SinglePostScreen({super.key, required this.post});

  @override
  State<SinglePostScreen> createState() => _SinglePostScreenState();
}

class _SinglePostScreenState extends State<SinglePostScreen> {
  final TextEditingController _commentController = TextEditingController();
  final List<String> _comments = [
    'Totally agree with this!',
    'Can we discuss this in the next meeting?',
  ];

  @override
  void dispose() {
    _commentController.dispose();
    super.dispose();
  }

  void _addComment() {
    if (_commentController.text.trim().isNotEmpty) {
      setState(() {
        _comments.add(_commentController.text.trim());
        _commentController.clear();
      });
      FocusScope.of(context).unfocus();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Post Thread'),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(12),
              children: [
                GlassContainer(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          CircleAvatar(
                            backgroundColor: Colors.grey.shade700,
                            backgroundImage: widget.post.authorAvatar.isNotEmpty
                                ? NetworkImage(widget.post.authorAvatar) 
                                : null,
                            child: widget.post.authorAvatar.isEmpty ? const Icon(Icons.person, color: Colors.white) : null,
                          ),
                          const SizedBox(width: 12),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(widget.post.authorName, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                              Text(widget.post.type.toUpperCase(), style: TextStyle(color: _getTypeColor(widget.post.type), fontSize: 10, fontWeight: FontWeight.bold)),
                            ],
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Text(widget.post.content, style: const TextStyle(color: Colors.white, fontSize: 16, height: 1.4)),
                      const SizedBox(height: 16),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          _buildInteraction(Icons.thumb_up, widget.post.upvotes.toString(), AppTheme.primaryBlue),
                          _buildInteraction(Icons.thumb_down, widget.post.downvotes.toString(), AppTheme.primaryRed),
                          _buildInteraction(Icons.comment, _comments.length.toString(), Colors.grey),
                        ],
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 24),
                const Text('Comments', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 16)),
                const SizedBox(height: 12),
                ..._comments.map((c) => Padding(
                  padding: const EdgeInsets.only(bottom: 8.0),
                  child: GlassContainer(
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const CircleAvatar(radius: 12, backgroundColor: Colors.grey, child: Icon(Icons.person, size: 16, color: Colors.white)),
                        const SizedBox(width: 12),
                        Expanded(child: Text(c, style: const TextStyle(color: Colors.white))),
                      ],
                    ),
                  ),
                )),
              ],
            ),
          ),
          // Sticky Comment Box
          Container(
            padding: const EdgeInsets.all(12),
            decoration: const BoxDecoration(
              color: AppTheme.bgPanel,
              border: Border(top: BorderSide(color: AppTheme.glassBorder)),
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _commentController,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: 'Write a comment...',
                      hintStyle: const TextStyle(color: AppTheme.textMuted),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(25),
                        borderSide: BorderSide.none,
                      ),
                      filled: true,
                      fillColor: Colors.black38,
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  onPressed: _addComment,
                  icon: const Icon(Icons.send, color: AppTheme.primaryBlue),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInteraction(IconData icon, String count, Color color) {
    return Row(
      children: [
        Icon(icon, size: 18, color: color),
        const SizedBox(width: 4),
        Text(count, style: const TextStyle(color: AppTheme.textMuted, fontSize: 12)),
      ],
    );
  }

  Color _getTypeColor(String type) {
    switch (type) {
      case 'official_order': return AppTheme.primaryRed;
      case 'announcement': return AppTheme.primaryGold;
      case 'ad': return AppTheme.primaryGreen;
      default: return AppTheme.primaryBlue;
    }
  }
}
