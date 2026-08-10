import 'package:flutter/material.dart';

class DashboardLayout extends StatelessWidget {
  final Widget child;
  final String title;

  const DashboardLayout({super.key, required this.child, required this.title});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          // Sidebar
          Container(
            width: 250,
            color: const Color(0xFF0F172A),
            child: Column(
              children: [
                const Padding(
                  padding: EdgeInsets.all(24.0),
                  child: Text(
                    'MASTER CONTROL',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFFFBBF24),
                    ),
                  ),
                ),
                ListTile(
                  leading: const Icon(Icons.dashboard, color: Colors.white70),
                  title: const Text('Dashboard', style: TextStyle(color: Colors.white70)),
                  onTap: () {},
                ),
                ListTile(
                  leading: const Icon(Icons.location_city, color: Colors.white),
                  title: const Text('Cities Management', style: TextStyle(color: Colors.white)),
                  onTap: () {
                    Navigator.pushReplacementNamed(context, '/cities');
                  },
                ),
                ListTile(
                  leading: const Icon(Icons.people, color: Colors.white),
                  title: const Text('Users & Moderation', style: TextStyle(color: Colors.white)),
                  onTap: () {
                    Navigator.pushReplacementNamed(context, '/users');
                  },
                ),
                ListTile(
                  leading: const Icon(Icons.campaign, color: Colors.white70),
                  title: const Text('Ads Network', style: TextStyle(color: Colors.white70)),
                  onTap: () {
                    Navigator.pushReplacementNamed(context, '/ads');
                  },
                ),
                ListTile(
                  leading: const Icon(Icons.article, color: Colors.white70),
                  title: const Text('Content Feed', style: TextStyle(color: Colors.white70)),
                  onTap: () {
                    Navigator.pushReplacementNamed(context, '/content');
                  },
                ),
                ListTile(
                  leading: const Icon(Icons.how_to_vote, color: Colors.white70),
                  title: const Text('Elections (EC)', style: TextStyle(color: Colors.white70)),
                  onTap: () {
                    Navigator.pushReplacementNamed(context, '/elections');
                  },
                ),
                ListTile(
                  leading: const Icon(Icons.location_city, color: Colors.white),
                  title: const Text('Mohallas', style: TextStyle(color: Colors.white)),
                  onTap: () {
                    Navigator.pushReplacementNamed(context, '/mohallas');
                  },
                ),
                const Spacer(),
                ListTile(
                  leading: const Icon(Icons.logout, color: Colors.redAccent),
                  title: const Text('Logout', style: TextStyle(color: Colors.redAccent)),
                  onTap: () {
                    Navigator.pushReplacementNamed(context, '/login');
                  },
                ),
              ],
            ),
          ),
          // Main Content Area
          Expanded(
            child: Column(
              children: [
                // Topbar
                Container(
                  height: 60,
                  padding: const EdgeInsets.symmetric(horizontal: 24),
                  decoration: const BoxDecoration(
                    color: Color(0xFF0A0F1C),
                    border: Border(bottom: BorderSide(color: Colors.white10)),
                  ),
                  child: Row(
                    children: [
                      Text(title, style: const TextStyle(color: Colors.white70)),
                      const Spacer(),
                      const CircleAvatar(
                        backgroundColor: Colors.white10,
                        child: Icon(Icons.person, color: Colors.white),
                      ),
                    ],
                  ),
                ),
                // Content
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(24.0),
                    child: child,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
