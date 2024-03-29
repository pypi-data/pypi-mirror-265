# Enter BLE SDK For PC

## 简介

Enter BLE SDK For PC 是[回车科技](https://www.entertech.cn/)提供的，适配回车科技蓝牙芯片的 PC 端 SDK。本 SDK 使用 Python 语言开发，可以在 macOS、Linux、Win 下运行。

## 安装

`pip install enterble`

## 功能

1. 搜索蓝牙设备
2. 连接蓝牙设备
3. 与蓝牙设备通信
4. 回车科技 Flowtime 系列芯片数据交互适配

## 使用

查看 [examples](https://github.com/Entertech/Enter-Biomodule-BLE-PC-SDK/tree/main/examples)

### 指引
1. 打开扫描设备
    - `loop.run_until_complete(device_discover())`
2. 运行 simple.py 
3. 观察设备扫描情况
4. 修改设备唯一 ID 为你扫到的自己的设备（macOS 系统用 UUID、Win 系统用 MAC 地址）
    - ```python
      device_identify = (
          "d2:ab:3f:c9:37:ad"
          if platform.system() != "Darwin"
          else "D5D4362A-1690-4204-B797-3015EEDB510E"
      )
      ```
5. 打开采集数据的代码
    - `loop.run_until_complete(data_collector())`
6. 运行 simple.py

Simple:

```python
import asyncio
import sys
import logging
import platform
from typing import List

from bleak.backends.client import BaseBleakClient

from enterble import DeviceScanner, FlowtimeCollector


if sys.version_info < (3, 7):
    asyncio.get_running_loop = asyncio._get_running_loop


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


def bleak_log(level=logging.INFO):
    import bleak
    logger.info(f'Bleak version: {bleak.__version__}')
    logging.getLogger('bleak').setLevel(level=level)


async def device_discover():
    """设备扫描器：扫描设备并获取设备 MAC 信息等

    Raises:
        Exception: 设备未发现
    """
    devices = await DeviceScanner.discover(
        name=None,
        model_nbr_uuid='0000ff10-1212-abcd-1523-785feabcd123',
    )
    if not devices:
        raise Exception('No device found, please try again later.')

    for device in devices:
        try:
            services = await device.get_services()
            for _id, service in services.characteristics.items():
                logger.info(f'{device} - {_id} - {service}')
            MAC = await device.get_mac_address()
            logger.info(
                f'{device} - {MAC}'
            )
        except Exception as e:
            logger.error(f'{device} - {device.identify} - {e}')


async def data_collector():
    """数据采集器：采集数据并输出到日志"""

    async def device_disconnected(device: BaseBleakClient) -> None:
        """设备断开回调函数

        Args:
            device (BaseBleakClient): 设备实例
        """
        logger.info(f'Device disconnected: {device}')

    async def soc_callback(soc: float) -> None:
        """电池电量回调函数

        Args:
            soc (float): 电池电量
        """
        logger.info(f'Battery SOC: {soc}')
        logger.info(f'SOC: {soc}')
        pass

    async def wear_status_callback(wear_status: bool) -> None:
        """佩戴状态回调函数

        Args:
            wear_status (bool): 佩戴状态
        """
        logger.info(f'Wear status: {wear_status}')
        pass

    async def eeg_data_collector(data: List[int]) -> None:
        """EEG 数据采集回调函数

        Args:
            data (List[int]): EEG 数据
        """
        logger.info(f'EEG: {data}')
        pass

    async def hr_data_collector(data: int):
        """HR 数据采集回调函数

        Args:
            data (int): HR 数据
        """
        logger.info(f'HR: {data}')
        pass

    # 设备广播 UUID
    model_nbr_uuid = '0000ff10-1212-abcd-1523-785feabcd123'

    # 设备唯一 ID（可以通过扫描设备确认）
    device_identify = (
        "d2:ab:3f:c9:37:ad"
        if platform.system() != "Darwin"
        else "D5D4362A-1690-4204-B797-3015EEDB510E"
    )

    # 初始化采集器
    collector = FlowtimeCollector(
        name='Flowtime',
        model_nbr_uuid=model_nbr_uuid,
        device_identify=device_identify,
        device_disconnected_callback=device_disconnected,
        soc_data_callback=soc_callback,
        wear_status_callback=wear_status_callback,
        eeg_data_callback=eeg_data_collector,
        hr_data_callback=hr_data_collector,
    )
    # 启动采集器
    await collector.start()
    # 等待结束
    await collector.wait_for_stop()


if __name__ == '__main__':
    bleak_log(logging.INFO)

    loop = asyncio.get_event_loop()
    # 扫描设备
    # loop.run_until_complete(device_discover())
    # 采集数据
    loop.run_until_complete(data_collector())

```
