import 'dart:convert';
import 'dart:io';

import 'package:testdolby/pages/json_table/json_table.dart';
import 'package:flutter/material.dart';
import 'package:testdolby/widgets/custom_text.dart';
import 'package:testdolby/pages/tresholds/model/treshold.dart';
import 'package:testdolby/pages/tresholds/model/test.dart';
import 'package:testdolby/pages/tresholds/widgets/text_dialog_widget.dart';
import 'package:get/get.dart';

class TableTreshold extends StatefulWidget {
  const TableTreshold({super.key});

  @override
  State<TableTreshold> createState() => _Tabletresholdstate();
}

class _Tabletresholdstate extends State<TableTreshold> {
  Directory currentDir = Directory.current;
  late List _tests = [];
  List<Widget> datatables = [];
  Future<List>? jsonList;
  bool reload = false;

  Future<void> readJson() async {
    List<Test> testList = [];
    final File file = File('${currentDir.path}/assets/json/thresholds.json');
    String contents = await file.readAsString();
    Map<String, dynamic> jsonResponse = jsonDecode(contents);
    setState(() {
      jsonResponse.forEach((key, value) {
        value.forEach((key, value) {
          Test test = Test(key, value.toString());
          testList.add(test);
        });
        Tresholds tresholds = Tresholds(key, testList);
        _tests.add(tresholds);
        testList = [];
      });
      jsonList = listToSend(_tests);
    });
  }

  Future updateJson(String name, String value) async {
    final File file = File('${currentDir.path}/assets/json/thresholds.json');
    for (var tests in _tests) {
      for (var test in tests.test) {
        if (name == test.name) {
          test.value = value;
        }
      }
    }
    var testsMap = _tests.map((e) {
      return '"${e.name}": ${{
        e.test
            .map((i) {
              String values = "";
              final regExp = RegExp(r'[a-zA-Z\^$*.\[\]{}()?\-"!@#%&/\,><:;_~`+='
                  "'" //
                  ']');
              if (!i.value.contains(regExp)) {
                values = '"${i.name}": ${i.value}';
              } else {
                values = '"${i.name}": "${i.value}"';
              }
              return values;
            })
            .toList()
            .join(", ")
      }}';
    }).toList();
    file.writeAsStringSync('{${testsMap.join(", ")}}');
    setState(() {
      _tests = [];
      jsonList = null;
      readJson();
      reload = !reload;
    });
  }

  Future editValue(String name, String value) async {
    final newValue = await showTextDialog(
      context,
      title: 'Change value',
      value: value,
    );
    updateJson(name, newValue);
  }

  Future<List> emptyList() async {
    return [];
  }

  Future<List> listToSend(List _tests) async {
    List<String> id = [];
    List<String> names = [];
    List list = [];

    for (var tests in _tests) {
      for (var test in tests.test) {
        id.add(tests.name);
        names.add(test.name);
        list.add({"Treshold": tests.name, "Place": test.name});
      }
    }
    return list;
  }

  List<DataCell> valueCells(String text) {
    List<String> names = [];
    List<String> values = [];
    for (var tests in _tests) {
      for (var test in tests.test) {
        names.add(test.name);
        values.add(test.value);
      }
    }
    List<DataCell> cells = [];
    for (int i = 0; i < values.length; i++) {
      cells.add(
          DataCell(CustomText(text: values[i]), showEditIcon: true, onTap: () {
        editValue(names[i], values[i]);
      }));
    }
    return cells;
  }

  @override
  void initState() {
    readJson();
  }

  @override
  Widget build(BuildContext context) {
    return jsonList == null
        ? Container()
        : JsonTable(
            key: ValueKey(reload),
            jsonList: jsonList,
            columns: [
              DataColumn(
                  label: Text(
                'Value',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
              ))
            ],
            cells: [valueCells('Value')],
          );
  }
}
