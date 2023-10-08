import 'dart:io';

import 'package:testdolby/pages/json_table/json_table.dart';
import 'package:testdolby/pages/logs/logs.dart';
import 'package:testdolby/pages/view/view.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class LogMessages extends StatefulWidget {
  const LogMessages({super.key});

  @override
  State<LogMessages> createState() => _LogMessagesState();
}

class _LogMessagesState extends State<LogMessages> {
  Directory currentDir = Directory.current;

  List<String> testsNames = [
    "Test_1",
    "Test_2",
    "Test_3",
    "Test_4",
    "Test_5",
    "Test_6",
    "Test_7"
  ];

  List<DataCell> viewCells(String text){
    List<DataCell> cells = [];
    for(var test in testsNames){
      cells.add(DataCell(TextButton(child: Text(text), onPressed: (){
        Get.to(() => ViewPage(
          test: test,
        ));
        print(test);
      })));
    }
    return cells;
  }

  List<DataCell> logCells(String text){
    List<DataCell> cells = [];
    for(var test in testsNames){
      cells.add(DataCell(TextButton(child: Text(text), onPressed: (){
        Get.to(() => LogsPage(
          test: test,
        ));
      })));
    }
    return cells;
  }

  @override
  Widget build(BuildContext context) {   
    return JsonTable(
      path: '${currentDir.path}/assets/json/audit_trail.json',
      columns: [
        DataColumn(
          label: Text(
            'Test result',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 18),
          )
        ),
        DataColumn(
          label: Text(
            'Logs',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 18),
          )
        ),
      ],
      cells: [
        viewCells('View'),
        logCells('Logs')
      ]
      );
  }
}
