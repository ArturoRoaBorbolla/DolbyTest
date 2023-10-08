import 'package:testdolby/constants/styles.dart';
import 'package:testdolby/model/user.dart';
import 'package:testdolby/pages/see_users/widgets/drop_down.dart';
import 'package:testdolby/pages/see_users/widgets/space.dart';
import 'package:testdolby/pages/see_users/widgets/textfield.dart';
import 'package:testdolby/service/sqlite_service.dart';
import 'package:testdolby/widgets/alert.dart';
import 'package:testdolby/widgets/card_with_title.dart';
import 'package:testdolby/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class SeeUserPage extends StatefulWidget {
  final String username;
  const SeeUserPage({super.key, required this.username});

  @override
  State<SeeUserPage> createState() => _SeeUserPageState();
}

class _SeeUserPageState extends State<SeeUserPage> {
  final nameController = TextEditingController();
  final lastnameController = TextEditingController();
  final titleController = TextEditingController();
  final passwordController = TextEditingController();
  final confirmPasswordController = TextEditingController();
  late int role = 0;  
  late SqliteService _sqliteService;
  
  @override
  void initState()  {
    _sqliteService= SqliteService();
    super.initState();  
  }

  Future<User> getData() {
    return _sqliteService.getUser(widget.username);
  }

  create(User user) async{
    await _sqliteService.createUser(user).then((value){
      _alertGoBack(context, "Save user",
        "The user ${widget.username} has been saved successfully.");
    }).catchError((e){
      print(e);
      _alert(context, "Saving user",
        "There has been an error saving ${user.username} user. Try to register the user again.");
    });
  }

  update(User user) async{
    await _sqliteService.updateUser(user).then((value){
      _alertGoBack(context, "Update user",
        "The user ${widget.username} has been updated successfully.");
    }).catchError((e){
      print(e);
      _alert(context, "Updating user",
        "There has been an error updating ${user.username} user. Try to update the user again.");
    });
  }

  delete(User user) async{
    _alertWithFunction(context, "Delete user",
      "Are you sure you want to delete this user?", () {
          _sqliteService.deleteUser(user).then((value) {
            _alertGoBack(context, "Delete user",
            "The user ${widget.username} has been delete successfully.");
        }).catchError((e){
          print(e);
          _alert(context, "Updating user",
            "There has been an error updating ${user.username} user. Try to update the user again.");
        });
      }
    );
    
  }

  _alert(BuildContext context, String title, String content) {
    Alert.noticeAlert(context, title, content);
  }

  _alertGoBack(BuildContext context, String title, String content) {
    Alert.noticeAlertGoBack(context, title, content);
  }

  _alertWithFunction(BuildContext context, String title, String content, Function function) {
    Alert.alertGoBack(context, title, content, function);
  }

  Widget body(Function function, bool deleteButton){
    return SingleChildScrollView(
      child: Column(
        children: [
          Container(
            height: MediaQuery.of(context).size.height * 0.9,
            child: CardOptions(
              textSection: "${widget.username}",
              widget: Expanded(
                child: SingleChildScrollView(
                child: Column(
                  children: [
                    deleteButton ? 
                    Container(
                      padding: EdgeInsets.only(left: 100, right: 100),
                      width: double.infinity,
                      child: Align(
                        alignment: Alignment.centerRight,
                        child: ElevatedButton(
                            child: Text('Delete user'),
                            onPressed: () => delete(User.delete(widget.username))),
                      ),
                    ) : Container(),
                    Space(),
                    CustomTextField(controller: nameController, hintText: "Name", fieldType: FieldType.inputFiled),
                    Space(),
                    CustomTextField(controller: lastnameController, hintText: "Lastname", fieldType: FieldType.inputFiled),
                    Space(),
                    CustomTextField(controller: titleController, hintText: "Title", fieldType: FieldType.inputFiled),
                    Space(),
                    (role!=1) ?
                    SizedBox(
                      width: MediaQuery.of(context).size.width * 0.5,
                      child: Column(children: [(role==0) ? 
                      DropDown(callback: (value) => role = int.parse(value)) :
                      DropDown(callback: (value) => role = int.parse(value), role: role, username: widget.username)])
                    ) :
                    CustomTextField(
                      controller: TextEditingController()..text = 'Superadmin', 
                      hintText: "Role", 
                      fieldType: FieldType.disabledField),
                    Space(),
                    CustomTextField(controller: passwordController, hintText: "Password", fieldType: FieldType.passwordField),
                    Space(),
                    CustomTextField(controller: confirmPasswordController, hintText: "Confirm password", fieldType: FieldType.passwordField),
                    Space(),
                    ElevatedButton(
                      onPressed: () {
                        if (nameController.text.isEmpty ||
                            lastnameController.text.isEmpty ||
                            titleController.text.isEmpty ||
                            passwordController.text.isEmpty ||
                            confirmPasswordController.text.isEmpty) {
                          _alert(context, "Empty fields",
                              "The user ${widget.username} has not been saved successfully, all fields must be filled");
                        } else {
                          if (passwordController.text !=
                              confirmPasswordController.text) {
                            _alert(context, "Passwords do not match",
                                "Password and confirm password fields must match");
                          } else {
                            function(User(widget.username, nameController.text, lastnameController.text, titleController.text, role, passwordController.text));                                    
                          }
                        }
                      },
                      child: Text('Save'),
                      style: ElevatedButton.styleFrom(
                          shape: StadiumBorder(),
                          padding: EdgeInsets.all(20)),
                    ),
                  ],
                ),
              ) 
              )
            )
          ),
        ],
      ),    
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          backgroundColor: brown,
          title: CustomText(
            text: "User",
            size: 24,
            weight: FontWeight.bold,
            color: Colors.white,
          ),
      ),
        body: FutureBuilder(
          builder: (ctx, snapshot) {
            if (snapshot.connectionState == ConnectionState.done) {
              if (snapshot.hasError) {
                return body(create, false);
          } else if (snapshot.hasData) {
            final data = snapshot.data;
            nameController.text = data!.name;
            lastnameController.text = data.lastname;
            titleController.text = data.title;
            role = data.role;  
            return body(update, true);
          }
        }

        return Center(
          child: CircularProgressIndicator(),
        );
      },
      future: getData(),
    ),
  );
  }
}


        