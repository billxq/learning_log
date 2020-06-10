### js基本语法



- 赋值

  var a = 1;

- 调用函数

  alert();  \# 和python一致

  var a = "hello"

  alert(a)  \# 传参d

- 定义函数

  ```js
  function x(a) {
      return a;
  }
  
  # 例子：
  function foo(bar) {
      alert(bar);
      return bar;
  }
  ```

- if和else

  ```js
  if (true) {...}
  else{...}
  # 例子
  function foo(bar) {
      if (bar > 3) {
          alert(bar+1);
      } else {
          alert("Not enough!");
      }
  }
  ```

- 列表和数组array

  ```js
  var a = [1,2,3];
  
  # 例子
  var arr = []
  function foo(bar) {
      if (bar > 3) {
          arr.push(bar);
      } else {
          alert("Not enough!");
      }
  }
  ```

- 对象object

  ```js
  o = {
      a:1,   # 键无需加双引号
      b:2
  }
  如何获取键值
  o.a; o.b
  ```

- js操作DOM

  ```js
  DOM,即Document Object Model，网页操作方法
  实例1：
  var el = document.querySelector("#random-ads");  # 找到id是ramdom-ads的元素，并且把它赋值给el，它是一个element对象
  el.setAttribute("style", "display:none;"); # 把style属性的display的值设为none
  ```

- 事件绑定

  - Where：特定区域
  - How：触发事件
  - What：做一些事情

  ```js
  把网站的背景变黑，字体变白
  var b = document.querySelector("body");
  b.setAttribute("style","background-color: black;");
  var dark="background-color: black; color: white;";
  var day="background-color: white; color: black;";
  var theme = {
  	dark="background-color: black; color: white;",
  	day="background-color: white; color: black;"
  };
  
  var button = document.querySelector(".nav");
  var web = document.querySelector("body");
  
  function lightSwitch() {
      if (web.style.cssText == dark) {
          web.style.cssText = day;
          alert("Day mode!");
      } else {
          web.style.cssText = dark;
          alert("Night mode!");
      }
  }
  
  button.onclick = lightSwitch  # 把函数绑定到button中
  ```

  

