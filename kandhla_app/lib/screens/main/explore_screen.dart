import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import '../../services/ecosystem_service.dart';
import '../../models/ecosystem_model.dart';

class ExploreScreen extends StatefulWidget {
  const ExploreScreen({super.key});

  @override
  State<ExploreScreen> createState() => _ExploreScreenState();
}

class _ExploreScreenState extends State<ExploreScreen> {
  final EcosystemService _ecosystemService = EcosystemService();
  late Future<List<CityModel>> _citiesFuture;
  String _searchQuery = '';
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _citiesFuture = _ecosystemService.fetchCities();
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Explore Democratic Republic'),
      ),
      body: FutureBuilder<List<CityModel>>(
        future: _citiesFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
             return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
             return const Center(child: Text('Error loading ecosystem data.', style: TextStyle(color: Colors.red)));
          }

          final allCities = snapshot.data ?? [];
          final cities = allCities.where((c) => c.name.toLowerCase().contains(_searchQuery.toLowerCase())).toList();

          return Column(
            children: [
              Padding(
                padding: const EdgeInsets.all(12.0),
                child: GlassContainer(
                  child: TextField(
                    controller: _searchController,
                    style: const TextStyle(color: Colors.white),
                    decoration: const InputDecoration(
                      hintText: 'Search Cities...',
                      hintStyle: TextStyle(color: AppTheme.textMuted),
                      prefixIcon: Icon(Icons.search, color: AppTheme.textMuted),
                      border: InputBorder.none,
                      contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                    ),
                    onChanged: (value) {
                      setState(() {
                        _searchQuery = value;
                      });
                    },
                  ),
                ),
              ),
              if (cities.isEmpty)
                Expanded(
                  child: Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: const [
                        Text('🌍', style: TextStyle(fontSize: 48)),
                        SizedBox(height: 16),
                        Text('No cities found.', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                        SizedBox(height: 8),
                        Text('The Republic is expanding. Check back later!', style: TextStyle(color: AppTheme.textMuted)),
                      ],
                    ),
                  ),
                )
              else
                Expanded(
                  child: ListView.builder(
                    padding: const EdgeInsets.symmetric(horizontal: 12),
                    itemCount: cities.length,
                    itemBuilder: (context, index) {
                      final city = cities[index];
              return Padding(
                padding: const EdgeInsets.only(bottom: 16.0),
                child: GlassContainer(
                  child: ExpansionTile(
                    title: Text(city.name, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                    subtitle: Text('Population: ${city.populationCount} | State: ${city.state}', style: const TextStyle(color: AppTheme.textMuted, fontSize: 12)),
                    iconColor: AppTheme.primaryGold,
                    collapsedIconColor: AppTheme.textMuted,
                    children: [
                      FutureBuilder<List<MohallaModel>>(
                        future: _ecosystemService.fetchMohallas(city.id),
                        builder: (context, mohallaSnapshot) {
                          if (mohallaSnapshot.connectionState == ConnectionState.waiting) {
                            return const Padding(
                              padding: EdgeInsets.all(16.0),
                              child: CircularProgressIndicator(),
                            );
                          }
                          final mohallas = mohallaSnapshot.data ?? [];
                          if (mohallas.isEmpty) {
                            return const Padding(
                              padding: EdgeInsets.all(16.0),
                              child: Text('No Mohallas registered.', style: TextStyle(color: AppTheme.textMuted)),
                            );
                          }
                          return Column(
                            children: mohallas.map((mohalla) {
                              return ListTile(
                                leading: const Icon(Icons.location_city, color: AppTheme.primaryBlue),
                                title: Text(mohalla.name, style: const TextStyle(color: Colors.white70)),
                                subtitle: Text('Population: ${mohalla.populationCount}', style: const TextStyle(fontSize: 10, color: AppTheme.textMuted)),
                                trailing: mohalla.hasCabinet 
                                    ? const Icon(Icons.stars, color: AppTheme.primaryGold, size: 16)
                                    : null,
                                onTap: () {
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(content: Text('Inter-mohalla feed coming soon! Comments disabled.'), backgroundColor: AppTheme.primaryBlue),
                                  );
                                },
                              );
                            }).toList(),
                          );
                        }
                      )
                    ],
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  },
),
    );
  }
}
