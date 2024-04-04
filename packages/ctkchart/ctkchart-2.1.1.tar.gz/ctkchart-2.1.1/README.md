<div align="center">

[![ctkchart](https://snyk.io/advisor/python/ctkchart/badge.svg)](https://snyk.io/advisor/python/ctkchart)

<img src="https://drive.google.com/thumbnail?id=1f4Q2dA64iJGUVWpAZsl0q6Mq0NVkGCDR&sz=w900">

[![Downloads](https://static.pepy.tech/badge/ctkchart)](https://pepy.tech/project/ctkchart) [![Downloads](https://static.pepy.tech/badge/ctkchart/month)](https://pepy.tech/project/ctkchart) [![Downloads](https://static.pepy.tech/badge/ctkchart/week)](https://pepy.tech/project/ctkchart)

<img src="https://drive.google.com/thumbnail?id=1-RSoULrf_fnIT0Tufm9VizmryPepwSTv&sz=w180">

</div>

**<li>ctkchart is a Python library for creating live updating line charts in customtkinter.</li>**

</div>

<hr>

### Features

- **Live Update**: Display live data with line charts.
- **Multiple Lines**: Support for plotting multiple lines on the same chart for easy comparison.
- **Color Customization**: Customize colors to match your application's design or data representation.
- **Dynamic Color Change**: Dynamic Color Change for Dark & Light.
- **Font Customization**: Adjust fonts for text elements to enhance readability.
- **Dimension Customization**: Customize chart dimensions to fit various display sizes and layouts.

<hr>

### Importing & Installation
* **Installation**
    ```
    pip install ctkchart
    ```

* **Importing**
    ```
    import ctkchart
    ```

<hr>

### Simple Guide
- **import package**
    ```
    import ctkchart
    ```

- **Create Line Chart and place the chart**
    ```
    chart = ctkchart.CTkLineChart(master=root,
                                x_axis_values=("a", "b", "c", "d", "e", "f"),
                                y_axis_values=(100, 900))
    chart.place(x=10, y=10)
    ```

- **Create Line**
    ```
    line = ctkchart.CTkLine(master=chart)
    ```

- **Display Data**
    display data using a loop
    ```

    def loop():
        while True:
            random_data = random.choice(range(100, 900))
            chart.show_data(line=line, data=[random_data])
            time.sleep(1)
    
    #call the loop as thead
    theading.Thread(target=loop).start()
    ```

<hr>

### Full Code Example
```
import ctkchart #  <- import the package
import tkinter
import random
import threading
import time

#create window
root = tkinter.Tk()

#create chart
chart = ctkchart.CTkLineChart(master=root,
                                x_axis_values=("a", "b", "c", "d", "e", "f"),
                                y_axis_values=(100, 900))
chart.place(x=10, y=10) #place chrt

#create line
line = ctkchart.CTkLine(master=chart)

def loop():
    while True:
        random_data = random.choice(range(100, 900)) #get random data
        chart.show_data(line=line, data=[random_data]) # <- display data using chart 
        time.sleep(1) #wait 1 sec
        
#call the loop as thead
threading.Thread(target=loop).start()

root.mainloop()
```

<hr>

### Links

- [**Documentation**](https://github.com/Thisal-D/ctkchart/blob/main/documentation/)
    - [English](https://github.com/Thisal-D/ctkchart/blob/main/documentation/DOCUMENTATION_EN.md)
    - [chinese](https://github.com/Thisal-D/ctkchart/blob/main/documentation/DOCUMENTATION_CN.md)
- **GitHub Repository :** [ctkchart](https://github.com/Thisal-D/ctkchart)