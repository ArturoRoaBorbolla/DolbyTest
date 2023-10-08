import 'package:testdolby/pages/see_users/see_users.dart';
import 'package:testdolby/widgets/alert.dart';
import 'package:testdolby/widgets/card_with_title.dart';
import 'package:testdolby/widgets/custom_text.dart';
import 'package:testdolby/widgets/section_title.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class UsersPage extends StatefulWidget {
  const UsersPage({super.key});

  @override
  State<UsersPage> createState() => _UsersPageState();
}

class _UsersPageState extends State<UsersPage> {
  final usernameController = TextEditingController();

  _alert(context, title, content) {
    Alert.noticeAlert(context, title, content);
  }

  @override
  void dispose() {
    usernameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
        child: Center(
            child: Column(
      children: [
        SectionTitle(
          customText: CustomText(
            text: "Users",
            size: 24,
            weight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        CardOptions(
          textSection: "Save, delete and update users",
          widget: SizedBox(
              width: MediaQuery.of(context).size.width * 0.2,
              child: Column(
                children: [
                  SizedBox(
                    width: MediaQuery.of(context).size.width * 0.2,
                    child: TextField(
                      controller: usernameController,
                      decoration: InputDecoration(
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(10.0),
                          ),
                          filled: true,
                          hintStyle: TextStyle(color: Colors.grey[500]),
                          hintText: "Username",
                          fillColor: Colors.white70),
                    ),
                  ),
                  SizedBox(
                    width: MediaQuery.of(context).size.width * 0.05,
                    height: MediaQuery.of(context).size.height * 0.03,
                  ),
                  ElevatedButton(
                    onPressed: () {
                      if (usernameController.text.isNotEmpty) {
                        Get.to(() => SeeUserPage(
                              username: usernameController.text,
                            ));
                      } else {
                        _alert(context, "Empty field",
                            "You must add the username you want to find");
                      }
                    },
                    child: Text('Search user'),
                    style: ElevatedButton.styleFrom(shape: StadiumBorder()),
                  ),
                ],
              )),
        ),
      ],
    )));
  }
}
