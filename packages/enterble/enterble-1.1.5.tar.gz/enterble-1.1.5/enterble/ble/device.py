import struct
import logging
import time
from typing import Awaitable, Callable, Optional, Any

from bleak.backends.device import BLEDevice
from bleak.backends.service import BleakGATTServiceCollection
from bleak.backends.client import BaseBleakClient
from bleak import BleakClient, BleakError


logger = logging.getLogger(__name__)


# 电池电量信息
class SOC(object):
    def __init__(self, soc_cal_call: callable):
        """初始化电量信息

        Args:
            soc_cal_call (callable): 电量计算，自定义算法 回调函数
        """
        self.soc_cal_call = soc_cal_call
        self.source_soc = None
        self.update_time = None
        self.soc_percentage = None

    async def set_soc(self, source_data):
        """设备电量原始数据

        Args:
            source_data (_type_): 电量原始数据
        """
        if self.soc_cal_call:
            self.soc_percentage = await self.soc_cal_call(source_data)
        else:
            self.soc_percentage = source_data
        self.source_soc = source_data
        self.update_time = time.time()

    async def update_soc(self, soc_percentage):
        """更新电量信息

        Args:
            soc_percentage (_type_): 电量百分比
        """
        self.soc_percentage = soc_percentage
        self.update_time = time.time()

    def __str__(self) -> str:
        return 'SOC: remain > %s | time > %s' % (self.soc_percentage, self.update_time)


