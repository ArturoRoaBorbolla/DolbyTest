class PriorityTest {
  late String id;
  late String name;
  late String status;

  PriorityTest(this.id, this.name, this.status);

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['name'] = this.name;
    data['status'] = this.status;

    return data;
  }
}
