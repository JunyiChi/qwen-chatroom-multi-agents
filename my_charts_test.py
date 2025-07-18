from pyecharts.charts import  Line
line = Line()
line.add_xaxis(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
line.add_yaxis("Product A", [120, 132, 101, 134, 90, 230, 210])
line.add_yaxis("Product B", [220, 182, 191, 234, 290, 330, 310])
line.render()
