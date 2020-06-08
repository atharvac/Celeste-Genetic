import psutil
import ctypes

kernel32 = ctypes.windll.kernel32
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020

OpenProcess = kernel32.OpenProcess
ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
CloseHandle = ctypes.windll.kernel32.CloseHandle


def getPid(proc_name):
	pid = None
	for proc in psutil.process_iter():
		if proc_name in proc.name():
			pid = proc.pid
	return pid


class ReadMemory:

	def __init__(self):
		self.hProcess = None
		self.dwDesiredAccess = ( PROCESS_QUERY_INFORMATION |
							PROCESS_VM_OPERATION |
							PROCESS_VM_READ |
							PROCESS_VM_WRITE )
		self.bInheritHandle = False

	def createProcessHandler(self, procName, getHandler=False):
		dwProcessID = getPid(procName)
		#print(f"PID : {dwProcessID}")

		if dwProcessID is not None:
			self.hProcess = OpenProcess(self.dwDesiredAccess, self.bInheritHandle, dwProcessID)
		else:
			print("Getting handler failed!")

		if getHandler:
			return self.hProcess

	def closeHandle(self):
		CloseHandle(self.hProcess)


	def readMemory(self, lpBaseAddress, dtype='float'):
		try:
			lpBaseAddress = lpBaseAddress
		
			if dtype == 'float':
				ReadBuffer = ctypes.c_float()
				nSize = ctypes.sizeof(ReadBuffer)
			elif dtype == 'int':
				ReadBuffer = ctypes.c_uint()
				nSize = ctypes.sizeof(ReadBuffer)
			else:
				ReadBuffer = ctypes.c_char_p()
				nSize = len(ReadBuffer.value)

			lpBuffer = ctypes.byref(ReadBuffer)
			lpNumberOfBytesRead = ctypes.c_ulong(0)
			ctypes.windll.kernel32.ReadProcessMemory(
													self.hProcess,
													lpBaseAddress,
													lpBuffer,
													nSize,
													lpNumberOfBytesRead
													)
			#print(f"Bytes Read:{lpNumberOfBytesRead}")
			return ReadBuffer.value
		except (BufferError, ValueError, TypeError):
			self.closeHandle()
			e = 'Handle Closed, Error'
			return e




