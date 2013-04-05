（以2009级为例）

毕业照
------

    ./graduation_photo.sh

需安装`curl`工具。

学位照
------

    python ./degree_photo.py

依赖[gevent](http://www.gevent.org/)和[Requests](http://docs.python-requests.org/en/latest/)。脚本默认会读取`students.txt`文件中的学号姓名列表（逗号分隔），默认下载小图片至`xwz`目录下。
