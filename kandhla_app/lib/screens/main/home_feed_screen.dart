import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import '../../widgets/custom_drawer.dart';
import 'concerns_screen.dart';
import '../../services/feed_service.dart';
import '../../models/post_model.dart';
import 'notifications_screen.dart';
import 'single_post_screen.dart';
import 'other_profile_screen.dart';

class HomeFeedScreen extends StatefulWidget {
  const HomeFeedScreen({super.key});

  @override
  State<HomeFeedScreen> createState() => _HomeFeedScreenState();
}

class _HomeFeedScreenState extends State<HomeFeedScreen> {
  final FeedService _feedService = FeedService();
  List<PostModel> _posts = [];
  bool _isLoading = true;
  bool _hasError = false;
  
  // Example dummy UUID for testing
  final String _dummyMohallaId = '7bcd20c2-d2fb-4646-b494-0de36159491a';

  @override
  void initState() {
    super.initState();
    _refreshFeed();
  }

  Future<void> _refreshFeed() async {
    setState(() {
      _isLoading = true;
      _hasError = false;
    });
    try {
      final posts = await _feedService.fetchMohallaFeed(_dummyMohallaId);
      setState(() {
        _posts = posts;
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
    final post = _posts[index];
    final success = await _feedService.submitInteraction(post.id, 'post', actionType);
    
    if (success) {
      // Optimistic update for now (in a real app, API would return updated count)
      setState(() {
        if (actionType == 'upvote') {
           _posts[index] = PostModel(
             id: post.id,
             authorName: post.authorName,
             authorRole: post.authorRole,
             authorAvatar: post.authorAvatar,
             content: post.content,
             category: post.category,
             type: post.type,
             status: post.status,
             upvotes: post.upvotes + 1,
             downvotes: post.downvotes,
             commentCount: post.commentCount,
             isPinned: post.isPinned,
             createdAt: post.createdAt,
           );
        } else if (actionType == 'downvote') {
           _posts[index] = PostModel(
             id: post.id,
             authorName: post.authorName,
             authorRole: post.authorRole,
             authorAvatar: post.authorAvatar,
             content: post.content,
             category: post.category,
             type: post.type,
             status: post.status,
             upvotes: post.upvotes,
             downvotes: post.downvotes + 1,
             commentCount: post.commentCount,
             isPinned: post.isPinned,
             createdAt: post.createdAt,
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
        title: const Text('Mohalla X'),
        leading: Builder(
          builder: (context) => IconButton(
            icon: const Icon(Icons.menu),
            onPressed: () => Scaffold.of(context).openDrawer(),
          ),
        ),
        actions: [
          IconButton(
            icon: const Text('🚨', style: TextStyle(fontSize: 20)),
            onPressed: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => const ConcernsScreen()));
            },
          ),
          IconButton(
            icon: const Text('🔔', style: TextStyle(fontSize: 20)),
            onPressed: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => const NotificationsScreen()));
            },
          )
        ],
      ),
      drawer: const CustomDrawer(),
      body: RefreshIndicator(
        onRefresh: _refreshFeed,
        child: _buildBody(),
      ),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_hasError) {
      return const Center(child: Text('Error loading feed.', style: TextStyle(color: Colors.red)));
    }
    if (_posts.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Text('📭', style: TextStyle(fontSize: 48)),
            SizedBox(height: 16),
            Text('No posts yet.', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Text('Start the revolution in your Mohalla!', style: TextStyle(color: AppTheme.textMuted)),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(12),
      itemCount: _posts.length,
      itemBuilder: (context, index) {
        final post = _posts[index];
        
        // VIP UI Logic
        Color frameColor = Colors.grey;
        LinearGradient? rubyGradient;
        String roleTitle = '';
        
        if (post.isPinned) {
            frameColor = AppTheme.primaryGold;
        } else {
            switch (post.authorRole) {
              case 'supreme_minister':
                frameColor = AppTheme.primaryGold;
                rubyGradient = AppTheme.rubyRed;
                roleTitle = '👑 Supreme Minister';
                break;
              case 'cabinet_minister':
                frameColor = AppTheme.primaryPurple;
                rubyGradient = AppTheme.rubyViolet;
                roleTitle = '🛡️ Cabinet Minister';
                break;
              case 'mohalla_minister':
                frameColor = AppTheme.primaryGreen;
                rubyGradient = AppTheme.rubyGreen;
                roleTitle = '🟢 Mohalla Minister';
                break;
              case 'mohalla_cabinet':
                frameColor = Colors.grey;
                rubyGradient = AppTheme.rubyGrey;
                roleTitle = '⚙️ Mohalla Cabinet';
                break;
              case 'admin':
                frameColor = AppTheme.primaryBlue;
                roleTitle = '🛠️ City Admin';
                break;
            }
        }

        return Padding(
          padding: const EdgeInsets.only(bottom: 16.0),
          child: GestureDetector(
            onTap: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => SinglePostScreen(post: post)));
            },
            child: GlassContainer(
              borderColor: post.isPinned ? AppTheme.primaryGold.withValues(alpha: 0.5) : AppTheme.glassBorder,
              backgroundColor: post.isPinned ? AppTheme.primaryGold.withValues(alpha: 0.05) : AppTheme.glassBg,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      GestureDetector(
                        onTap: () {
                          Navigator.push(context, MaterialPageRoute(
                            builder: (_) => OtherProfileScreen(
                              userId: post.authorName, // using name as mock ID
                              name: post.authorName,
                              credibilityScore: 500, // mock
                              role: post.authorRole,
                            )
                          ));
                        },
                        child: Stack(
                          clipBehavior: Clip.none,
                          children: [
                            Container(
                              width: 40,
                              height: 40,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                border: Border.all(color: frameColor, width: 2),
                                color: AppTheme.bgPanel,
                              ),
                              child: post.authorAvatar.isNotEmpty
                                ? ClipRRect(
                                    borderRadius: BorderRadius.circular(20),
                                    child: Image.network(post.authorAvatar, fit: BoxFit.cover),
                                  )
                                : const Center(child: Text('👤', style: TextStyle(fontSize: 20))),
                            ),
                        if (rubyGradient != null)
                          Positioned(
                            bottom: -2,
                            right: -2,
                            child: Container(
                              width: 14,
                              height: 14,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                gradient: rubyGradient,
                                border: Border.all(color: Colors.white, width: 1),
                              ),
                            ),
                          )
                      ],
                    ),
                  ), // close GestureDetector
                  const SizedBox(width: 12),
                  Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Text(post.authorName, style: TextStyle(color: post.isPinned ? AppTheme.primaryGold : Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
                              if (post.type == 'official_order')
                                Padding(
                                  padding: const EdgeInsets.only(left: 8.0),
                                  child: Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                    decoration: BoxDecoration(color: AppTheme.primaryRed.withValues(alpha: 0.2), borderRadius: BorderRadius.circular(4), border: Border.all(color: AppTheme.primaryRed)),
                                    child: const Text('OFFICIAL ORDER', style: TextStyle(color: AppTheme.primaryRed, fontSize: 8, fontWeight: FontWeight.bold)),
                                  ),
                                ),
                            ],
                          ),
                          if (roleTitle.isNotEmpty && !post.isPinned)
                            Text(roleTitle, style: TextStyle(color: frameColor, fontSize: 10, fontWeight: FontWeight.bold)),
                          Text(post.createdAt.split('T').first, style: const TextStyle(color: AppTheme.textMuted, fontSize: 10)),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Text(post.content),
                if (!post.isPinned) ...[
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      StreamBuilder<DatabaseEvent>(
                        stream: FirebaseDatabase.instance.ref('/interactions/posts/${post.id}').onValue,
                        builder: (context, snapshot) {
                          int currentUpvotes = post.upvotes;
                          int currentDownvotes = post.downvotes;
                          
                          if (snapshot.hasData && snapshot.data?.snapshot.value != null) {
                            try {
                                final data = snapshot.data!.snapshot.value as Map<dynamic, dynamic>;
                                currentUpvotes = data['likes'] != null ? (data['likes'] as num).toInt() : currentUpvotes;
                                currentDownvotes = data['dislikes'] != null ? (data['dislikes'] as num).toInt() : currentDownvotes;
                            } catch (e) {
                                // Fallback to local state if casting fails
                            }
                          }
                          
                          return Row(
                            children: [
                              InkWell(
                                onTap: () => _handleInteraction(index, 'upvote'),
                                child: Padding(
                                  padding: const EdgeInsets.all(4.0),
                                  child: AnimatedSwitcher(
                                    duration: const Duration(milliseconds: 300),
                                    transitionBuilder: (Widget child, Animation<double> animation) {
                                      return ScaleTransition(scale: animation, child: child);
                                    },
                                    child: Text(
                                      '👍 $currentUpvotes',
                                      key: ValueKey<int>(currentUpvotes),
                                      style: const TextStyle(fontSize: 12, color: AppTheme.textMuted),
                                    ),
                                  ),
                                ),
                              ),
                              const SizedBox(width: 16),
                              InkWell(
                                onTap: () => _handleInteraction(index, 'downvote'),
                                child: Padding(
                                  padding: const EdgeInsets.all(4.0),
                                  child: AnimatedSwitcher(
                                    duration: const Duration(milliseconds: 300),
                                    transitionBuilder: (Widget child, Animation<double> animation) {
                                      return ScaleTransition(scale: animation, child: child);
                                    },
                                    child: Text(
                                      '👎 $currentDownvotes',
                                      key: ValueKey<int>(currentDownvotes),
                                      style: const TextStyle(fontSize: 12, color: AppTheme.textMuted),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          );
                        }
                      ),
                      const SizedBox(width: 16),
                      Padding(
                        padding: const EdgeInsets.all(4.0),
                        child: AnimatedSwitcher(
                          duration: const Duration(milliseconds: 300),
                          transitionBuilder: (Widget child, Animation<double> animation) {
                            return ScaleTransition(scale: animation, child: child);
                          },
                          child: Text(
                            '💬 ${post.commentCount}',
                            key: ValueKey<int>(post.commentCount),
                            style: const TextStyle(fontSize: 12, color: AppTheme.textMuted),
                          ),
                        ),
                      ),
                    ],
                  ),
                ]
              ],
            ),
          ),
          ),
        );
      },
    );
  }
}


