import 'package:testdolby/constants/styles.dart';
import 'package:testdolby/service/sqlite_service.dart';
import 'package:testdolby/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:testdolby/widgets/card_with_title.dart';
class SeeTable extends StatefulWidget {
  final String table;
  
  const SeeTable({super.key, required this.table});

  @override
  State<SeeTable> createState() => _SeeTableState();
}

class _SeeTableState extends State<SeeTable> {
  final SqliteService _sqliteService = SqliteService();

  final _verticalScrollController = ScrollController();
  final _horizontalScrollController = ScrollController();
  
  List<String> columns = [];
  List<Map> rows = [];
  List<DataColumn> dataCell = [];
  List<DataRow> dataRow = [];
  List<DataCell> cells = [];
  
  late bool isLoading;
  setLoading(bool state) => setState(() => isLoading = state);

  late DataTableSource _data;

  @override
  void initState() {
    super.initState();
    column(widget.table);
    setLoading(true);
  }

  Future<void> column(String table) async {
    columns = await _sqliteService.getAllColumnNames(table); 
    setState(() {
      for (int i=0; i<columns.length;i++){
        dataCell.add(DataColumn(label: Text(columns[i], style: TextStyle(fontWeight: FontWeight.bold))));
      }
      infoTable(widget.table);
    });
  }

  Future<void> infoTable(String table) async {
    rows = await _sqliteService.getRowsTable(table); 
    setState(() {
      for (int i=0; i<rows.length;i++){
        for (int j=0; j<columns.length;j++){
          cells.add(DataCell(Text(rows[i][columns[j]].toString()))); 
        }
        dataRow.add(DataRow(cells: cells));
        cells = [];
      }
      _data = MyData(dataRow, rows.length);
      setLoading(false);
    });
  }
  

  @override
  Widget build(BuildContext context) {
    if(isLoading) return Container(color: Colors.white, child: Transform.scale(
        scale: 3,
        child: Center(
          child: CircularProgressIndicator(strokeWidth: 3),
        ),
      )
    );

    return Scaffold(
      appBar: AppBar(
        backgroundColor: brown,
        title: CustomText(
          text: widget.table,
          size: 24,
          weight: FontWeight.bold,
          color: Colors.white,
      )),
      body: SingleChildScrollView(
    child: Container(
        padding: EdgeInsets.only(
          left: 60, 
          right: 60,
        ),
        child: Column(
          children: [
            CardOptions(
              textSection: widget.table, 
              widget: PaginatedDataTable(
                controller: _verticalScrollController,
                source: _data,
                columns: dataCell,
                columnSpacing: 100,
                horizontalMargin: 10,
                rowsPerPage: 10,
                showCheckboxColumn: false,
              ),
            ),
          ],
        ),
      )
    ),
    );
  }
}

class MyData extends DataTableSource {
  late List<DataRow> dataRow;
  late int rows;

  MyData(this.dataRow, this.rows);
    
  @override
  bool get isRowCountApproximate => false;
  @override
  int get rowCount => rows;
  @override
  int get selectedRowCount => 0;
  @override
  DataRow getRow(int index) {
    return dataRow[index];
  }
}