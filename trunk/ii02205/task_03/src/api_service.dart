import 'package:flutter/material.dart';

class Person {
  String id = "";
  String nickname = "";
  List<String> friendIds = [];
  Person(this.id, this.nickname, this.friendIds);

  static String getNicknameById(String id) {
    int index = DB.persons.indexWhere((element) {
      if (element.id == id) return true;
      return false;
    });

    if (index != -1) return DB.persons[index].nickname;
    return "";
  }

  static Person? getPersonById(String id) {
    int index = DB.persons.indexWhere((element) {
      if (element.id == id) return true;
      return false;
    });
    if (index == -1) return null;
    return DB.persons[index];
  }
}

class DB {
  static List<Person> persons = [
    Person("1", "Adryian4ik", ["2", "3", "4", "5", "6"]),
    Person("2", "SirnikSun", ["1", "3", "4", "5", "6"]),
    Person("3", "Psijik", ["2", "1", "4", "5", "6"]),
    Person("4", "Lumonces", ["2", "3", "1 ", "5", "6"]),
    Person("5", "Corowka", ["2", "3", "4", "1", "6"]),
    Person("6", "NeonchikCallMe", ["2", "3", "4", "1", "5"]),
  ];

  static List<Post> posts = [
    Post("1", "3", "Прекрасный день для новых открытий!"),
    Post("2", "2", "Сегодня был на удивительной прогулке по парку."),
    Post("3", "5", "Поделился рецептом вкуснейшего пирога с яблоками."),
    Post("4", "1", "Ура! Закончил очередной проект!"),
    Post("5", "4", "Погода за окном просто потрясающая!"),
    Post("6", "3", "Новая книга просто захватывает!"),
    Post("7", "2", "Провел весь день за чтением. Нет лучшего способа отдыха!"),
    Post("8", "5", "Поделился впечатлениями от последнего фильма."),
    Post("9", "1",
        "Завершил курс по машинному обучению. Впечатления зашкаливают!"),
    Post("10", "4", "Сегодняшний рассвет просто восхитителен!"),
    Post("11", "3", "Отличный результат на тестировании!"),
    Post("12", "2", "Новая музыкальная композиция завораживает!"),
    Post("13", "5", "Сборка новой мебели - это искусство!"),
    Post("14", "1", "Прекрасный вечер для прогулки под звездами."),
    Post("15", "4", "Получил приглашение на конференцию по инновациям."),
    Post("16", "3",
        "Сегодняшний тренировочный день оказался самым продуктивным!"),
    Post("17", "2",
        "Обнаружил интересный баг в программе. Время его исправить!"),
    Post("18", "5", "Новый рецепт супа покорил всех в семье!"),
    Post("19", "1", "Завершил чтение увлекательной книги."),
    Post("20", "4", "Провел день за изучением новых технологий."),
    Post("21", "3", "Отличный выходной день в кругу семьи!"),
    Post("22", "2", "Получил новый заказ на разработку сайта."),
    Post("23", "5", "Погода сегодня идеальная для пикника!"),
    Post("24", "1", "Сделал интересное открытие в своем исследовании."),
    Post("25", "4", "Начал изучение нового иностранного языка."),
    Post("26", "3", "Новый фильм просто поразил своим сюжетом!"),
    Post("27", "2", "Удачная покупка - новый фотоаппарат!"),
    Post("28", "5", "Провел день за пазлами. Умственная гимнастика важна!"),
    Post("29", "1",
        "Получил похвалу от начальства за хорошо выполненную работу."),
    Post("30", "4", "Сегодняшний закат просто невероятен!"),
    Post("31", "3", "Завершил проект и горжусь результатом!"),
    Post("32", "2", "Посетил выставку современного искусства."),
    Post("33", "5", "Открыл для себя новый вид спорта - бадминтон."),
    Post("34", "1",
        "Новая кулинарная рецепт-книга вдохновила меня на эксперименты!"),
    Post("35", "4", "Прочитал интересную статью о космосе."),
    Post("36", "3",
        "Получил новое резюме от потенциального кандидата на работу."),
    Post("37", "2", "Сделал красивые фотографии во время прогулки по городу."),
    Post("38", "5", "Сегодняшний день был полон приключений!"),
    Post("39", "1", "Новая коллекция книг в библиотеке просто потрясающая!"),
    Post("40", "4", "Посетил лекцию по истории искусства."),
    Post("41", "3", "Сегодняшний день был насыщен событиями."),
    Post("42", "2", "Начал новый проект в области программирования."),
    Post("43", "5", "Провел день за занятиями йогой. Очень расслабляет."),
    Post("44", "1", "Получил новую идею для будущего стартапа."),
    Post("45", "4", "Побывал на выставке ретро автомобилей."),
    Post("46", "3", "Отлично провел время на вечеринке с друзьями."),
    Post("47", "2", "Получил комплименты за свой новый наряд."),
    Post("48", "5", "Сегодняшний рассвет просто волшебный!"),
    Post("49", "1", "Новый рецепт салата - моя находка недели!"),
    Post("50", "6", "Провела вечер за просмотром любимого сериала."),
    Post("51", "6", "Сегодняшний рассвет вдохновил меня на новые идеи."),
    Post(
        "52", "6", "Закончила книгу, которую начала читать на прошлой неделе."),
    Post(
        "53", "6", "Новый трек моего любимого исполнителя просто потрясающий!"),
    Post("54", "6",
        "Открыла для себя новый ресторан с вегетарианской кухней. Впечатления невероятные!"),
  ];

