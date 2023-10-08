import 'package:testdolby/service/sqlite_service.dart';
import 'package:flutter/material.dart';
import 'package:localstorage/localstorage.dart';

class DropDown extends StatefulWidget {
  final Function callback;
  final int? role;
  final String? username;
  const DropDown({super.key, required this.callback, this.role, this.username});

  @override
  State<DropDown> createState() => _DropDownState();
}

class _DropDownState extends State<DropDown> {
  final LocalStorage storage = LocalStorage('login');
  late List<dynamic> _users = [];
  String? _user;

  List<dynamic> userOptions() {
    int userType = storage.getItem('type_user');
    List userOptions = [];    
    if (userType == 2) {
      userOptions = [
        {"id": 3, "type": "User"}
      ];
    }
    if(userType == 1){
      userOptions = [
        {"id": 3, "type": "User"},
        {"id": 2, "type": "Admin"},
      ];
    }
    if (userType == 2 && widget.role == 2) {
      userOptions = [
        {"id": 3, "type": "User"},
        {"id": 2, "type": "Admin"},
      ];
    } 
    print(userType);
    print(userOptions);
    return userOptions;
  }

  @override
  void initState() {
    super.initState();
    _users = userOptions();
    if(widget.role != null){
      _user = widget.role.toString();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          height: 55,
          color: Colors.white,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: <Widget>[
              Expanded(
                child: InputDecorator(
                  decoration: InputDecoration(
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10.0),
                      borderSide:
                          const BorderSide(color: Colors.black87, width: 0.0),
                    ),
                    border: const OutlineInputBorder(),
                  ),
                  child: DropdownButtonHideUnderline(
                    child: ButtonTheme(
                      alignedDropdown: true,
                      child: DropdownButton<String>(
                        isExpanded: true,
                        value: _user,
                        iconSize: 30,
                        style: const TextStyle(
                          color: Colors.black,
                          fontSize: 16,
                        ),
                        hint: const Text('Type of user'),
                        onChanged: (value) => setState(() {
                          _user = value;
                          widget.callback(_user);
                        }),
                        items: _users.map((item) {
                              return DropdownMenuItem(
                                value: item['id'].toString(),
                                child: Text(item['type']),
                              );
                            }).toList() ??
                            [],
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
