import 'dart:core';
import 'package:testdolby/pages/tresholds/model/test.dart';

class Tresholds{
  late String name;
  late List test;

  Tresholds(this.name, this.test);

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['test'] = this.name;
    data['tests_list'] = this.test;
    return data;
  }
}