 import 'dart:io';

import 'package:testdolby/pages/dashboard/widgets/graphic_section.dart';
import 'package:testdolby/pages/dashboard/widgets/card.dart';
import 'package:testdolby/pages/dashboard/widgets/table_high_priority_tests.dart';
import 'package:testdolby/service/json_service.dart';
import 'package:testdolby/widgets/alert.dart';
import 'package:testdolby/widgets/custom_text.dart';
import 'package:testdolby/widgets/section_title.dart';

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:localstorage/localstorage.dart' as ls;

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});
  static ValueNotifier<bool> loading = ValueNotifier(true);
  @override
  State<DashboardPage> createState() => DashboardPageState();
}

class DashboardPageState extends State<DashboardPage> {
  bool loading = true;
  late bool isLoading;
  bool reload = false;
  final ls.LocalStorage storage = ls.LocalStorage('login');
  late Widget graphics;
  setLoading(bool state) => setState(() => isLoading = state);
  Directory currentDir = Directory.current;

  final TextEditingController _textController = TextEditingController();

  Directory current_dir = Directory.current;

  TextEditingController dateFrom = TextEditingController();
  TextEditingController dateTo = TextEditingController();
  String FromDate = "";
  String ToDate = "";
  String header = "";
  List<String> subheaders = [];

  _alert(BuildContext context, String title, String content) {
    Alert.noticeAlert(context, title, content);
  }

  _noticeAlertRefresh(BuildContext context, String title, String content) {
    refresh() {
      setState(() {
        reload = !reload;
      });
    }

    Alert.noticeAlertRefresh(context, title, content, refresh);
  }

  readJson(String path) async {
    JsonService jsonService = JsonService();
    List jsonResponse = [];
    jsonResponse = await jsonService.readJson(path);
    return jsonResponse;
  }

  Future<void> titles() async {
    List headersResponse =
        await readJson('${currentDir.path}/assets/json/headers.json');
    for (Map<String, dynamic> section in headersResponse) {
      section.forEach((key, value) {
        if (key ==
            (DashboardPage).toString().replaceAll("Page", "").toLowerCase()) {
          setState(() {
            for (int i = 0; i < value[1]['subheaders'].length; i++) {
              header = value[0]['header'];
              print(header);
              subheaders.add(value[1]['subheaders'][i]['subheader${i + 1}']);
            }
          });
        }
      });
    }
  }

  @override
  void initState() {
    super.initState();
    titles();
    if (ToDate == "" && FromDate == "") {
      setLoading(true);
    } else {
      setLoading(storage.getItem('is_loading'));
    }
  }

  @override
  Widget build(BuildContext context) {
    return header.isEmpty && subheaders.isEmpty
        ? Container()
        : ListView(children: [
            Column(children: [
              SectionTitle(
                customText: CustomText(
                  text: header,
                  size: 24,
                  weight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              CardOptions(
                  textSection: subheaders[0], widget: HighPriorityTests()),
              CardOptions(
                  textSection: subheaders[1],
                  widget: Container(
                      padding: EdgeInsets.only(
                          left: 60, right: 60, bottom: 20, top: 10),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment
                            .spaceEvenly, // use whichever suits your need
                        children: <Widget>[
                          Expanded(
                              child: TextField(
                                  controller: dateFrom,
                                  decoration: InputDecoration(
                                      icon: Icon(Icons.calendar_today),
                                      labelText: "Date from"),
                                  readOnly: true,
                                  onTap: () async {
                                    DateTime? pickedDate = await showDatePicker(
                                        context: context,
                                        initialDate: DateTime.now(),
                                        firstDate: DateTime(1950),
                                        lastDate: DateTime(2100));
                                    if (pickedDate != null) {
                                      //FromDate = DateFormat('yyyyMMdd')
                                      FromDate = DateFormat('yyyyMMdd')
                                          .format(pickedDate);
                                      setState(() {
                                        dateFrom.text = FromDate;
                                        if (storage.getItem('is_loading') ==
                                                false ||
                                            storage.getItem('is_loading') ==
                                                null) {
                                          if (ToDate != "" && FromDate != "") {
                                            setLoading(false);
                                          }
                                        }
                                      });
                                    }
                                  })),
                          SizedBox(
                            width: 100,
                          ),
                          Expanded(
                              child: TextField(
                                  controller: dateTo,
                                  decoration: InputDecoration(
                                      icon: Icon(Icons.calendar_today),
                                      labelText: "Date to"),
                                  readOnly: true,
                                  onTap: () async {
                                    DateTime? pickedDate = await showDatePicker(
                                        context: context,
                                        initialDate: DateTime.now(),
                                        firstDate: DateTime(1950),
                                        lastDate: DateTime(2100));
                                    if (pickedDate != null) {
                                      //ToDate = DateFormat('yyyyMMdd')
                                      ToDate = DateFormat('yyyyMMdd')
                                          .format(pickedDate);
                                      setState(() {
                                        dateTo.text = ToDate;
                                        if (storage.getItem('is_loading') ==
                                                false ||
                                            storage.getItem('is_loading') ==
                                                null) {
                                          if (ToDate != "" && FromDate != "") {
                                            setLoading(false);
                                          }
                                        }
                                      });
                                    }
                                  })),
                          SizedBox(
                            width: 100,
                          ),
                          ElevatedButton(
                              child: Text('Update'),
                              onPressed: isLoading
                                  ? null
                                  : () async {
                                      setLoading(true);
                                      storage.setItem('is_loading', true);
                                      String pyscript;
                                      Directory current_dir = Directory.current;
                                      _alert(context, 'Updating',
                                          'To Update the graphics will take a time. A message will appear when we finish to update them.');
                                      for (int i = 1; i <= 7; i++) {
                                        if (i < 7 ){
                                          pyscript =
                                              "${current_dir.path}\\scripts\\Test_" +
                                                  i.toString() + "\\Test_" + i.toString() +
                                                  ".py";
                                        } else {
                                          pyscript =
                                              "${current_dir.path}\\scripts\\Test_" +
                                                  i.toString() + "\\Test_" + i.toString() +
                                                  ".py ";
                                        }
                                        print(pyscript);
                                        await Process.run('python', [
                                          pyscript,
                                          FromDate,
                                          ToDate
                                        ]).then((ProcessResult rs) {
                                          print(rs.stdout +
                                              rs.toString() +
                                              rs.stderr);
                                          exitCode = rs.exitCode;
                                        });
                                      }
                                      setLoading(false);
                                      storage.deleteItem('is_loading');
                                      _noticeAlertRefresh(context, 'Refreshing',
                                          'Graphics refreshing');
                                    }),
                        ],
                      ))),
              GraphicSection(
                  key: ValueKey(reload),
                  subheaders:
                      subheaders.getRange(2, subheaders.length).toList())
            ]),
          ]);
  }
}