  static List<Message> messages = [
    // Message(["1", ""], "", ""),
    Message(["1", "2"], "Привет! Как дела?", "1", DateTime.now()),
    Message(["1", "2"], "Привет! Всё хорошо, спасибо. А у тебя?", "2",
        DateTime.now().add(const Duration(minutes: 1))),
    Message(["1", "2"], "Тоже неплохо, спасибо. Как прошла твоя неделя?", "1",
        DateTime.now().add(const Duration(minutes: 2))),
    Message(["1", "2"], "Довольно насыщенно, много работы, но в целом хорошо.",
        "2", DateTime.now().add(const Duration(minutes: 3))),
    Message(
        ["1", "2"],
        "Понимаю. У меня тоже была занятая неделя. Какие планы на выходные?",
        "1",
        DateTime.now().add(const Duration(minutes: 4))),
    Message([
      "1",
      "2"
    ], "Планирую отдохнуть дома, почитать книгу и посмотреть новый фильм. А у тебя?",
        "2", DateTime.now().add(const Duration(minutes: 5))),
    Message([
      "1",
      "2"
    ], "Тоже не собираюсь много бегать, скорее всего останусь дома и посижу за рисунками. Хорошего отдыха!",
        "1", DateTime.now().add(const Duration(minutes: 6))),
    Message(["1", "2"], "Спасибо, тебе тоже! Будем держать связь. До встречи!",
        "2", DateTime.now().add(const Duration(minutes: 7))),
    Message(["1", "2"], "До встречи!", "1",
        DateTime.now().add(const Duration(minutes: 8))),

    Message(["1", "3"], "Привет! Как прошел день?", "1", DateTime.now()),
    Message(["1", "3"], "Привет! Всё отлично, спасибо. А у тебя?", "3",
        DateTime.now().add(const Duration(minutes: 1))),
    Message(["1", "3"], "У меня тоже всё хорошо. Чем занимался сегодня?", "1",
        DateTime.now().add(const Duration(minutes: 2))),
    Message(
        ["1", "3"],
        "Сегодня был на работе, а потом провел время с друзьями.",
        "3",
        DateTime.now().add(const Duration(minutes: 3))),
    Message(["1", "3"], "Звучит здорово. Что делал с друзьями?", "1",
        DateTime.now().add(const Duration(minutes: 4))),
    Message(["1", "3"], "Мы поиграли в футбол и пошли в кафе. Было весело.",
        "3", DateTime.now().add(const Duration(minutes: 5))),
    Message([
      "1",
      "3"
    ], "Поиграть в футбол звучит как отличная идея. Может, в следующий раз присоединюсь?",
        "1", DateTime.now().add(const Duration(minutes: 6))),
    Message(
        ["1", "3"],
        "Конечно, буду рад. Дай знать заранее, и мы устроим игру.",
        "3",
        DateTime.now().add(const Duration(minutes: 7))),
    Message(
        ["1", "3"],
        "Отлично, обязательно так и сделаю. Спасибо! До свидания.",
        "1",
        DateTime.now().add(const Duration(minutes: 8))),
    Message(["1", "3"], "Пожалуйста! До свидания!", "3",
        DateTime.now().add(const Duration(minutes: 9)))
  ];
}

class SideRoute {
  IconData icon = Icons.hourglass_empty;
  String label = "";
  String route = "";
  SideRoute(this.icon, this.label, this.route);
}

class Post {
  String userId = "";
  String label = "";
  String id = "";
  Post(this.id, this.userId, this.label);
}

List<SideRoute> sideRoutes = [
  SideRoute(Icons.home, "Домашняя страница", "/"),
  SideRoute(Icons.message, "Сообщения", "/messages"),
  SideRoute(Icons.person, "Друзья", "/friends"),
  SideRoute(Icons.logout, "Выход", "/logout"),
];

class Message {
  List<String> chatId = [];
  String text = "";
  String senderId = "";
  DateTime date = DateTime(2024);
  Message(this.chatId, this.text, this.senderId, this.date);

  static List<Message> getMessages(String id, String id2) {
    List<Message> result = DB.messages;
    result = result.where((e) {
      return (e.chatId.contains(id) && e.chatId.contains(id2));
    }).toList();
    return result;
  }
}
