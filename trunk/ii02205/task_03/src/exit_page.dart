import 'package:flutter/material.dart';

class ExitPage extends StatefulWidget {
  const ExitPage({super.key});

  @override
  State<StatefulWidget> createState() {
    return ExitPageState();
  }
}

class ExitPageState extends State<ExitPage> {
  @override
  Widget build(context) {
    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false,
        title: const Text("Социальная сеть Абоба"),
        backgroundColor: Colors.blueGrey,
      ),
      body: const Center(child: Text("Пока...")),
    );
  }
}
