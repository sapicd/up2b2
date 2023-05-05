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

在 **站点管理-网站设置** 底部的钩子配置区域配置B2相关信息，
如Bucket、访问密钥ID和Secret等（请在BackBlaze创建一个B2服务，并在
用户-我的安全凭证-访问密钥，创建新的访问密钥，拿到密钥ID（AccessKey）、SecretKey；
允许使用子用户IAM的密钥，要求拥有B2管理权限）。

目前要求B2配置为公开访问，钩子上传的图片、视频其ACL也是公共可读。

使用：
^^^^^^^^

同样在 **站点管理-网站设置** 上传区域中选择存储后端为up2b2即可，
后续图片上传时将保存到B2。

上传图片的sender名称是：up2b2
