import 'dart:io';

import 'package:testdolby/constants/styles.dart';
import 'package:testdolby/pages/data_management/widgets/card.dart';
import 'package:testdolby/service/json_service.dart';
import 'package:testdolby/widgets/custom_text.dart';
import 'package:testdolby/widgets/section_title.dart';
import 'package:flutter/material.dart';
import 'package:localstorage/localstorage.dart';

class DataManagementPage extends StatefulWidget {
  const DataManagementPage({super.key});

  @override
  State<DataManagementPage> createState() => _DataManagementPageState();
}

class _DataManagementPageState extends State<DataManagementPage> {
  final LocalStorage storage = LocalStorage('login');
  JsonService jsonService = JsonService();
  Directory currentDir = Directory.current;
  String header = "";
  List<String> subheaders = [];

  Future readJson(String className) async {
    List jsonResponse = [];
    jsonResponse = await jsonService
        .readJson('${currentDir.path}/assets/json/headers.json');
    for (Map<String, dynamic> section in jsonResponse) {
      section.forEach((key, value) {
        if (key == className) {
          setState(() {
            header = value[0]['header'];
            for (int i = 0; i < value[1]['subheaders'].length; i++) {
              subheaders.add(value[1]['subheaders'][i]['subheader${i + 1}']);
            }
          });
        }
      });
    }
  }

  Widget userOptions() {
    int userType = storage.getItem('type_user');
    if (userType == 3) {
      return header.isEmpty && subheaders.isEmpty
          ? Container()
          : Center(
              child: Column(children: [
              SectionTitle(
                customText: CustomText(
                  text: header,
                  size: 24,
                  weight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              Column(children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Expanded(
                        child: CardOptions(
                            textSection: subheaders[0], textCard: "Update"))
                  ],
                ),
              ]),
            ]));
    } else {
      return header.isEmpty && subheaders.isEmpty
          ? Container()
          : Center(
              child: Column(children: [
              SectionTitle(
                customText: CustomText(
                  text: "Infrastructure",
                  size: 24,
                  weight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              Column(children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Expanded(
                        child: CardOptions(
                            textSection: subheaders[1], textCard: "Update")),
                    VerticalDivider(width: 1.0),
                    Expanded(
                      child: CardOptions(
                        textSection: "Database",
                        textCard: "Access to my database",
                      ),
                    ),
                  ],
                ),
              ]),
            ]));
    }
  }

  @override
  void initState() {
    readJson(
        (DataManagementPage).toString().replaceAll("Page", "").toLowerCase());
  }

  @override
  Widget build(BuildContext context) {
    return userOptions();
  }
}
