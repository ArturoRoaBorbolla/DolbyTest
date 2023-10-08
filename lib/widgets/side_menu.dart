import 'dart:io';

import 'package:testdolby/constants/controllers.dart';
import 'package:testdolby/constants/styles.dart';
import 'package:testdolby/helpers/responsiveness.dart';
import 'package:testdolby/pages/authentication/authentication.dart';
import 'package:testdolby/routing/routes.dart';
import 'package:testdolby/service/json_service.dart';
import 'package:testdolby/widgets/side_menu_item.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:localstorage/localstorage.dart';

class SideMenu extends StatefulWidget {
  const SideMenu({super.key});
  static ValueNotifier<String> testStatus =
      ValueNotifier("Test: None\nStatus: No test running");

  @override
  State<SideMenu> createState() => _SideMenuState();
}

class _SideMenuState extends State<SideMenu> {
  JsonService jsonService = JsonService();
  Directory currentDir = Directory.current;
  late var jsonResponse;
  final LocalStorage storage = LocalStorage('login');
  TextEditingController textController = TextEditingController();
  File photoPath = File('assets/AIVER_logo.png');

  @override
  void initState() {
    super.initState();
  }

  List<Widget> sideMenuPages(BuildContext context) {
    late List<Widget> menu;
    List<dynamic> menuString = sideMenuItemsUser;
    int userType = storage.getItem('type_user');
    if (userType == 1 || userType == 2) {
      menuString = sideMenuItemsSuperadmin;
    }
    menu = menuString
        .map((itemName) => SideMenuItem(
              itemName:
                  itemName == AuthenticationPageRoute ? "Log Out" : itemName,
              onTap: () {
                if (itemName == AuthenticationPageRoute) {
                  Get.offAll(() => AuthenticationPage());
                  storage.deleteItem('type_user');
                  storage.deleteItem('username');
                }

                if (!menuController.isActive(itemName)) {
                  menuController.changeActiveItemTo(itemName);
                  if (ResponsiveWidget.isSmallScreen(context)) Get.back();
                  navigationController.navigatoTo(itemName);
                }
              },
            ))
        .toList();
    return menu;
  }

  List<Widget> sideMenuOptions(BuildContext context) {
    List<Widget> menu = [];
    for (var option in sideMenuPages(context)) {
      menu.add(option);
    }
    menu.add(ValueListenableBuilder(
      valueListenable: SideMenu.testStatus,
      builder: (BuildContext context, String value, Widget? child) {
        textController.text = SideMenu.testStatus.value;
        return Container(
            margin: EdgeInsets.all(20),
            padding: EdgeInsets.all(10),
            color: Colors.white,
            child: TextField(
              controller: textController,
              keyboardType: TextInputType.multiline,
              minLines: 2,
              maxLines: 5,
              enabled: false,
              decoration: InputDecoration(
                border: InputBorder.none,
              ),
            ));
      },
    ));
    return menu;
  }

  @override
  Widget build(BuildContext context) {
    double _width = MediaQuery.of(context).size.width;
    return Container(
      color: navyBlue,
      child: Column(
        children: [
          Expanded(
            child: ListView(
              children: sideMenuOptions(context),
            ),
          ),
          Row(
            children: [
              SizedBox(width: _width / 48),
              Container(
                child: Image.file(
                  photoPath,
                  width: MediaQuery.of(context).size.width / 10,
                  height: 100,
                ),
              ),
              /*
              Container(
                child: Image.asset(
                  "assets/AIVER_logo.png",
                  width: MediaQuery.of(context).size.width / 8.68,
                  height: 100,
                ),
              ),*/
              SizedBox(
                width: _width / 48,
              )
            ],
          ),
        ],
      ),
    );
  }
}
