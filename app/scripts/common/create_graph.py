def create_data(headers,data):
    string=""
    for i in range(len(headers)):
        string+=f" {{'country' : '{headers[i]}','visits' : '{data[i]}' }}, "
    return string
    
def creategraph(filename,headers,data):
    return f'''
    <div class="col-md-6">
                                <!-- Widget -->
                                <div class="widget">
                                    <div class="widget-extra text-center themed-background-flatie">
                                <!--        <h3 class="widget-content-light"><strong>Payments by Currency</strong></h3>-->
                                    </div>
<br>
<br>
                                    <div class="widget-simple">
                                        <div class="row text-center">

                                            <!-- Styles -->
                                            <style>
                                            #chartdiv {{
                                              width: 100%;
                                              height: 600px;
                                            }}
                                            </style>
                                            
                                            <!-- Resources -->
                                            <script src="https://www.amcharts.com/lib/4/core.js"></script>
                                            <script src="https://www.amcharts.com/lib/4/charts.js"></script>
                                            <script src="https://www.amcharts.com/lib/4/themes/animated.js"></script>
                                            <script src="https://cdn.amcharts.com/lib/5/index.js"></script>
                                            <script src="https://cdn.amcharts.com/lib/5/xy.js"></script>
                                            <script src="https://cdn.amcharts.com/lib/5/themes/Animated.js"></script>
                                            <script src="https://cdn.amcharts.com/lib/5/plugins/exporting.js"></script>
                                            
                                            <!-- Chart code -->
                                            <script>
                                            am4core.ready(function() {{
                                            
                                            
                                            am4core.useTheme(am4themes_animated);
                                            
                                            
                                            
                                            var chart = am4core.create("chartdiv", am4charts.RadarChart);
                                            
                                            chart.data = [
                                            {create_data(headers,data)}
                                            ];
                                            
                                            chart.innerRadius = am4core.percent(30)
                                            
                                            var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
                                            categoryAxis.renderer.grid.template.location = 0;
                                            categoryAxis.dataFields.category = "country";
                                            categoryAxis.renderer.minGridDistance = 50;
                                            categoryAxis.renderer.inversed = true;
                                            categoryAxis.renderer.labels.template.location = 0.5;
                                            categoryAxis.renderer.grid.template.strokeOpacity = 0.08;
                                            
                                            var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
                                            valueAxis.min = 0;
                                            valueAxis.extraMax = 0.1;
                                            valueAxis.renderer.grid.template.strokeOpacity = 0.08;
                                            
                                            chart.seriesContainer.zIndex = -10;
                                            
                                            
                                            var series = chart.series.push(new am4charts.RadarColumnSeries());
                                            series.dataFields.categoryX = "country";
                                            series.dataFields.valueY = "visits";
                                            series.tooltipText = "{{valueY.value}}"
                                            series.columns.template.strokeOpacity = 0;
                                            series.columns.template.radarColumn.cornerRadius = 3;
                                            series.columns.template.radarColumn.innerCornerRadius = 0;
                                            
                                            chart.zoomOutButton.disabled = true;
                                            
                                            series.columns.template.adapter.add("fill", (fill, target) => {{
                                             return chart.colors.getIndex(target.dataItem.index);
                                            }});

                                            categoryAxis.sortBySeries = series;
                                            
                                            chart.cursor = new am4charts.RadarCursor();
                                            chart.cursor.behavior = "none";
                                            chart.cursor.lineX.disabled = true;
                                            chart.cursor.lineY.disabled = true;
                                            chart.exporting.menu = new am4core.ExportMenu();
                                            }}); 
                                            
                                            setInterval(()=>{{location.reload() ;}}, 15000)
                                            </script>
                                            
                                            <!-- HTML -->
                                            <div id="chartdiv"><div style="width: 40%; height: 40%; position: relative; top: -0.21875px; left: -0.5px;"></div></div>

                                        </div>
<br>
<br>

                                    </div>
                                <!-- END Widget -->
                            </div>
                        </div>
    
    '''




