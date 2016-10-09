push-ip-to-dnspod
============

使用dnspod api将主机IP设置到某个 域名下

`API说明 <https://www.dnspod.cn/docs/info.html>`_

`获取token <https://support.dnspod.cn/Kb/showarticle/tsid/227>`_

crontab.sh中ifconfig需要使用绝对路径, 可以通过 which ifconfig获取

config.py.example
dnspod_api.py
crontab.sh
README.rst

定时脚本(crontab -e), 一分钟同步一次:

::

    * * * * * cd $HOME/push-ip-to-dnspod && bash ip.sh


使用httpdns更新域名对应的ip
https://www.dnspod.cn/httpdns/guide

get_record_ip() 保存的文件保存(时间|ip), 如果时间间隔大于某个值(默认10分钟)更新远程IP


在virtualenv中使用虚拟环境:

.. code:: bash

    #!/usr/bin/bash
    source  $WORKON_HOME/dev/bin/activate  &&  which python
    
-  `网卡启动后执行脚本 <http://unix.stackexchange.com/questions/91245/execute-custom-script-when-an-interface-gets-connected>`_， /etc/network/interface

.. code:: bash

    auto eth0
    iface eth0 inet dhcp
    post-up /home/ubuntu/push-ip-to-dnspod/push-ip.sh

- `mac clear DNS Cache <https://support.apple.com/en-mn/HT202516>`_
