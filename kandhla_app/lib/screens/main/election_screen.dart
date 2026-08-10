import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../theme/glass_widgets.dart';
import '../../services/election_service.dart';
import '../../models/election_model.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'nomination_screen.dart';
import 'live_results_screen.dart';

class ElectionScreen extends StatefulWidget {
  const ElectionScreen({super.key});

  @override
  State<ElectionScreen> createState() => _ElectionScreenState();
}

class _ElectionScreenState extends State<ElectionScreen> {
  final ElectionService _electionService = ElectionService();
  List<ElectionModel> _activeElections = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchElections();
  }

  Future<void> _fetchElections() async {
    final elections = await _electionService.fetchActiveElections();
    setState(() {
      _activeElections = elections;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Election Hub'),
        actions: [
          TextButton.icon(
            onPressed: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => const NominationScreen()));
            },
            icon: const Icon(Icons.edit_document, color: AppTheme.primaryGold),
            label: const Text('Parcha Bharo', style: TextStyle(color: AppTheme.primaryGold, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _activeElections.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: const [
                      Text('🗳️', style: TextStyle(fontSize: 48)),
                      SizedBox(height: 16),
                      Text('No Active Elections.', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                      SizedBox(height: 8),
                      Text('Stay tuned for upcoming democratic processes.', style: TextStyle(color: AppTheme.textMuted)),
                    ],
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: _activeElections.length,
                  itemBuilder: (context, index) {
                    return _buildElectionCard(_activeElections[index]);
                  },
                ),
    );
  }

  Widget _buildElectionCard(ElectionModel election) {
    return GlassContainer(
      borderColor: AppTheme.primaryGold.withValues(alpha: 0.5),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(election.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: AppTheme.primaryGold)),
          const SizedBox(height: 4),
          Text('Phase: ${election.phase.toUpperCase()}', style: const TextStyle(color: AppTheme.primaryRed, fontWeight: FontWeight.bold, fontSize: 12)),
          const SizedBox(height: 8),
          Text('Ends on: ${election.endDate.split('T').first}', style: const TextStyle(color: AppTheme.textMuted, fontSize: 12)),
          const SizedBox(height: 16),
          if (election.phase == 'voting')
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.push(context, MaterialPageRoute(builder: (_) => VotingScreen(electionId: election.id)));
                },
                child: const Text('Cast Vote'),
              ),
            )
          else if (election.phase == 'results')
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.push(context, MaterialPageRoute(builder: (_) => LiveResultsScreen(electionName: election.name)));
                },
                style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGold),
                child: const Text('View Live Results', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
              ),
            )
          else
            const Center(child: Text('Voting is not active for this phase', style: TextStyle(color: AppTheme.textMuted, fontSize: 12))),
        ],
      ),
    );
  }
}

class VotingScreen extends StatefulWidget {
  final String electionId;
  const VotingScreen({super.key, required this.electionId});

  @override
  State<VotingScreen> createState() => _VotingScreenState();
}

class _VotingScreenState extends State<VotingScreen> {
  final ElectionService _electionService = ElectionService();
  List<CandidateModel> _candidates = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchCandidates();
  }

  Future<void> _fetchCandidates() async {
    final candidates = await _electionService.fetchCandidates(widget.electionId);
    setState(() {
      _candidates = candidates;
      _isLoading = false;
    });
  }

  void _castVote(String candidateId) async {
    // In production, get the real device ID string.
    final prefs = await SharedPreferences.getInstance();
    final deviceId = prefs.getString('device_id') ?? 'test-device-id';
    
    if (!mounted) return;
    
    // Optimistic UI interaction
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Casting secure vote...'), duration: Duration(seconds: 1)),
    );

    final success = await _electionService.castVote(widget.electionId, candidateId, deviceId);
    
    if (!mounted) return;
    
    if (success) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Vote successfully added to queue!'), backgroundColor: AppTheme.primaryGreen),
      );
      Navigator.of(context).pop(); // Go back after voting
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Failed to cast vote.'), backgroundColor: AppTheme.primaryRed),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Ballot Paper')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _candidates.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: const [
                      Text('👥', style: TextStyle(fontSize: 48)),
                      SizedBox(height: 16),
                      Text('No Candidates Yet.', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                      SizedBox(height: 8),
                      Text('Candidates have not been finalized.', style: TextStyle(color: AppTheme.textMuted)),
                    ],
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: _candidates.length,
                  itemBuilder: (context, index) {
                    final candidate = _candidates[index];
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 12.0),
                      child: GlassContainer(
                        child: ListTile(
                          leading: candidate.symbolUrl.isNotEmpty 
                              ? Image.network(candidate.symbolUrl, width: 40, height: 40, errorBuilder: (context, error, stackTrace) => const Icon(Icons.person, color: Colors.white))
                              : const Icon(Icons.person, color: Colors.white),
                          title: Text(candidate.name, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                          subtitle: Text(candidate.manifesto, maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(color: AppTheme.textMuted, fontSize: 12)),
                          trailing: ElevatedButton(
                            onPressed: () => _castVote(candidate.id),
                            style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryBlue),
                            child: const Text('VOTE'),
                          ),
                        ),
                      ),
                    );
                  },
                ),
    );
  }
}
