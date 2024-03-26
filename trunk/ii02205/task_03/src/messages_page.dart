import 'package:flutter/material.dart';
import 'package:giis3/api_service.dart';

class MessagePage extends StatefulWidget {
  const MessagePage({super.key});

  @override
  State<StatefulWidget> createState() {
    return MessagePageState();
  }
}

class MessagePageState extends State<MessagePage> {
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
          children: [getSidePanel(), getMainContent()],
        ));
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

  int currentIndex = -1;

  Widget getMainContent() {
    return StatefulBuilder(builder: (context, setMainState) {
      List friendsId = [];
      Person? myPerson = Person.getPersonById(myId);
      if (myPerson != null) {
        friendsId = myPerson.friendIds;
      }

      Person? friend = (currentIndex == -1)
          ? null
          : Person.getPersonById(friendsId[currentIndex]);
      List<Message> messages = [];
      if (friend != null) {
        messages = Message.getMessages(myId, friend.id);
      }

      messages.sort((a, b) {
        return a.date.compareTo(b.date);
      });

      return Expanded(
          child: Container(
              alignment: Alignment.topLeft,
              // color: Colors.blue,
              child: Row(
                children: [
                  const VerticalDivider(),
                  SizedBox(
                    width: 250,
                    height: double.infinity,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: List.generate(friendsId.length, (index) {
                        Person? friend = Person.getPersonById(friendsId[index]);
                        if (friend == null) {
                          return TextButton(
                              onPressed: () {},
                              child: const Text("Пользователь удален"));
                        }
                        return TextButton(
                            style: ButtonStyle(
                              backgroundColor: (currentIndex == index)
                                  ? MaterialStateColor.resolveWith((states) =>
                                      const Color.fromARGB(255, 181, 208, 181))
                                  : null,
                            ),
                            onPressed: () {
                              setState(() {
                                currentIndex = index;
                              });
                            },
                            child: Text(friend.nickname));
                      }),
                    ),
                  ),
                  const VerticalDivider(),
                  if (currentIndex != -1)
                    Expanded(
                        child: Padding(
                      padding: const EdgeInsets.all(15),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(Person.getPersonById(friendsId[currentIndex])!
                              .nickname),
                          const Divider(),
                          Expanded(
                              child: Container(
                            color: const Color.fromARGB(255, 23, 139, 106),
                            child: ListView(
                              children: List.generate(messages.length, (index) {
                                Message message = messages[index];
                                return Row(
                                  mainAxisAlignment: (message.chatId
                                              .indexOf(message.senderId) ==
                                          0)
                                      ? MainAxisAlignment.start
                                      : MainAxisAlignment.end,
                                  children: [
                                    Card(
                                      color: (message.chatId
                                                  .indexOf(message.senderId) ==
                                              0)
                                          ? const Color.fromARGB(
                                              255, 132, 172, 203)
                                          : const Color.fromARGB(
                                              255, 157, 206, 42),
                                      child: SizedBox(
                                        width:
                                            MediaQuery.of(context).size.width *
                                                .3,
                                        child: Padding(
                                          padding: const EdgeInsets.all(5),
                                          child: Text(message.text),
                                        ),
                                      ),
                                    )
                                  ],
                                );
                              }),
                            ),
                          )),
                          Row(
                            children: [
                              const Expanded(
                                child: TextField(),
                              ),
                              TextButton.icon(
                                onPressed: () {},
                                label: const Text("Отправить"),
                                icon: const Icon(Icons.send),
                              )
                            ],
                          )
                        ],
                      ),
                    )),
                ],
              )));
    });
  }
}
