class Test {
  late String id;
  late String name;
  late String lastRunDate;
  late String description;

  Test(this.id, this.name, this.lastRunDate, this.description);

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['name'] = this.name;
    data['last_run_date'] = this.lastRunDate;
    data['description'] = this.description;

    return data;
  }
}
