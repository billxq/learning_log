### Vue.js

- 在body标签最后添加：

  ```js
  <script>
  	var vm = new Vue({
          el:"#app",			# app是body标签的id
          data: {				# 类似于django中的context
          	article:{
          		title: "Here's a title",
          		content: "Hey, there!"
      		},
      	}
      })    
  </script>
  ```

  

- 循环