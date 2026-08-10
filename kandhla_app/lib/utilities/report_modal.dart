import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class ReportModal {
  static void show(BuildContext context, {required String targetId, required String type}) {
    final TextEditingController reasonController = TextEditingController();

    showModalBottomSheet(
      context: context,
      backgroundColor: AppTheme.bgPanel,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      isScrollControlled: true,
      builder: (context) {
        return Padding(
          padding: EdgeInsets.only(
            left: 16,
            right: 16,
            top: 24,
            bottom: MediaQuery.of(context).viewInsets.bottom + 24,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Report Violation', style: TextStyle(color: AppTheme.primaryRed, fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Text('Reporting $type ($targetId)', style: const TextStyle(color: AppTheme.textMuted, fontSize: 12)),
              const SizedBox(height: 16),
              const Text('Please describe the issue:', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              TextField(
                controller: reasonController,
                maxLines: 4,
                style: const TextStyle(color: Colors.white),
                decoration: const InputDecoration(
                  hintText: 'Spam, abuse, misinformation...',
                  hintStyle: TextStyle(color: AppTheme.textMuted),
                ),
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    if (reasonController.text.trim().isEmpty) return;
                    // Mock API call to send report to Mod Queue
                    Navigator.pop(context);
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Report submitted to Mod Queue.'), backgroundColor: AppTheme.primaryRed),
                    );
                  },
                  style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryRed),
                  child: const Text('Submit Report'),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
