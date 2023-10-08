import 'package:flutter/material.dart';

enum FieldType {
  inputFiled,
  passwordField,
  disabledField
}

class CustomTextField extends StatefulWidget {
  final TextEditingController controller;
  final String hintText;
  final FieldType fieldType;
  const CustomTextField({super.key, required this.controller, required this.hintText, required this.fieldType});

  @override
  State<CustomTextField> createState() => _CustomTextFieldState();
}

class _CustomTextFieldState extends State<CustomTextField> {


  Widget check(FieldType input){
    switch (input) {
        case FieldType.inputFiled:
          return inputFiled();
        case FieldType.passwordField:
          return  passwordField();
        case FieldType.disabledField:
          return disabledField();
      }
  }

  Widget inputFiled(){
    return SizedBox(
      width: MediaQuery.of(context).size.width * 0.5,
      child: TextField(
        controller: widget.controller,
        decoration: InputDecoration(
            contentPadding: EdgeInsets.only(
                left: 27.0, right: 27.0),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(10.0),
            ),
            filled: true,
            hintStyle:
                TextStyle(color: Colors.grey[500]),
            hintText: widget.hintText,
            fillColor: Colors.white70),
      ),
    );
  }

  Widget passwordField(){
    return SizedBox(
      width: MediaQuery.of(context).size.width * 0.5,
      child: TextField(
        controller: widget.controller,
        obscureText: true,
        decoration: InputDecoration(
            contentPadding: EdgeInsets.only(
                left: 27.0, right: 27.0),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(10.0),
            ),
            filled: true,
            hintStyle:
                TextStyle(color: Colors.grey[500]),
            hintText: widget.hintText,
            fillColor: Colors.white70),
      ),
    );
  }

  Widget disabledField(){
    return SizedBox(
      width: MediaQuery.of(context).size.width * 0.5,
      child: TextField(
        controller: TextEditingController()..text = 'Superadmin',
        enabled: false, 
        decoration: InputDecoration(
            contentPadding: EdgeInsets.only(
                left: 27.0, right: 27.0),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(10.0),
            ),
            filled: true,
            hintStyle:
                TextStyle(color: Colors.grey[500]),
            hintText: "Role",
            fillColor: Colors.white70),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return check(widget.fieldType);
  }
}