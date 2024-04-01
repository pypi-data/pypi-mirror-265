# 介绍
- telegram转发 修改自:[tgcf](https://github.com/aahnik/tgcf)
- 支持代理设置,如需代理请设置环境变量,例如:`export TG_PROXY="socks5://127.0.0.1:7890"`
- 只支持linux上运行,不支持windows
# 在docker alpine-linux上安装
```shell
apk add --no-cache python3
apk add --no-cache pipx
pipx ensurepath
apk add python3-dev
apk add --no-cache g++


pipx install my-tgcf
```
# 使用
1. `tgw`
2. 浏览器打开:http://localhost:8501