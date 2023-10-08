import 'package:flutter/material.dart';

import 'package:testdolby/service/sqlite_service.dart';
import 'package:testdolby/pages/see_tables/widgets/table.dart';
import 'package:testdolby/widgets/card_with_title.dart';

class Tables extends StatefulWidget {
  const Tables({super.key});

  @override
  State<Tables> createState() => _TablesState();
}

class _TablesState extends State<Tables> {
  final SqliteService _sqliteService = SqliteService();
  List<String> tables = [];

  Future<void> table() async {
    tables = await _sqliteService.getAllTableNames();
    setState(()=> tables);
  }
  
  @override
  void initState() {
    super.initState();
    table();
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Container(
        padding: EdgeInsets.only(left: 140, right: 140, bottom: 20, top: 20),
        child: CardOptions(
        textSection: "Database tables",
        widget: ListView.builder(
          shrinkWrap: true,
          padding: const EdgeInsets.all(8),
          itemCount: tables.length,
          itemBuilder: (BuildContext context, int index) {
            return Container(
              height: 50,
              margin: EdgeInsets.all(2),
              child: Center(
                child: Column(
                  children: [
                    TextButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => SeeTable(table: tables[index])),
                    );
                  },
                  child: Text(tables[index],
                    style: TextStyle(fontSize: 18),
                  )
                ),
                Divider(
                    thickness: 1,
                    indent : 10,
                    endIndent : 10,       
                ),
                  ],
                )
              ),
            );
          }
        )
      )
      ),
    );
  }
}