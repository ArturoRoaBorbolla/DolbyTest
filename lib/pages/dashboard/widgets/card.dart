import 'package:testdolby/constants/styles.dart';
import 'package:testdolby/widgets/custom_text.dart';
import 'package:testdolby/widgets/section_title.dart';
import 'package:flutter/material.dart';

class CardOptions extends StatelessWidget {
  final String textSection;
  final Widget widget;

  const CardOptions(
      {super.key, required this.textSection, required this.widget});

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      margin: const EdgeInsets.all(15),
      elevation: 10,
      child: Container(
          child: Column(
        children: <Widget>[
          SectionTitle(
            color: lightGrey,
            height: 40,
            customText: CustomText(
              text: textSection,
              size: 26,
              weight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          const SizedBox(
            height: 15,
          ),
          widget,
          const SizedBox(
            height: 15,
          ),
        ],
      )),
    );
  }
}
