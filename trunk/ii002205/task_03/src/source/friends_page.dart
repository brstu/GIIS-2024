import 'package:flutter/material.dart';
import 'package:giis3/api_service.dart';

class FriendsPage extends StatefulWidget {
  const FriendsPage({super.key});

  @override
  State<StatefulWidget> createState() {
    return FriendsPageState();
  }
}

class FriendsPageState extends State<FriendsPage> {
  String myId = "1";

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
      Person? myPerson = Person.getPersonById(myId);
      if (myPerson == null) return const Text("Ошибка");
      return Expanded(
          child: GridView(
        gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
            maxCrossAxisExtent: 200, mainAxisExtent: 80),
        children: List.generate(myPerson.friendIds.length, (index) {
          Person? friend = Person.getPersonById(myPerson.friendIds[index]);
          if (friend == null) {
            return const Card(
              child: Padding(
                  padding: EdgeInsets.all(5),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Padding(
                        padding: EdgeInsets.all(5),
                        child: Text("Пользователь не найден"),
                      )
                    ],
                  )),
            );
          }
          return Card(
            child: Padding(
                padding: const EdgeInsets.all(5),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(5),
                      child: Text(friend.nickname),
                    ),
                    TextButton.icon(
                        onPressed: () {},
                        icon: const Icon(Icons.delete),
                        label: const Text("Удалить"))
                  ],
                )),
          );
        }),
      ));
    });
  }
}
