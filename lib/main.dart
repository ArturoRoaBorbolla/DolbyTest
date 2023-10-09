import 'dart:io';
import 'package:testdolby/controllers/menu_controller.dart' as menu;
import 'package:testdolby/controllers/navigation_controller.dart';
import 'package:testdolby/pages/authentication/authentication.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:localstorage/localstorage.dart' as ls;
import 'package:fluttertoast/fluttertoast.dart';


void main() {
  executeInstallation();
  Get.put(menu.MenuController());
  Get.put(NavigationController());
  runApp(MyApp());
  final ls.LocalStorage storage = ls.LocalStorage('login');
  storage.setItem('is_loading', false);
}

void executeInstallation() async {
  Directory currentDir = Directory.current;
  final installationScript = '${currentDir.path}\\scripts\\common\\instalation.py';

  final pythonCommand = 'python';
  final pythonArguments = [installationScript];

  Process.run(pythonCommand, pythonArguments).then((ProcessResult results) {
    print('Instalation: ${results.stdout}');
  });

  final pipOutputFile = File('${currentDir.path}\\scripts\\common\\pip_output.txt');
  String pipOutputContent = await pipOutputFile.readAsString();
  print('Content of  pip_output.txt: $pipOutputContent');

  //Flushbar(
  //  message: pipOutputContent,
  //  duration: Duration(seconds: 5),
  //  backgroundColor: Colors.black,
  //  textColor: Colors.white,
 // )..show(context);


}



class MyApp extends StatelessWidget {
  MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Bot Dashboard - Aiver',
      theme: ThemeData(
          scaffoldBackgroundColor: Colors.white,
          textTheme: GoogleFonts.mulishTextTheme(Theme.of(context).textTheme)
              .apply(bodyColor: Colors.black),
          pageTransitionsTheme: const PageTransitionsTheme(builders: {
            TargetPlatform.iOS: FadeUpwardsPageTransitionsBuilder(),
            TargetPlatform.android: FadeUpwardsPageTransitionsBuilder()
          }),
          primaryColor: Colors.blue),
      home: const AuthenticationPage(),
    );
  }
}
