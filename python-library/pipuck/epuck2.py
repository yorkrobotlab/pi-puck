from typing import Optional
from .epuck import EPuck


class EPuck2(EPuck):
	"""Class for interfacing with an e-puck2 robot"""

	def __init__(self, i2c_bus: Optional[int] = None, i2c_address: Optional[int] = None):
		super().__init__(i2c_bus, i2c_address)
		print("e-puck2 not yet implemented")
