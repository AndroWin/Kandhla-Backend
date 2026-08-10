import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import '../../models/concern_model.dart';
import '../utilities/image_viewer_screen.dart';

class SingleConcernScreen extends StatefulWidget {
  final ConcernModel concern;

  const SingleConcernScreen({super.key, required this.concern});

  @override
  State<SingleConcernScreen> createState() => _SingleConcernScreenState();
}

class _SingleConcernScreenState extends State<SingleConcernScreen> {
  late int _supportCount;
  late int _rejectCount;
  final TextEditingController _commentController = TextEditingController();
  final List<String> _comments = [
    'We need this fixed immediately!',
    'I agree, the condition is terrible.',
    'I have already complained to the municipality.',
  ];

  @override
  void initState() {
    super.initState();
    _supportCount = widget.concern.supportCount;
    _rejectCount = widget.concern.doNotSupportCount;
  }

  void _handleInteraction(String type) {
    setState(() {
      if (type == 'support') {
        _supportCount++;
      } else {
        _rejectCount++;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Concern Details'),
        backgroundColor: AppTheme.bgDark,
        elevation: 0,
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [AppTheme.bgDark, AppTheme.bgPanel],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: Column(
          children: [
            Expanded(
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  GlassContainer(
                    borderColor: widget.concern.escalatedToCity ? AppTheme.primaryGold : AppTheme.glassBorder,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Expanded(
                              child: Text(
                                widget.concern.title,
                                style: const TextStyle(color: AppTheme.primaryRed, fontWeight: FontWeight.bold, fontSize: 18),
                              ),
                            ),
                            if (widget.concern.escalatedToCity)
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                decoration: BoxDecoration(
                                  color: AppTheme.primaryGold,
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: const Text(
                                  'City Priority',
                                  style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
                                ),
                              )
                          ],
                        ),
                        const SizedBox(height: 12),
                        Text(widget.concern.description, style: const TextStyle(fontSize: 16, color: Colors.white, height: 1.4)),
                        const SizedBox(height: 16),
                        if (widget.concern.imageUrl != null && widget.concern.imageUrl!.isNotEmpty)
                          GestureDetector(
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => ImageViewerScreen(
                                    imageUrl: widget.concern.imageUrl!,
                                    tag: 'single_concern_image_${widget.concern.id}',
                                  ),
                                ),
                              );
                            },
                            child: Hero(
                              tag: 'single_concern_image_${widget.concern.id}',
                              child: ClipRRect(
                                borderRadius: BorderRadius.circular(8),
                                child: Image.network(
                                  widget.concern.imageUrl!,
                                  width: double.infinity,
                                  height: 250,
                                  fit: BoxFit.cover,
                                ),
                              ),
                            ),
                          ),
                        const SizedBox(height: 16),
                        Text('Raised by: ${widget.concern.authorName}', style: const TextStyle(color: AppTheme.textMuted, fontSize: 12)),
                        const SizedBox(height: 16),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceAround,
                          children: [
                            InkWell(
                              onTap: () => _handleInteraction('support'),
                              child: Container(
                                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                                decoration: BoxDecoration(
                                  color: AppTheme.primaryBlue.withValues(alpha: 0.2),
                                  borderRadius: BorderRadius.circular(16),
                                ),
                                child: AnimatedSwitcher(
                                  duration: const Duration(milliseconds: 300),
                                  transitionBuilder: (Widget child, Animation<double> animation) {
                                    return ScaleTransition(scale: animation, child: child);
                                  },
                                  child: Text(
                                    '✅ Support ($_supportCount)', 
                                    key: ValueKey<int>(_supportCount),
                                    style: const TextStyle(color: AppTheme.primaryBlue, fontSize: 14, fontWeight: FontWeight.bold)
                                  ),
                                ),
                              ),
                            ),
                            InkWell(
                              onTap: () => _handleInteraction('do_not_support'),
                              child: Container(
                                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                                decoration: BoxDecoration(
                                  color: Colors.white.withValues(alpha: 0.1),
                                  borderRadius: BorderRadius.circular(16),
                                ),
                                child: AnimatedSwitcher(
                                  duration: const Duration(milliseconds: 300),
                                  transitionBuilder: (Widget child, Animation<double> animation) {
                                    return ScaleTransition(scale: animation, child: child);
                                  },
                                  child: Text(
                                    '❌ Reject ($_rejectCount)', 
                                    key: ValueKey<int>(_rejectCount),
                                    style: const TextStyle(fontSize: 14, color: Colors.white)
                                  ),
                                ),
                              ),
                            ),
                          ],
                        )
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),
                  const Text('Discussion', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18)),
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
              child: SafeArea(
                child: Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: _commentController,
                        style: const TextStyle(color: Colors.white),
                        decoration: InputDecoration(
                          hintText: 'Add to the discussion...',
                          hintStyle: const TextStyle(color: AppTheme.textMuted),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(20),
                            borderSide: BorderSide.none,
                          ),
                          filled: true,
                          fillColor: Colors.black26,
                          contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    CircleAvatar(
                      backgroundColor: AppTheme.primaryGold,
                      child: IconButton(
                        icon: const Icon(Icons.send, color: Colors.black, size: 18),
                        onPressed: () {
                          if (_commentController.text.isNotEmpty) {
                            setState(() {
                              _comments.add(_commentController.text);
                              _commentController.clear();
                            });
                          }
                        },
                      ),
                    )
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
