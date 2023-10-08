class Log {
  late String? userId;
  late String? time;
  late String? testId;
  late String? status;
  late String? eventDetails;

  Log(this.userId, this.time, this.testId, this.status, this.eventDetails);

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['user_id'] = this.userId;
    data['time'] = this.time;
    data['test_id'] = this.testId;
    data['event_type'] = this.status;
    data['event_details'] = this.eventDetails;

    return data;
  }

  @override
  String toString() {
    return '$userId $time $testId $status $eventDetails';
  }
}
