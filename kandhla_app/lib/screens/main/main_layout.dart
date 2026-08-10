import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import 'home_feed_screen.dart';
import 'explore_screen.dart';
import 'create_post_screen.dart';
import 'profile_screen.dart';

class MainLayout extends StatefulWidget {
  const MainLayout({super.key});

  @override
  State<MainLayout> createState() => _MainLayoutState();
}

class _MainLayoutState extends State<MainLayout> {
  int _currentIndex = 0;

  final List<Widget> _screens = [
    const HomeFeedScreen(),
    const ExploreScreen(),
    const CreatePostScreen(),
    const ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.bgDark,
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          border: Border(
            top: BorderSide(color: AppTheme.glassBorder, width: 1),
          ),
        ),
        child: BottomNavigationBar(
          currentIndex: _currentIndex,
          onTap: (index) {
            setState(() {
              _currentIndex = index;
            });
          },
          backgroundColor: AppTheme.bgPanel,
          selectedItemColor: AppTheme.primaryBlue,
          unselectedItemColor: AppTheme.textMuted,
          type: BottomNavigationBarType.fixed,
          showUnselectedLabels: true,
          items: const [
            BottomNavigationBarItem(
              icon: Text('🏠', style: TextStyle(fontSize: 20)),
              label: 'Feed',
            ),
            BottomNavigationBarItem(
              icon: Text('🌍', style: TextStyle(fontSize: 20)),
              label: 'Explore',
            ),
            BottomNavigationBarItem(
              icon: Text('➕', style: TextStyle(fontSize: 20)),
              label: 'Post',
            ),
            BottomNavigationBarItem(
              icon: Text('👤', style: TextStyle(fontSize: 20)),
              label: 'Profile',
            ),
          ],
        ),
      ),
    );
  }
}
