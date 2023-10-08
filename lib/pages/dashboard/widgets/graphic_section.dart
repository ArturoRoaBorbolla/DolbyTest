import 'dart:io';

import 'package:testdolby/pages/dashboard/dashboard.dart';
import 'package:testdolby/pages/dashboard/widgets/web_view_card.dart';
import 'package:testdolby/service/json_service.dart';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:webview_windows/webview_windows.dart';
import 'package:localstorage/localstorage.dart' as ls;

class GraphicSection extends StatefulWidget {
  final List subheaders;
  const GraphicSection({super.key, required this.subheaders});

  @override
  State<GraphicSection> createState() => GraphicSectionState();
}

class GraphicSectionState extends State<GraphicSection> {
  ls.LocalStorage storage = ls.LocalStorage('login');
  Directory currentDir = Directory.current;
  List<Widget> row = [];
  bool loading = true;

  readJson(String path) async {
    JsonService jsonService = JsonService();
    List jsonResponse = [];
    jsonResponse = await jsonService.readJson(path);
    return jsonResponse;
  }

  Future<void> rows(List urls, List controllers) async {
    List numCell = [];
    List<Widget> cells = [];
    List graphicsResponse = await readJson(
        '${currentDir.path}/assets/json/dashboard_graphics.json');
    numCell = graphicsResponse[0]['rows'];
    int index = 0;
    for (int i = 0; i < numCell.length; i++) {
      for (int j = 0; j < numCell[i]; j++) {
        cells.add(WebViewCard(
            textSection: widget.subheaders[index],
            stringUrlGraphic: urls[index],
            urlGraphic: controllers[index]));
        cells.add(VerticalDivider(width: 1.0));
        index += 1;
      }
      row.add(Row(children: cells));
      cells = [];
    }
    setState(() {
      loading = false;
    });
  }

  initPlatformState() async {
    List controllers = [];
    for (int i = 0; i < 8; i++) {
      controllers.add(WebviewController());
      await controllers[i].initialize();
    }
    webView(controllers);
  }

  Future<void> webView(List controllers) async {
    List urls = [];
    List response = await readJson(
        '${currentDir.path}/assets/json/dashboard_graphics.json');
    urls = response[1]['urls'];
    for (int i = 0; i < 7; i++) {
      //controllers[i].loadUrl(urls[i]);
      await controllers[i].setBackgroundColor(Colors.transparent);
      await controllers[i].setPopupWindowPolicy(WebviewPopupWindowPolicy.allow);
      var page = urls[i];
      page = "${currentDir.path}/scripts/$page";
      print(page);
      await controllers[i].loadUrl(page);
      //await controllers[i].loadUrl(urls[i]);
      //print(urls[i].toString());
    }
    rows(urls, controllers);
  }

  @override
  void initState() {
    initPlatformState();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    if (loading) {
      return SizedBox(
          height: MediaQuery.of(context).size.height - 500,
          width: MediaQuery.of(context).size.width - 200,
          child: Transform.scale(
            scale: 3,
            child: Center(
              child: CircularProgressIndicator(strokeWidth: 3),
            ),
          ));
    }
    return Column(children: row);
  }
}
