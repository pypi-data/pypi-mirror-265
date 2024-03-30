# lazyOfAPI

> 一个简单的用于请求OpenFrp API的库
>
隧道信息相关参数名称及内容类型请参阅[OpenFrp的官方文档](https://github.com/ZGIT-Network/OPENFRP-APIDOC?tab=readme-ov-file#openfrp-openapi-%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97)
>
> 本文档遵循CC BY-NC-SA许可.

`OpenFrpAPI` 类提供了一个 Python 接口，用于与 OpenFrp 服务进行交互，允许用户管理他们的 FRP（快速反向代理）隧道。

## 初始化 OpenFrpAPI

创建 `OpenFrpAPI` 类的实例，用于后续的 API 调用。

## 用户登录回调

### oauth_login_callback

用户登录回调，用于验证用户名和密码。

| 参数       | 类型  | 描述  |
|----------|-----|-----|
| username | str | 用户名 |
| password | str | 密码  |

返回值：登录成功返回 `True`，否则返回 `False`。

## 获取 OAuth 认证码

### oauth_get_code

获取 OAuth 认证码，用于进一步的用户认证。

返回值：成功获取返回 `True`，否则返回 `False`。

## 使用认证码登录

### oauth_code_login

使用获取到的认证码进行登录。

返回值：登录成功返回 `True`，否则返回 `False`。

## 用户登录

### login

用户登录，通过用户名和密码登录 OpenFrp 服务。

| 参数       | 类型  | 描述  |
|----------|-----|-----|
| username | str | 用户名 |
| password | str | 密码  |

返回值：登录成功返回 `True`，否则返回 `False`。

## 获取用户信息的原始数据

### get_user_info_raw

获取用户信息的原始数据。

返回值：用户信息的字典。

## 获取格式化后的用户信息

### get_user_info

获取格式化后的用户信息。

返回值：格式化后的用户信息字符串。

## 获取用户的隧道列表

### get_user_proxies

获取用户的隧道列表。

返回值：隧道信息的列表。

## 创建新的隧道

### new_proxy

创建新的隧道。

| 参数            | 类型                     | 描述     |
|---------------|------------------------|--------|
| node_id       | int                    | 节点 ID  |
| name          | str                    | 隧道名称   |
| protocol_type | Union[str, ProxyTypes] | 隧道协议类型 |
| local_addr    | str                    | 本地地址   |
| local_port    | int                    | 本地端口   |
| remote_port   | int                    | 远程端口   |
| encrypt       | bool                   | 是否加密   |
| compress      | bool                   | 是否压缩   |
| domain        | str                    | 绑定域名   |
| route         | str                    | 路由     |
| host          | str                    | 主机重写   |
| request_from  | str                    | 请求来源   |
| request_pass  | str                    | 请求密码   |
| custom        | str                    | 自定义参数  |

返回值：创建成功返回 `True`，否则返回 `False`。

## 删除隧道

### remove_proxy

删除隧道。

| 参数       | 类型  | 描述    |
|----------|-----|-------|
| proxy_id | str | 隧道 ID |

返回值：删除成功返回 `True`，否则返回 `False`。

## 获取节点列表

### get_node_list

获取节点列表。

| 参数       | 类型   | 描述     |
|----------|------|--------|
| classify | int  | 目标节点地区 |
| group    | list | 目标用户组  |

返回值：节点列表。