import 'dart:io';

import 'package:testdolby/service/json_service.dart';
import 'package:flutter/material.dart';
import 'package:data_table_2/data_table_2.dart';

class JsonTableAnalytics extends StatefulWidget {
  final String? path;
  final List<DataColumn>? columns;
  final List? cells;
  final Future<List>? jsonList;
  const JsonTableAnalytics(
      {super.key, this.path, this.columns, this.cells, this.jsonList});

  @override
  State<JsonTableAnalytics> createState() => _JsonTableAnalyticsState();
}

class _JsonTableAnalyticsState extends State<JsonTableAnalytics> {
  List jsonResponse = [];
  JsonService jsonService = JsonService();
  List<dynamic> columnNames = [];
  List<dynamic> rowData = [];
  List<DataColumn> columns = [];
  List<DataRow> rows = [];

  ScrollController controller = ScrollController();

  Future<void> readJson() async {
    jsonResponse = await jsonService.readJson(widget.path!);
    jsonResponse[0].forEach((key, value) {
      columnNames.add(key);
    });
    for (var item in jsonResponse) {
      List<dynamic> row = [];
      for (var column in columnNames) {
        row.add(item[column]);
      }
      rowData.add(row);
      row = [];
    }
    setState(() {
      columns = buildColumns();
      rows = buildRows();
    });
  }

  Future<void> readList() async {
    jsonResponse = await widget.jsonList!;
    jsonResponse[0].forEach((key, value) {
      columnNames.add(key);
    });
    for (var item in jsonResponse) {
      List<dynamic> row = [];
      for (var column in columnNames) {
        row.add(item[column]);
      }
      rowData.add(row);
      row = [];
    }
    setState(() {
      columns = buildColumns();
      rows = buildRows();
    });
  }

  List<DataColumn> buildColumns() {
    List<DataColumn> columns = [];
    for (var item in columnNames) {
      columns.add(DataColumn(
          label: Text(
        capitalize(item.replaceAll(RegExp('[^A-Za-z0-9]'), ' ')),
        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
      )));
    }
    if (widget.columns != null) {
      for (var column in widget.columns!) {
        columns.add(column);
      }
    }
    return columns;
  }

  List<DataRow> buildRows() {
    List<DataRow> rows = [];
    List tempCell = [];
    List<DataCell> cells = [];
    for (var row in rowData) {
      for (var item in row) {
        cells.add(DataCell(Text(item)));
      }
      tempCell.add(cells);
      cells = [];
    }
    if (widget.cells != null) {
      for (var widgetC in widget.cells!) {
        for (int i = 0; i < widgetC.length; i++) {
          (tempCell[i].add(widgetC[i]));
        }
      }
    }
    for (var cells in tempCell) {
      rows.add(DataRow(cells: cells));
    }
    return rows;
  }

  String capitalize(String string) {
    return "${string[0].toUpperCase()}${string.substring(1).toLowerCase()}";
  }

  @override
  void initState() {
    super.initState();
    if (widget.jsonList == null) {
      readJson();
    } else {
      readList();
    }
  }

  Widget table() {
    return columns.isNotEmpty
        ? DataTable2(
            columnSpacing: 12,
            horizontalMargin: 12,
            dataRowHeight: 200,
            minWidth: 600,
            columns: columns,
            rows: rows,
          )
        : Center(
            child: CircularProgressIndicator(strokeWidth: 3),
          );
    ;
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
        height: MediaQuery.of(context).size.height - 220,
        width: 1200,
        child: Container(
            padding: const EdgeInsets.all(20),
            margin: const EdgeInsets.only(bottom: 30),
            child: table()));
  }
}
