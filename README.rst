up2b2
========

这是基于 `sapic <https://github.com/sapicd/sapic>`_
的一个小的扩展模块，用来将上传的图片保存到 BackBlaze `B2 <https://www.backblaze.com/b2/>`_

安装
------

- 正式版本

    `$ pip install -U up2b2`

- 开发版本

    `$ pip install -U git+https://github.com/sapicd/up2b2.git@master`

开始使用
----------

此扩展请在部署 `sapic <https://github.com/sapicd/sapic>`_ 图床后使用，需要
其管理员进行添加扩展、设置钩子等操作。

添加：
^^^^^^^^

请在 **站点管理-钩子扩展** 中添加第三方钩子，输入模块名称：up2b2，
确认后提交即可加载这个模块（请在服务器先手动安装或Web上安装第三方包）。

配置：
^^^^^^^^

在 **站点管理-网站设置** 底部的钩子配置区域配置 BackBlaze B2 相关信息。

Bucket即桶名称，要求公开可读。

在账户-应用密钥中，可以看到KeyID，生成新的主应用程序密钥即可获取应用密钥。

访问域名请浏览档案，在桶中任意上传文件可获取友好URL或S3 URL，任选一种前缀即可：

- 友好URL：`https://f005.backblazeb2.com/file/<Bucket>/`

- S3 URL：`https://<Bucket>.s3.us-east-005.backblazeb2.com/`

使用：
^^^^^^^^

同样在 **站点管理-网站设置** 上传区域中选择存储后端为 `up2b2` 即可，
后续图片上传时将保存到B2。

上传图片的sender名称是：up2b2
