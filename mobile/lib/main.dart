import 'package:flutter/material.dart';

void main() {
  runApp(const TradingBotApp());
}

class TradingBotApp extends StatelessWidget {
  const TradingBotApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Trading Bot',
      theme: ThemeData.dark(),
      home: const DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Trading Bot Dashboard'),
      ),
      body: const Center(
        child: Text('Mobile Interface Placeholder'),
      ),
    );
  }
}
