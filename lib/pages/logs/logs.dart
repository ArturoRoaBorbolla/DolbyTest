import 'dart:io';

import 'package:data_table_2/data_table_2.dart';
import 'package:testdolby/constants/styles.dart';
import 'package:testdolby/widgets/alert.dart';
import 'package:testdolby/widgets/card_with_title.dart';
import 'package:testdolby/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';

class LogsPage extends StatefulWidget {
  final String test;
  const LogsPage({super.key, required this.test});

  @override
  State<LogsPage> createState() => _LogsPageState();
}

class _LogsPageState extends State<LogsPage> {
  List _logs = [];
  String contents = "";
  String currentDir = Directory.current.path.replaceAll("'", "");

  final List _test = [
    {"id": "Test_1", "result": "OR_1_1_2"},
    {"id": "Test_2", "result": "OR_2_1"},
    {"id": "Test_3", "result": "OR_3_2"},
    {"id": "Test_4", "result": "OR_4_1_3"},
    {"id": "Test_5", "result": "OR_5_1"},
    {"id": "Test_6", "result": "OR_6_2"},
    {"id": "Test_7", "result": "OR_7_2"}
  ];

  Future<void> readTxt() async {
    final Directory? directory = await getDownloadsDirectory();
    print(directory);
    // final File file = File('C:\\Users\\C\\Work\\NDolby\\scripts\\${widget.test}\\Logs\\${widget.test}.log');

    final File file = File('${currentDir}\\scripts\\${widget.test}\\Logs\\${widget.test}.log');
    contents = await file.readAsString();
    setState(() {
      _logs = contents.split('\n');
    });
  }

  _write(BuildContext context) async {
    final Directory? directory = await getDownloadsDirectory();
    print(directory);
    final File file = File('${directory?.path}\\${widget.test}.log');
    print(file);
    await file.writeAsString(contents);
    _alert(context, 'File download successfully', 'You can visualize the document in your local downloads folder');
  }

  _alert(context, title, content) {
    Alert.noticeAlert(context, title, content);
  }

  @override
  void initState() {
    super.initState();
    readTxt();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          backgroundColor: brown,
          title: CustomText(
            text: "Logs",
            size: 24,
            weight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        body: Column(
          children: [
            CardOptions(
                textSection: "${widget.test}",
                widget: Column(
                  children: [
                    SizedBox(
                        height: MediaQuery.of(context).size.height - 220,
                        width: 1200,
                        child: Container(
                          padding: const EdgeInsets.all(20),
                          margin: const EdgeInsets.only(bottom: 20),
                          child: DataTable2(
                              columnSpacing: 12,
                              horizontalMargin: 12,
                              minWidth: 600,
                              columns: const [
                                DataColumn2(
                                    label: Text(
                                      'Logged messages',
                                      style: TextStyle(
                                          fontWeight: FontWeight.bold),
                                    ),
                                    size: ColumnSize.S),
                              ],
                              rows: List<DataRow>.generate(
                                  _logs.length,
                                  (index) => DataRow(cells: [
                                        DataCell(CustomText(text: _logs[index]))
                                      ]))),
                        )),
                    ElevatedButton(
                        onPressed: () {
                          _write(context);
                        }, child: Text('Download Result')),
                  ],
                )),
          ],
        ));
  }
}
