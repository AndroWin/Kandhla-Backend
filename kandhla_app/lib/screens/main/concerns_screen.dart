import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import '../../services/feed_service.dart';
import '../../models/concern_model.dart';
import '../utilities/image_viewer_screen.dart';
import 'single_concern_screen.dart';

class ConcernsScreen extends StatefulWidget {
  const ConcernsScreen({super.key});

  @override
  State<ConcernsScreen> createState() => _ConcernsScreenState();
}

class _ConcernsScreenState extends State<ConcernsScreen> {
  final FeedService _feedService = FeedService();
  List<ConcernModel> _concerns = [];
  bool _isLoading = true;
  bool _hasError = false;

  final String _dummyMohallaId = '7bcd20c2-d2fb-4646-b494-0de36159491a';

  @override
  void initState() {
    super.initState();
    _refreshConcerns();
  }

  Future<void> _refreshConcerns() async {
    setState(() {
      _isLoading = true;
      _hasError = false;
    });
    try {
      final concerns = await _feedService.fetchConcerns(_dummyMohallaId);
      setState(() {
        _concerns = concerns;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _hasError = true;
        _isLoading = false;
      });
    }
  }

  Future<void> _handleInteraction(int index, String actionType) async {
    final concern = _concerns[index];
    final success = await _feedService.submitInteraction(concern.id, 'concern', actionType);
    
    if (success) {
      setState(() {
        if (actionType == 'support') {
           _concerns[index] = ConcernModel(
             id: concern.id,
             authorName: concern.authorName,
             title: concern.title,
             description: concern.description,
             category: concern.category,
             status: concern.status,
             supportCount: concern.supportCount + 1,
             doNotSupportCount: concern.doNotSupportCount,
             escalatedToCity: concern.escalatedToCity,
             createdAt: concern.createdAt,
           );
        } else if (actionType == 'do_not_support') {
           _concerns[index] = ConcernModel(
             id: concern.id,
             authorName: concern.authorName,
             title: concern.title,
             description: concern.description,
             category: concern.category,
             status: concern.status,
             supportCount: concern.supportCount,
             doNotSupportCount: concern.doNotSupportCount + 1,
             escalatedToCity: concern.escalatedToCity,
             createdAt: concern.createdAt,
           );
        }
      });
    } else {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Interaction failed.'), backgroundColor: AppTheme.primaryRed),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Samasya Hub'),
      ),
      body: RefreshIndicator(
        onRefresh: _refreshConcerns,
        child: _buildBody(),
      ),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_hasError) {
      return const Center(child: Text('Error loading concerns.', style: TextStyle(color: Colors.red)));
    }
    if (_concerns.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Text('🛡️', style: TextStyle(fontSize: 48)),
            SizedBox(height: 16),
            Text('No active concerns.', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Text('Your Mohalla is peaceful right now.', style: TextStyle(color: AppTheme.textMuted)),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(12),
      itemCount: _concerns.length,
      itemBuilder: (context, index) {
        final concern = _concerns[index];
        return Padding(
          padding: const EdgeInsets.only(bottom: 16.0),
          child: GestureDetector(
            onTap: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => SingleConcernScreen(concern: concern)));
            },
            child: GlassContainer(
              borderColor: AppTheme.primaryRed.withValues(alpha: 0.5),
              backgroundColor: AppTheme.primaryRed.withValues(alpha: 0.05),
              child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        concern.title,
                        style: const TextStyle(color: AppTheme.primaryRed, fontWeight: FontWeight.bold, fontSize: 16),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: concern.escalatedToCity ? AppTheme.primaryGold : AppTheme.primaryRed,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        concern.escalatedToCity ? 'City Priority' : 'Active',
                        style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
                      ),
                    )
                  ],
                ),
                const SizedBox(height: 8),
                Text(concern.description, style: const TextStyle(fontSize: 14)),
                const SizedBox(height: 12),
                if (concern.imageUrl != null && concern.imageUrl!.isNotEmpty)
                  GestureDetector(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => ImageViewerScreen(
                            imageUrl: concern.imageUrl!,
                            tag: 'concern_image_${concern.id}',
                          ),
                        ),
                      );
                    },
                    child: Padding(
                      padding: const EdgeInsets.only(bottom: 12.0),
                      child: Hero(
                        tag: 'concern_image_${concern.id}',
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: Image.network(
                            concern.imageUrl!,
                            width: double.infinity,
                            height: 200,
                            fit: BoxFit.cover,
                          ),
                        ),
                      ),
                    ),
                  ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('Raised by: ${concern.authorName}', style: const TextStyle(color: AppTheme.textMuted, fontSize: 12)),
                    Row(
                      children: [
                        InkWell(
                          onTap: () => _handleInteraction(index, 'support'),
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
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
                                '✅ Support (${concern.supportCount})', 
                                key: ValueKey<int>(concern.supportCount),
                                style: const TextStyle(color: AppTheme.primaryBlue, fontSize: 12, fontWeight: FontWeight.bold)
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        InkWell(
                          onTap: () => _handleInteraction(index, 'do_not_support'),
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
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
                                '❌ Reject (${concern.doNotSupportCount})', 
                                key: ValueKey<int>(concern.doNotSupportCount),
                                style: const TextStyle(fontSize: 12)
                              ),
                            ),
                          ),
                        ),
                      ],
                    )
                  ],
                ),
              ],
            ),
          ),
          ),
        );
      },
    );
  }
}
