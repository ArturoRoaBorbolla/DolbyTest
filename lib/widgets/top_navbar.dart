import 'dart:io';

import 'package:testdolby/constants/styles.dart';
import 'package:testdolby/helpers/responsiveness.dart';
import 'package:flutter/material.dart';

import 'custom_text.dart';

File photoPath = File('assets/Dolby_Logo.png');

AppBar topNavigationBar(BuildContext context, GlobalKey<ScaffoldState> key) =>
    AppBar(
      leading: !ResponsiveWidget.isSmallScreen(context)
          ? Row(
              children: [
                Container(
                  padding: const EdgeInsets.only(left: 20),
                  child: Image.file(
                    photoPath,
                    height: 25,
                  ),
                  /*Image.asset(
                    "assets/Dolby_Logo.png",
                    height: 25,
                  ),*/
                ),
              ],
            )
          : IconButton(
              onPressed: () {
                key.currentState?.openDrawer();
              },
              icon: const Icon(
                Icons.menu,
                color: Colors.black,
              )),
      elevation: 0,
      title: Row(
        children: [
          Container(
              padding: EdgeInsets.only(left: 15),
              child: CustomText(
                text: "Dolby",
                color: navyBlue,
                size: 20,
                weight: FontWeight.bold,
              ))
        ],
      ),
      backgroundColor: Colors.white,
    );
