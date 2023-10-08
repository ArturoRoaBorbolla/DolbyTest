import 'dart:convert';
import 'dart:io';

import 'package:testdolby/pages/analytics/models/test.dart';
import 'package:testdolby/pages/audit_trial/model/log.dart';
import 'package:testdolby/pages/dashboard/models/PriorityTest.dart';
import 'package:testdolby/pages/json_table/json_table_analytics.dart';
import 'package:testdolby/pages/view/view.dart';
import 'package:testdolby/service/json_service.dart';
import 'package:testdolby/widgets/side_menu.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import 'package:localstorage/localstorage.dart';

class TestRoster extends StatefulWidget {
  const TestRoster({super.key});

  @override
  State<TestRoster> createState() => _TestRosterState();
}

class _TestRosterState extends State<TestRoster> {
  Directory currentDir = Directory.current;

  late bool isLoading;
  final LocalStorage storage = LocalStorage('login');

  setLoading(bool state) => setState(() => isLoading = state);

  List<DataCell> cellsView = [];
  List<DataCell> cellsLog = [];
  List _tests = [];
  List _logs = [];
  List view = [];
  List _priorityTests = [];
  List run = [];
  JsonService jsonService = JsonService();

  Future<void> readJsonTestRoster() async {
    List jsonResponse = [];
    jsonResponse = await jsonService
        .readJson('${currentDir.path}/assets/json/test_roster.json');
    for (var t in jsonResponse) {
      Test test =
          Test(t['id'], t['name'], t['last_run_date'], t['description']);
      _tests.add(test);
    }
  }

  Future<void> readJsonButtons() async {
    List jsonResponse = [];
    jsonResponse = await jsonService
        .readJson('${currentDir.path}/assets/json/buttons.json');
    for (var button in jsonResponse) {
      run = button['analytics'][0]['run'];
      view = button['analytics'][1]['view'];
    }
  }

  Future<void> readJsonLogMessages() async {
    List jsonResponse = [];
    jsonResponse = await jsonService
        .readJson('${currentDir.path}/assets/json/audit_trail.json');
    if (_logs.length == jsonResponse.length) {
      _logs = [];
    }
    for (var l in jsonResponse) {
      Log log = Log(l['user_id'], l['time'], l['test_id'], l['event_details'],
          l['event_details']);
      _logs.add(log);
    }
  }

  Future<void> readJsonHighPriorityTests() async {
    List jsonResponse = [];
    jsonResponse = await jsonService
        .readJson('${currentDir.path}/assets/json/high_priority_tests.json');
    for (var t in jsonResponse) {
      PriorityTest test = PriorityTest(t['id'], t['name'], t['status']);
      _priorityTests.add(test);
    }
  }

  Future updateJsonTestRoster(Test execTest) async {
    _tests.map((test) {
      if (test.id == execTest.id) {
        test.lastRunDate = execTest.lastRunDate;
      }
    }).toList();
    jsonService.updateJson(
        '${currentDir.path}/assets/json/test_roster.json', _tests);
    setState(() {
      _tests = [];
      readJsonTestRoster();
    });
  }

  Future updateJsonLogMessages(Log execLog) async {
    _logs.map((log) {
      if (execLog.testId == log.testId) {
        log.userId = storage.getItem('username');
        log.time = execLog.time;
        log.status = execLog.status;
        log.eventDetails = execLog.eventDetails;
      }
    }).toList();
    SideMenu.testStatus.value =
        "Test: ${execLog.testId}\nStatus: ${execLog.status}";
    jsonService.updateJson(
        '${currentDir.path}/assets/json/audit_trail.json', _logs);
  }

  Future updateJsonHighPriorityTests(PriorityTest execTest) async {
    for (int i = 0; i < _priorityTests.length; i++) {
      if (_priorityTests[i].id == execTest.id) {
        _priorityTests.removeAt(i);
      }
    }
    _priorityTests.add(execTest);
    jsonService.updateJson(
        '${currentDir.path}/assets/json/high_priority_tests.json',
        _priorityTests);
  }
  // List<DataCell> viewCells() {
  //   List<DataCell> cells = [];
  //   for (int i = 0; i < 5; i++) {
  //     cells.add(DataCell(TextButton(
  //         child: Text(capitalize(view[i]['text'])),
  //         onPressed: () {
  //           Get.to(() => ViewPage(
  //             test: view[i]['test'],
  //           ));
  //         })));
  //   }
  //   return cells;
  // }

