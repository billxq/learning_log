### 用 Semantic UI 轻松上手第一个网页

- 使用基础样式

  - 在编辑器中输入html就会呈现模板

  - 在head中引用，加入link标签，要注意：rel="sytlesheet"和href属性

    ```html
    <head>
    	<link rel="stylesheet" href="css/semantic.css" media="screen">
    </head>
    ```

  - 在body标签下增加内容，要注意随时保存

    ```html
    <body>
        <div class="ui segment">
            hello
        </div>
        <div class="ui segment">
            my friend
        </div>
    </body>
    ```

    

- 使用“形容词”改变样式

  - inverted color反转颜色: inverted red 背景变为红色，直接写inverted即为黑色

    ```html
    <body>
        <div class="ui inverted blue segment">
    Give me the strength lightly to bear my joys and sorrows.Give me the strength to make my love fruitful in service.Give me the strength never to disown the poor or bend my knees before insolent might.Give me the strength to raise my mind high above daily trifles.And give me the strength to surrender my strength to thy will with love.
        </div>
        <div class="ui inverted segment">
           Give me the strength lightly to bear my joys and sorrows.Give me the strength to make my love fruitful in service.Give me the strength never to disown the poor or bend my knees before insolent might.Give me the strength to raise my mind high above daily trifles.And give me the strength to surrender my strength to thy will with love.
        </div>
    </body>
    ```

  - vertical垂直：文字紧贴左边

    ![image-20200423110740934](C:\Users\bill-\AppData\Roaming\Typora\typora-user-images\image-20200423110740934.png)

  - padded和边距保持距离，还有very padded

  - basic：去除每个segment的线条 `<div class="ui vertical basic segement"></div>`

  - container容器

  - fixed： 元素一直停留在这个位置，无论上下拉动页面`<div class="ui fixed inverted segement"><div>`

    - 例子：设计菜单栏

      ```html
      <div class="ui fixed inverted segement">
          <a class="item" href="#">Home</a>  # ‘#’表示不跳转
          <a class="item" href="#">About</a>
          <a class="item" href="#">Contact</a>
      </div>
      ```

    - vertical text menu: 垂直文本菜单

      ```html
      <div class="ui vertical text menu">
          <div class="item">
              1
          </div>
          <div class="item">
              2
          </div>
          <div class="item">
              3
          </div>
      </div>   # 看不到文字可以用inverted
      ```

      

  - 网格grid：默认16栏

    - 例子

      ```html
      <div class="ui grid">
          <div class="ten wide column">
              <img src="" alt="" /> # 前10栏插入图片
          </div>
          <div class="six wide column">  # 后6栏是文章
              <h2 class="ui header">
                  <i class="icon star"></i>  # 图标的样式
                  This is a title
              </h2>
      		<P>
                  This is the paragraph.
              </P>
          </div>
      </div>
      ```

      

- 使用嵌套制作

  - 根据上面的例子衍生：

    ```html
    <body>
        <div class="ui inverted blue segment">
    Give me the strength lightly to bear my joys and sorrows.Give me the strength to make my love fruitful in service.Give me the strength never to disown the poor or bend my knees before insolent might.Give me the strength to raise my mind high above daily trifles.And give me the strength to surrender my strength to thy will with love.
        </div>
        <div class="ui inverted vertical segment padded">
            <div class="ui container segment">
                <h1 class="ui header">
                    My poem
                </h1>
                <P>
                    Give me the strength lightly to bear my joys and sorrows.Give me the strength to make my love fruitful in service.
                </P>
                <button class="ui inverted blue button" type="button" name="button">
                    Read more
                </button>
            </div>
    
        </div>
    </body>
    ```

  - 通过ui image加入banner

    ```html
    <div class="ui image">
        <img src="images/banner.png" alt="" />
    </div>
    ```

  - footer

    ```html
    <div class="ui segment inverted very padded vertical">
        <img src="images/banner.png" alt="" />
    </div>
    ```

    