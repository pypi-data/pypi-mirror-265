# 介绍
- telegram转发 修改自:[tgcf](https://github.com/aahnik/tgcf)
- 支持代理设置,如需代理请设置环境变量,例如:`export TG_PROXY="socks5://127.0.0.1:7890"`
- 只支持linux上运行,不支持windows
# 安装示例
```shell
apt install -y python3
RUN sudo apt install -y pipx
RUN pipx ensurepath
pipx install my-tgcf
```
# 使用
1. 设置环境变量 密码:`export PASSWORD="123456"` 可选设置代理:`export TG_PROXY="123456"`
2. `tgw`
3. 浏览器打开:http://localhost:8501