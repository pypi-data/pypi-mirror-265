# distributed-logging
# 概括

当前logging包只支持linux平台。

若需要再windows平台使用，请安装pywin32包，如：pip install pywin32

## 说明
本包名字为*distributed-logging*,使用方法包括...

### 打包方法

python setup.py sdist

twine upload dist\distributed-logging-1.0.1.tar.gz -r nexus

### 安装方法

### 参数说明

### 使用说明
import traceback
import logging.config

config = ProjectConfig.get_object(env_type="development")
logging_plus = getattr(config, "logging")
logging.config.dictConfig(logging_plus)
logger = logging.getLogger("root")

logger.error(traceback.format_exc())

### 错误反馈
