# -*- coding: utf-8 -*-
"""
    up2b2
    ~~~~~

    Save uploaded pictures in Backblaze B2.

    :copyright: (c) 2023 by Hiroshi.tao.
    :license: Apache 2.0, see LICENSE for more details.
"""

__version__ = "0.1.0"
__author__ = "staugur <me@tcw.im>"
__hookname__ = "up2b2"
__description__ = "将图片保存到Backblaze B2"
__catalog__ = "upload"

from flask import g
from b2sdk.v2 import InMemoryAccountInfo, B2Api, Bucket, FileVersion
from b2sdk._v3.exception import B2Error
from io import BytesIO
from posixpath import join
from mimetypes import guess_type
from utils._compat import string_types
from utils.tool import slash_join


intpl_localhooksetting = """
<div class="layui-col-xs12 layui-col-sm12 layui-col-md6">
    <fieldset class="layui-elem-field layui-field-title" style="margin-bottom: auto">
        <legend>
            BackBlaze B2（{% if "up2b2" in g.site.upload_includes %}使用中{% else
            %}未使用{% endif %}）
        </legend>
        <div class="layui-field-box">
            <div class="layui-form-item">
                <label class="layui-form-label"><b style="color: red">*</b> Bucket</label>
                <div class="layui-input-block">
                    <input type="text" name="b2_bucket" value="{{ g.site.b2_bucket }}" placeholder="B2服务的存储桶名称"
                        autocomplete="off" class="layui-input" />
                </div>
            </div>
            <div class="layui-form-item">
                <label class="layui-form-label"><b style="color: red">*</b> keyID</label>
                <div class="layui-input-block">
                    <input type="text" name="b2_kid" value="{{ g.site.b2_kid }}" placeholder="BackBlaze B2 keyID"
                        autocomplete="off" class="layui-input" />
                </div>
            </div>
            <div class="layui-form-item">
                <label class="layui-form-label"><b style="color: red">*</b> 应用密钥</label>
                <div class="layui-input-block">
                    <input type="password" name="b2_key" value="{{ g.site.b2_key }}"
                        placeholder="BackBlaze B2 applicationKey" autocomplete="off" class="layui-input" />
                </div>
            </div>
            <div class="layui-form-item">
                <label class="layui-form-label">
                    <b style="color: red">*</b> 访问域名
                </label>
                <div class="layui-input-block">
                    <input type="url" name="b2_url" value="{{ g.site.b2_url }}" placeholder="B2友好或S3的URL前缀"
                        autocomplete="off" class="layui-input" />
                </div>
            </div>
            <div class="layui-form-item">
                <label class="layui-form-label">存储根目录</label>
                <div class="layui-input-block">
                    <input type="text" name="b2_basedir" value="{{ g.site.b2_basedir }}"
                        placeholder="图片存储到B2的基础目录，默认是根目录" autocomplete="off" class="layui-input" />
                </div>
            </div>
        </div>
    </fieldset>
</div>
"""


def get_bucket_obj()->Bucket:
    kid = g.cfg.b2_kid
    key = g.cfg.b2_key
    name = g.cfg.b2_bucket
    b2_api = B2Api(InMemoryAccountInfo())
    b2_api.authorize_account("production", kid, key)
    return b2_api.get_bucket_by_name(name)


def upimg_save(**kwargs):
    res = dict(code=1)
    try:
        filename = kwargs["filename"]
        stream = kwargs["stream"]
        upload_path = kwargs.get("upload_path") or ""
        if not filename or not stream:
            return ValueError
    except (KeyError, ValueError):
        res.update(msg="Parameter error")
    else:
        bucket = g.cfg.b2_bucket
        kid = g.cfg.b2_kid
        key = g.cfg.b2_key
        dn = g.cfg.b2_url
        b2_basedir = g.cfg.b2_basedir or ""
        if not bucket or not kid or not key or not dn:
            res.update(msg="The b2 parameter error")
            return res
        errmsg = "An unknown error occurred in the program"
        if isinstance(upload_path, string_types):
            if upload_path.startswith("/"):
                upload_path = upload_path.lstrip("/")
            if b2_basedir.startswith("/"):
                b2_basedir = b2_basedir.lstrip("/")
            filepath = join(b2_basedir, upload_path, filename)
            try:
                #: 使用Backblaze官方SDK上传
                b2obj = get_bucket_obj()
                mime_type, _ = guess_type(filename)
                b2file:FileVersion = b2obj.upload_unbound_stream(
                    BytesIO(stream),
                    filepath,
                    content_type=mime_type,
                )
            except B2Error as e:
                res.update(code=500, msg=str(e) or errmsg)
            else:
                src = slash_join(dn, filepath)
                res.update(
                    code=0,
                    src=src,
                    basedir=b2_basedir,
                    fileId=b2file.id_
                )
        else:
            res.update(msg="The upload_path type error")
    return res


def upimg_delete(sha, upload_path, filename, basedir, save_result):
    b2_basedir = g.cfg.b2_basedir or ""
    filepath = join(basedir or b2_basedir, upload_path, filename)
    b2obj = get_bucket_obj()
    b2obj.delete_file_version(save_result["fileId"], filepath)
