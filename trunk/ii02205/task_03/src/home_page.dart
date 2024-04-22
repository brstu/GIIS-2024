import 'package:flutter/material.dart';
import 'package:giis3/api_service.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<StatefulWidget> createState() {
    return HomePageState();
  }
}

class HomePageState extends State<HomePage> {
  @override
  Widget build(context) {
    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false,
        title: const Text("Социальная сеть Абоба"),
        backgroundColor: Colors.blueGrey,
      ),
      body: Row(
        children: [getSidePanel(), const VerticalDivider(), getMainContent()],
      ),
    );
  }

  Widget getSidePanel() {
    return StatefulBuilder(builder: (context, setSideState) {
      return SizedBox(
        width: 250,
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 10),
          child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              // mainAxisAlignment: MainAxisAlignment.start,
              children: List.generate(sideRoutes.length, (index) {
                SideRoute value = sideRoutes[index];

                return TextButton.icon(
                    onPressed: () {
                      Navigator.pushNamed(context, value.route);
                    },
                    icon: Icon(value.icon),
                    label: IntrinsicWidth(
                      child: Text(value.label),
                    ));
              })),
        ),
      );
    });
  }

  Widget getMainContent() {
    return StatefulBuilder(builder: (context, setMainState) {
      DB.posts.shuffle();
      return Expanded(
          child: Column(
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(15),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text("Новый пост"),
                  const TextField(),
                  const SizedBox(
                    height: 10,
                  ),
                  TextButton(
                    onPressed: () {},
                    style: ButtonStyle(
                        backgroundColor: MaterialStateColor.resolveWith(
                            (states) =>
                                const Color.fromARGB(255, 18, 198, 138))),
                    child: const Text("Опубликовать"),
                  )
                ],
              ),
            ),
          ),
          Expanded(
              child: ListView(
                  children: List.generate(DB.posts.length, (index) {
            Post postInfo = DB.posts[index];
            return Card(
              child: Padding(
                padding: const EdgeInsets.all(15),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      Person.getNicknameById(postInfo.userId),
                      style: const TextStyle(fontSize: 20),
                    ),
                    const Divider(),
                    Text(postInfo.label)
                  ],
                ),
              ),
            );
          })))
        ],
      ));
    });
  }
}