  // List<DataCell> logCells() {
  //   List<DataCell> cells = [];
  //   for (int i = 0; i < 5; i++) {
  //     cells.add(DataCell(TextButton(
  //         child: Text(capitalize(run[i]['text'])),
  //         onPressed: isLoading
  //             ? null
  //             : () {
  //           runAction(run[i]['script'], run[i]['test']);
  //         })));
  //   }
  //   return cells;
  // }

  List<DataCell> viewCells() {
    List<DataCell> cells = [];
    for (int i = 0; i < view.length; i++) {
      print(view[i]['text']);
      cells.add(DataCell(TextButton(
          child: Text(capitalize(view[i]['text'])),
          onPressed: () {
            Get.to(() => ViewPage(
              test: view[i]['test'],
            ));
          })));
    }
    return cells;
  }

  List<DataCell> logCells() {
    List<DataCell> cells = [];
    for (int i = 0; i < view.length; i++) {
      print("Inside run");
      print(run[i]['text']);
      print(isLoading.toString());
      cells.add(DataCell(TextButton(
          child: Text(capitalize(run[i]['text'])),
          onPressed: isLoading
              ? null
              : () {
            print(run[i]['script']);
            print(run[i]['test']);
            runAction(run[i]['script'], run[i]['test']);
          })));
    }
    return cells;
  }



  Future<int> runScript(
      String script, String test, String formattedDate) async {
    late int exitCode;
    late Test runningTest;
    String pyscript = "${currentDir.path}\\scripts\\$test\\$script";
    print("Trying to run");
    print(pyscript);
    runningTest = _tests.where((e) => e.id == test).first;

    await Process.run('python', [pyscript]).then((ProcessResult rs) {
      exitCode = rs.exitCode;
      storage.deleteItem('is_loading');
      String user = storage.getItem('username');
      if (rs.exitCode == 0) {
        updateJsonLogMessages(Log(
            user, formattedDate, runningTest.id, "Succeed", "Test completed"));
        updateJsonHighPriorityTests(
            PriorityTest(runningTest.id, runningTest.name, "Succeed"));
      }
      if (rs.exitCode == -1) {
        updateJsonLogMessages(Log(
            user, formattedDate, runningTest.id, "Failed", "Failed script"));
        updateJsonHighPriorityTests(
            PriorityTest(runningTest.id, runningTest.name, "Failed"));
      }
      if (rs.exitCode == -2) {
        updateJsonLogMessages(Log(
            user, formattedDate, runningTest.id, "Failed", "Display failure"));
        updateJsonHighPriorityTests(
            PriorityTest(runningTest.id, runningTest.name, "Failed"));
      }
      updateJsonTestRoster(Test(runningTest.id, runningTest.name, formattedDate,
          runningTest.description));
    });
    return exitCode;
  }



  Future<void> runAction(String script, String test) async {
    setLoading(true);
    storage.setItem('is_loading', true);
    final DateTime date = DateTime.now();
    final String formattedDay = DateFormat.yMd().format(date);
    final String formattedHour = DateFormat.Hm().format(date);
    String formattedDate = "$formattedDay $formattedHour";

    updateJsonLogMessages(
        Log("JJ Cracaft", formattedDate, test, "Processing", "Task running"));
    await runScript(script, test, formattedDate);
    setLoading(false);
  }

  String capitalize(String string) {
    return "${string[0].toUpperCase()}${string.substring(1).toLowerCase()}";
  }

  @override
  void initState() {
    super.initState();
    readJsonTestRoster();
    readJsonLogMessages();
    readJsonHighPriorityTests();
    readJsonButtons();
    if (storage.getItem('is_loading') == null) {
      setLoading(false);
    } else {
      setLoading(storage.getItem('is_loading'));
    }
  }

  Future<void> getData() {
    return Future.delayed(Duration(seconds: 1), () {
      cellsView = viewCells();
      cellsLog = logCells();



      return [cellsView, cellsLog];
    });
  }


  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      builder: (ctx, snapshot) {
        if (snapshot.connectionState == ConnectionState.done) {
          if (snapshot.hasError) {
            return Center(
              child: Text(
                '${snapshot.error} occurred',
                style: TextStyle(fontSize: 18),
              ),
            );
          } else if (snapshot.hasData) {
            return JsonTableAnalytics(
                key: ValueKey(isLoading),
                path: '${currentDir.path}\\assets\\json\\test_roster.json',
                columns: [
                  DataColumn(
                      label: Text(
                    'Test result',
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                  )),
                  DataColumn(
                      label: Text(
                    'Run test',
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                  )),
                ],
                cells: [
                  cellsView,
                  cellsLog
                ]);
          }
        }
        return Center(
          child: CircularProgressIndicator(strokeWidth: 3),
        );
      },
      future: getData(),
    );
  }
}
