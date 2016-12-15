push-ip-to-dnspod
==================

使用dnspod api将主机IP设置到某个 域名下

push-ip.sh的配置
----------------

默认使用python3， 如果使用python， 将push-ip.sh的下面一行::

    python3 set_record.py 2>&1 | tee -a $LOG_PATH

的python3替换为python， 并安装requests


如果要上传指定网卡的IP, 例如eth0, 将::

    $(which ifconfig) | awk ...

改为::

    $(which ifconfig) eth0 | awk ...


config.py的配置
---------------

复制config.py.example，并完善信息


忘记启动后上传IP信息(推荐)
--------------------------

-  `网卡启动后执行脚本 <http://unix.stackexchange.com/questions/91245/execute-custom-script-when-an-interface-gets-connected>`_ 
  
编辑 /etc/network/interface

.. code-block:: bash

    auto eth0
    iface eth0 inet dhcp
    post-up /home/ubuntu/push-ip-to-dnspod/push-ip.sh

定时任务上传IP信息(不推荐）
--------------------------

.. code::

    * * * * * cd $HOME/push-ip-to-dnspod && bash ip.sh


脚本中ifconfig要使用绝对路径可以用$(which ifconfig), 参见push-ip.sh

- `mac clear DNS Cache <https://support.apple.com/en-mn/HT202516>`_
- `API说明 <https://www.dnspod.cn/docs/info.html>`_
- `获取token <https://support.dnspod.cn/Kb/showarticle/tsid/227>`_
-  `使用httpdns更新域名对应的ip <https://www.dnspod.cn/httpdns/guide>`_
