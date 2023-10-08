import 'dart:io';

import 'package:flutter/material.dart';
import 'package:testdolby/pages/dashboard/widgets/card.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:webview_windows/webview_windows.dart';

class WebViewCard extends StatelessWidget {
  final String textSection;
  final String? stringUrlGraphic;
  final WebviewController? urlGraphic;
  WebViewCard(
      {super.key,
      required this.textSection,
      this.urlGraphic,
      this.stringUrlGraphic});

  @override
  Widget build(BuildContext context) {
    return Expanded(
        child: CardOptions(
            textSection: textSection,
            widget: Container(
              //width: MediaQuery.of(context).size.width * 0.6,
              //height: MediaQuery.of(context).size.height * 0.6,
              width: MediaQuery.of(context).size.width * 0.8,
              height: MediaQuery.of(context).size.height * 0.8,

            child: (Platform.isAndroid || Platform.isIOS)
                  ? InAppWebView(
                      initialUrlRequest:
                          URLRequest(url: Uri.parse(stringUrlGraphic!)),
                    )
                  : (Platform.isWindows)
                      ? Webview(
                          urlGraphic!,
                        )
                      : Text("Option for MacOS"),
            )));
  }
}