# 通用设备
class Device(object):

    def __init__(
        self,
        device: BLEDevice,
        disconnected_callback: Optional[Callable[["BaseBleakClient"], None]] = None,
        soc_cal_call: Awaitable = None
    ) -> None:
        """设备初始化

        Args:
            device (BLEDevice): 设备元信息对象(bleak 设备类)
            disconnected_callback (Awaitable, optional): 设备断开回调函数. Defaults to None.
            soc_cal_call (Awaitable, optional): 电量自定义计算回调函数. Defaults to None.
        """
        self.device: BLEDevice = device
        self.disconnected_callback: Optional[Callable[["BaseBleakClient"], None]] = disconnected_callback
        self.soc_col_call: Awaitable = soc_cal_call
        self.soc: SOC = SOC(soc_cal_call)
        self._client: BleakClient = None
        self.connected: bool = False
        logger.info(f'Device initialized: {self}')

    async def set_disconnected_callback(self, callback: callable):
        """设置设备断开回调函数

        Args:
            callback (callable): 设备断开回调函数
        """
        self.disconnected_callback = callback

    async def set_soc_cal_call(self, callback: callable):
        """设置电量自定义计算回调函数

        Args:
            callback (callable): 电量自定义计算回调函数
        """
        self.soc.soc_cal_call = callback

    @property
    def identify(self):
        """设备标识

        Returns:
            _type_: 设备标识: Win 为 MAC 地址; macOS 为 UUID
        """
        return self.device.address

    def __str__(self) -> str:
        return f'{self.device}'

    async def connect(self) -> None:
        """连接设备"""
        logger.info(f'Connecting to {self}')
        self._client = BleakClient(
            address_or_ble_device=self.identify,
            disconnected_callback=self.disconnected_callback,
        )
        await self._client.connect()
        self.connected = True
        logger.info(f'Connected to {self}')

    async def disconnect(self) -> None:
        """断开设备"""
        logger.info(f'Disconnecting from {self}')
        if self._client:
            await self._client.disconnect()
        self.connected = False
        logger.info(f'Disconnected from {self}')

    async def client(self) -> BleakClient:
        """获取设备连接对象"""
        if self._client and self.connected:
            return self._client
        await self.connect()
        return self._client

    async def get_services(self) -> BleakGATTServiceCollection:
        """获取设备所有服务

        Returns:
            BleakGATTServiceCollection: 设备所有服务
        """
        return await (await self.client()).get_services()

    async def get_name(self) -> str:
        """获取设备名称

        Returns:
            str: 设备名称
        """
        name = await self.read_gatt_char('00002A00-0000-1000-8000-00805F9B34FB')
        if name is None:
            return None
        name = struct.unpack('>{}s'.format(len(name)), name)
        return name[0].decode('utf-8')

    async def set_name(self, name: str, response: bool = True) -> None:
        """写入设备名称

        Args:
            name (str): 新设备名称
            response (bool, optional): 是否回显. Defaults to True.
        """
        name = struct.pack('>s', name.encode('utf-8'))
        await self.write_gatt_char('00002A00-0000-1000-8000-00805F9B34FB', name, response)

    async def get_model(self) -> str:
        """获取设备类型

        Returns:
            str: 设备类型
        """
        model = await self.read_gatt_char('00002A01-0000-1000-8000-00805F9B34FB')
        if model is None:
            return None
        model = struct.unpack('>{}s'.format(len(model)), model)
        return model[0].decode('utf-8')

    async def get_connect_params(self) -> Any:
        """获取设备连接参数

        Returns:
            str: 设备连接参数
        """
        params = await self.read_gatt_char('00002A04-0000-1000-8000-00805F9B34FB')
        if params is None:
            return None
        params = struct.unpack('>{}s'.format(len(params)), params)
        return params[0]

    async def get_soc(self) -> SOC:
        """获取设备电量信息

        Returns:
            SOC: 设备电量信息
        """
        soc = await self.read_gatt_char('00002A19-0000-1000-8000-00805F9B34FB')
        if soc is None:
            return None
        soc = struct.unpack('>B', soc)
        await self.soc.set_soc(soc[0])
        return self.soc

    async def get_mac_address(self) -> str:
        """获取设备 MAC 地板

        Returns:
            str: MAC 地址
        """
        MAC = await (await self.client()).read_gatt_char('00002A24-0000-1000-8000-00805F9B34FB')
        if MAC is None:
            return None
        MAC = [bytes([b]).hex() for b in struct.unpack('>6B', MAC)]
        MAC.reverse()
        return ':'.join(MAC)

    async def get_serial_number(self) -> str:
        """获取设备序列号

        Returns:
            str: 序列号
        """
        serial = await self.read_gatt_char('00002A25-0000-1000-8000-00805F9B34FB')
        if serial is None:
            return None
        serial = struct.unpack('>{}s'.format(len(serial)), serial)
        try:
            return serial[0].decode('utf-8')
        except UnicodeDecodeError:
            return None

    async def get_firmware_version(self) -> str:
        """获取设备固件版本

        Returns:
            str: 固件版本
        """
        version = await self.read_gatt_char('00002A26-0000-1000-8000-00805F9B34FB')
        if version is None:
            return None
        version = struct.unpack('>{}s'.format(len(version)), version)
        return version[0].decode('utf-8')

    async def get_hardware_version(self) -> str:
        """获取设备硬件版本

        Returns:
            str: 硬件版本
        """
        version = await self.read_gatt_char('00002A27-0000-1000-8000-00805F9B34FB')
        if version is None:
            return None
        version = struct.unpack('>{}s'.format(len(version)), version)
        return version[0].decode('utf-8')

    async def get_manufacturer(self) -> str:
        """获取设备制造商信息

        Returns:
            str: 制造商信息
        """
        manufacturer = await self.read_gatt_char('00002A29-0000-1000-8000-00805F9B34FB')
        if manufacturer is None:
            return None
        manufacturer = struct.unpack('>{}s'.format(len(manufacturer)), manufacturer)
        return manufacturer[0].decode('utf-8')

    async def start_notify(self, char_specifier: str, callback: callable) -> None:
        """开始通知

        Args:
            char_specifier (str): 设备特征值
            callback (callable): 回调函数
        """
        await (await self.client()).start_notify(char_specifier, callback)

    async def stop_notify(self, char_specifier: str) -> None:
        """停止通知

        Args:
            char_specifier (str): 设备特征值
        """
        await (await self.client()).stop_notify(char_specifier)

    async def write_gatt_char(self, char_specifier: str, data: bytes, response: bool = True) -> None:
        """写入设备特征值

        Args:
            char_specifier (str): 设备特征值
            data (bytes): 数据
            response (bool, optional): 是否回显. Defaults to True.
        """
        try:
            await (await self.client()).write_gatt_char(char_specifier, data, response)
        except Exception as e:
            logger.error(f'Error writing to {self}: {e}')

    async def read_gatt_char(self, char_specifier: str) -> bytes:
        """读取设备特征值

        Args:
            char_specifier (str): 设备特征值

        Returns:
            bytes: 数据
        """
        try:
            data = await (await self.client()).read_gatt_char(char_specifier)
        except BleakError as e:
            logger.error(f'Error reading {char_specifier}: {e}')
            return None
        return data
