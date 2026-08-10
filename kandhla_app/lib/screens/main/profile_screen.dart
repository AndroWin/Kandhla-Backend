import 'package:flutter/material.dart';
import 'election_screen.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import '../../services/user_service.dart';
import '../vip/mantralaya_dashboard.dart';
import '../utilities/edit_profile_screen.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final UserService _userService = UserService();
  late Future<UserProfile?> _profileFuture;

  @override
  void initState() {
    super.initState();
    _profileFuture = _userService.fetchMyProfile();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        actions: [
          IconButton(
            icon: const Text('⚙️', style: TextStyle(fontSize: 20)),
            onPressed: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => const EditProfileScreen()));
            },
          )
        ],
      ),
      body: FutureBuilder<UserProfile?>(
        future: _profileFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError || !snapshot.hasData || snapshot.data == null) {
            return const Center(child: Text('Failed to load profile', style: TextStyle(color: Colors.red)));
          }

          final user = snapshot.data!;
          
          Color frameColor = AppTheme.glassBorder;
          LinearGradient? rubyGradient;
          String roleIcon = '👤';
          String roleTitle = 'Citizen';
          
          switch (user.role) {
            case 'supreme_minister':
              frameColor = AppTheme.primaryGold;
              rubyGradient = AppTheme.rubyRed;
              roleIcon = '👑';
              roleTitle = 'Supreme Minister';
              break;
            case 'cabinet_minister':
              frameColor = AppTheme.primaryPurple;
              rubyGradient = AppTheme.rubyViolet;
              roleIcon = '🛡️';
              roleTitle = 'Cabinet Minister';
              break;
            case 'mohalla_minister':
              frameColor = AppTheme.primaryGreen;
              rubyGradient = AppTheme.rubyGreen;
              roleIcon = '🟢';
              roleTitle = 'Mohalla Minister';
              break;
            case 'mohalla_cabinet':
              frameColor = Colors.grey;
              rubyGradient = AppTheme.rubyGrey;
              roleIcon = '⚙️';
              roleTitle = 'Mohalla Cabinet';
              break;
            case 'admin':
              frameColor = AppTheme.primaryBlue;
              roleIcon = '🛠️';
              roleTitle = 'City Admin';
              break;
            default:
              frameColor = AppTheme.glassBorder;
              roleIcon = '👤';
              roleTitle = 'Citizen';
          }

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                const SizedBox(height: 20),
                Center(
                  child: Stack(
                    clipBehavior: Clip.none,
                    children: [
                      Container(
                        width: 100,
                        height: 100,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          border: Border.all(color: frameColor, width: 3),
                          color: AppTheme.bgPanel,
                        ),
                        child: user.profileImage != null && user.profileImage!.isNotEmpty
                            ? ClipRRect(
                                borderRadius: BorderRadius.circular(50),
                                child: Image.network(user.profileImage!, fit: BoxFit.cover),
                              )
                            : const Center(child: Text('👤', style: TextStyle(fontSize: 40))),
                      ),
                      if (rubyGradient != null)
                        Positioned(
                          bottom: -5,
                          right: -5,
                          child: Container(
                            width: 24,
                            height: 24,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              gradient: rubyGradient,
                              border: Border.all(color: Colors.white, width: 1.5),
                              boxShadow: [
                                BoxShadow(
                                  color: rubyGradient.colors.last.withValues(alpha: 0.5),
                                  blurRadius: 10,
                                  spreadRadius: 2,
                                )
                              ],
                            ),
                          ),
                        )
                    ],
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  user.name,
                  style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 4),
                Text(
                  '$roleIcon ${roleTitle.toUpperCase()}',
                  style: TextStyle(color: frameColor, fontSize: 14, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 24),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Column(
                      children: [
                        Text('${user.credibilityScore}', style: const TextStyle(color: AppTheme.primaryBlue, fontWeight: FontWeight.bold, fontSize: 18)),
                        const Text('Credibility', style: TextStyle(color: AppTheme.textMuted, fontSize: 12)),
                      ],
                    ),
                    const SizedBox(width: 40),
                    Column(
                      children: [
                        Text('${user.postsCount}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                        const Text('Posts', style: TextStyle(color: AppTheme.textMuted, fontSize: 12)),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 24),
                if (user.role == 'supreme_minister' || user.role == 'cabinet_minister' || user.role == 'mohalla_minister' || user.role == 'admin') ...[
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      onPressed: () {
                        Navigator.push(context, MaterialPageRoute(builder: (_) => MantralayaDashboard(role: user.role)));
                      },
                      icon: const Icon(Icons.shield, color: Colors.white),
                      label: const Text('VIP Mantralaya Hub'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppTheme.primaryGold,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),
                ],
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: () {
                      Navigator.push(context, MaterialPageRoute(builder: (_) => const ElectionScreen()));
                    },
                    icon: const Icon(Icons.how_to_vote, color: Colors.white),
                    label: const Text('Election Hub'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppTheme.primaryBlue,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                  ),
                ),
                const SizedBox(height: 40),
                GlassContainer(
                  child: const Center(
                    child: Text('More profile details and settings will appear here.', style: TextStyle(color: AppTheme.textMuted)),
                  ),
                ),
              ],
            ),
          );
        }
      ),
    );
  }
}
