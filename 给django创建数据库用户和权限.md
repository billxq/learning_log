### 创建work账户

1. 使用root账户创建数据库django_bbs，为业务开发准备

   ` CREATE DATABASE django_bbs;`

2.  使用root账户创建work账户

   `CREATE USER work IDENTIFIED BY 'Djangobbs'` 创建用户work，密码是Djangobbs

3. 给work账户赋予权限

   `GRANT ALL ON django_bbs.* TO 'work'@'%' WITH GRANT OPTION`  

   设置好后，work账户就有了django_bbs数据库所有的权限
   
4.  查看表字段 `desc post_comment`

