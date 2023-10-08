import 'dart:io';

import 'package:testdolby/widgets/alert.dart';
import 'package:process_run/shell.dart';

import 'package:testdolby/widgets/card_with_title.dart';
import 'package:flutter/material.dart';
import 'package:webview_windows/webview_windows.dart';

import '../../widgets/custom_text.dart';
import 'package:testdolby/constants/styles.dart';

class ViewPage extends StatefulWidget {
  final String test;
  const ViewPage({super.key, required this.test});

  @override
  State<ViewPage> createState() => _ViewPageState();
}

class _ViewPageState extends State<ViewPage> {
  final _controller = WebviewController();
  final _textController = TextEditingController();
  final TextEditingController _textFieldController = TextEditingController();
  String codeDialog = "0";
  String valueText = "0";
  bool loading = true;

  final List _test = [
    {"id": "Test_1", "result": "Test_1_2_1"},
    {"id": "Test_2", "result": "Test_2_1"},
    {"id": "Test_3", "result": "Test_3_1_2"},
    {"id": "Test_4", "result": "OR_4_1_9"},
    {"id": "Test_5", "result": "OR_5_1"},
    {"id": "Test_6", "result": "OR_6_2"},
    {"id": "Test_7", "result": "OR_7_2"}
  ];

  Future<void> initPlatformState() async {
    await _controller.initialize();
    if (!mounted) return;
    setState(() {});

    if (_controller.value.isInitialized) {
      //stderr.writeln("Done");
    }
    //stderr.writeln("No");
  }

  Future<void> _alertRowsNumber(BuildContext context) async {
    return showDialog(
        context: context,
        builder: (context) {
          return AlertDialog(
            title: const Text('Select the rows number in the results'),
            content: TextField(
              onChanged: (value) {
                setState(() {
                  valueText = value;
                });
              },
              controller: _textFieldController,
              decoration: const InputDecoration(hintText: 'Rows number'),
            ),
            actions: <Widget>[
              MaterialButton(
                color: red,
                textColor: Colors.white,
                child: const Text('CANCEL'),
                onPressed: () {
                  setState(() {
                    Navigator.pop(context);
                  });
                },
              ),
              MaterialButton(
                color: green,
                textColor: Colors.white,
                child: const Text('OK'),
                onPressed: () {
                  setState(() {
                    codeDialog = valueText;
                    try {
                      int.parse(codeDialog);
                      shellCommand();
                      setState(() {
                        loading = true;
                      });
                      Navigator.of(context).pop();
                    } catch (e) {
                      print(e);
                      _alertError(
                        context,
                        'Wrong type of value',
                        'Put an integer value for the rows number.'
                      );
                    }
                  });
                },
              ),
            ],
          );
        });
  }

  _alertError(context, title, content) {
    Alert.noticeAlert(context, title, content);
  }
  Future shellCommand() async {
    var shell = Shell();
    late String shellCommandPython;

    String currentDir = Directory.current.path.replaceAll("'", "").replaceAll('\\', '\\\\').replaceAll('/', '//');
    //String current = '${currentDir}\\\\scripts\\\\${widget.test}\\\\Output\\\\${widget.test}.py';
    String current = '${currentDir}\\\\scripts\\\\${widget.test}\\\\Output\\\\';
    print("curren directory");
    print(current);


    if (int.parse(codeDialog) == 0)
    {
      shellCommandPython = '''python -c "import scripts.common.visualize as create;create.create_html('${current}',10)"''';
    }
    else
      {
        shellCommandPython = '''python -c "import scripts.common.visualize as create;create.create_html('${current}','''+ int.parse(codeDialog).toString()+''')"''';
      }


    await shell.run(shellCommandPython).then((value) async {
      for(var code in value){
        String url = '';
          for (var test in _test) {
            if (test['id'] == widget.test) {
              String result = test['result'];
              url =
                  'file:///$currentDir\\scripts\\${widget.test}\\Output\\html\\${result}.html';
            }
          }
          print("Next one is the url");
          print(url);
          _controller.loadUrl(url);
          await _controller.setBackgroundColor(Colors.transparent);
          await _controller.setPopupWindowPolicy(WebviewPopupWindowPolicy.deny);
          await _controller.loadUrl(url);
      }
    });
    setState(() {
      loading = false;
    });
  }

  Widget loader(){
    return Container(color: Colors.white, child: Transform.scale(
        scale: 3,
        child: Center(
          child: CircularProgressIndicator(strokeWidth: 3),
      ),
    ));
  }

  Widget body(){
    return ListView(
      children: [
        CardOptions(
            textSection: "Visualization",
            widget: Column(
              children: [
                SizedBox(
                  height: 10,
                ),
                Container(
                  padding: EdgeInsets.only(left: 100, right: 100),
                  width: double.infinity,
                  child: Align(
                    alignment: Alignment.centerRight,
                    child: ElevatedButton(
                        child: Text('Select rows number'),
                        onPressed: () => _alertRowsNumber(context)),
                  ),
                ),
                SizedBox(
                  height: 30,
                ),
                Container(
                  width: MediaQuery.of(context).size.width * 0.85,
                  height: MediaQuery.of(context).size.height * 0.8,
                  child: Webview(
                    _controller,
                  ),
                )
              ],
            )),
        SizedBox(
          height: 20,
        )
      ],
    );
  }

  @override
  void initState() {
    super.initState();
    shellCommand();
    initPlatformState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          backgroundColor: brown,
          title: CustomText(
            text: "Test Result ${widget.test}",
            size: 24,
            weight: FontWeight.bold,
            color: Colors.white,
          )),
      body: loading? loader() : body()
    );
  }
}
