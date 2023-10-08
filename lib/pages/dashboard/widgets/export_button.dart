import 'package:flutter/material.dart';

import 'package:dropdown_button2/dropdown_button2.dart';
import 'package:material_design_icons_flutter/material_design_icons_flutter.dart';

class ExportButton extends StatefulWidget {
  const ExportButton({super.key});

  @override
  State<ExportButton> createState() => _ExportButtonState();
}

class _ExportButtonState extends State<ExportButton> {
  @override
  Widget build(BuildContext context) {
    return DropdownButtonHideUnderline(
      child: DropdownButton2(
        customButton: const Icon(
          MdiIcons.fileExportOutline,
          size: 46,
          color: Colors.grey,
        ),
        items: [
          ...MenuItems.menuItems.map(
            (item) => DropdownMenuItem<MenuItem>(
              value: item,
              child: MenuItems.buildItem(item),
            ),
          )
        ],
        onChanged: (value) {
          MenuItems.onChanged(context, value as MenuItem);
        },
        dropdownStyleData: DropdownStyleData(
          width: 200,
          padding: const EdgeInsets.symmetric(vertical: 6),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(4),
            color: Colors.grey,
          ),
          elevation: 8,
          offset: const Offset(0, 8),
        ),
        menuItemStyleData: MenuItemStyleData(
          customHeights: [
            ...List<double>.filled(MenuItems.menuItems.length, 48),
          ],
          padding: const EdgeInsets.only(left: 16, right: 16),
        ),
      ),
    );
  }
}

class MenuItem {
  final String text;
  final IconData icon;

  const MenuItem({
    required this.text,
    required this.icon,
  });
}

class MenuItems {
  late TextEditingController _controller;
  late String fileName;

  static const List<MenuItem> menuItems = [print, toHtml, toExcel, toPdf];

  static const print = MenuItem(text: 'Print', icon: MdiIcons.printer);
  static const toHtml = MenuItem(text: 'To HTML', icon: MdiIcons.languageHtml5);
  static const toExcel = MenuItem(text: 'To Excel', icon: MdiIcons.fileExcel);
  static const toPdf = MenuItem(text: 'To PDF', icon: MdiIcons.filePdfBox);

  static Widget buildItem(MenuItem item) {
    return Row(
      children: [
        Icon(item.icon, color: Colors.white, size: 22),
        const SizedBox(
          width: 10,
        ),
        Text(
          item.text,
          style: const TextStyle(
            color: Colors.white,
          ),
        ),
      ],
    );
  }

  static onChanged(BuildContext context, MenuItem item) {
    switch (item) {
      case MenuItems.print:
        debugPrint("print");
        break;
      case MenuItems.toHtml:
        debugPrint("html");
        break;
      case MenuItems.toExcel:
        debugPrint("excel");
        break;
      case MenuItems.toPdf:
        debugPrint("pdf");
        break;
    }
  }
}
