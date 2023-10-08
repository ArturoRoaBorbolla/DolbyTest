import 'package:testdolby/constants/styles.dart';
import 'package:testdolby/pages/see_tables/widgets/tables.dart';
import 'package:testdolby/widgets/custom_text.dart';
import 'package:flutter/material.dart';

class SeeTablesPage extends StatelessWidget {
  const SeeTablesPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: brown,
        title: CustomText(
          text: 'Database Tables',
          size: 24,
          weight: FontWeight.bold,
          color: Colors.white,
      )),
      body: Tables()
    );
  }
}