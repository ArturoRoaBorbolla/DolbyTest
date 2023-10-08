import 'package:testdolby/constants/styles.dart';
import 'package:testdolby/widgets/custom_text.dart';
import 'package:flutter/material.dart';

class SectionTitle extends StatelessWidget {
  final CustomText customText;
  final double? height;
  final Color? color;
  const SectionTitle(
      {super.key, required this.customText, this.height, this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
        height: height ?? 60,
        width: double.infinity,
        color: color ?? brown,
        child: Center(
          child: customText,
        ));
  }
}
