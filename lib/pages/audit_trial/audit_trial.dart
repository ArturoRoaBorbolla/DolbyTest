import 'dart:io';

import 'package:testdolby/service/json_service.dart';
import 'package:testdolby/widgets/card_with_title.dart';
import 'package:testdolby/pages/audit_trial/widgets/log_messages.dart';
import 'package:testdolby/widgets/custom_text.dart';
import 'package:testdolby/widgets/section_title.dart';
import 'package:flutter/material.dart';

class AuditTrialPage extends StatefulWidget {
  const AuditTrialPage({super.key});

  @override
  State<AuditTrialPage> createState() => _AuditTrialPageState();
}

class _AuditTrialPageState extends State<AuditTrialPage> {
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

  @override
  void initState() {
    readJson((AuditTrialPage).toString().replaceAll("Page", "").toLowerCase());
  }

  @override
  Widget build(BuildContext context) {
    return header.isEmpty && subheaders.isEmpty
        ? Container()
        : SingleChildScrollView(
            child: Center(
                child: Column(children: [
              SectionTitle(
                customText: CustomText(
                  text: header,
                  size: 24,
                  weight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              CardOptions(textSection: subheaders[0], widget: LogMessages()),
            ])),
          );
  }
}
