import 'package:flutter/material.dart';

class AppTheme {
  // Brand Colors
  static const Color primaryBlue = Color(0xFF0ea5e9);
  static const Color primaryGold = Color(0xFFfbbf24);
  static const Color primaryGreen = Color(0xFF22c55e);
  static const Color primaryRed = Color(0xFFef4444);
  static const Color primaryPurple = Color(0xFFc084fc);

  // Background Colors
  static const Color bgDark = Color(0xFF0a0f1c);
  static const Color bgPanel = Color(0xFF111827);

  // Glassmorphism Colors
  static const Color glassBg = Color(0x0CFFFFFF); // 5% opacity white
  static const Color glassBorder = Color(0x19FFFFFF); // 10% opacity white
  
  // Text Colors
  static const Color textMuted = Color(0xFFcbd5e1);
  static const Color textWhite = Colors.white;

  // Linear Gradients for Rubies
  static const LinearGradient rubyRed = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF991b1b), Color(0xFFdc2626)],
  );

  static const LinearGradient rubyViolet = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF7e22ce), Color(0xFFc026d3)],
  );

  static const LinearGradient rubyGreen = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF166534), Color(0xFF22c55e)],
  );

  static const LinearGradient rubyGrey = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [Color(0xFF4b5563), Color(0xFF9ca3af)],
  );

  static ThemeData get darkTheme {
    return ThemeData(
      brightness: Brightness.dark,
      scaffoldBackgroundColor: bgDark,
      primaryColor: primaryBlue,
      fontFamily: 'Segoe UI',
      colorScheme: const ColorScheme.dark(
        primary: primaryBlue,
        secondary: primaryGold,
        surface: bgPanel,
      ),
      textTheme: const TextTheme(
        displayLarge: TextStyle(color: textWhite, fontWeight: FontWeight.bold),
        bodyLarge: TextStyle(color: textWhite),
        bodyMedium: TextStyle(color: textMuted),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
        iconTheme: IconThemeData(color: primaryBlue),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.black38,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: glassBorder),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: glassBorder),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: primaryBlue),
        ),
        labelStyle: const TextStyle(color: primaryBlue),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryBlue,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 8),
          textStyle: const TextStyle(fontWeight: FontWeight.bold),
        ),
      ),
    );
  }
}
