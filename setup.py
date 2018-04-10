from cx_Freeze import setup, Executable

setup(
    name = "test",
    version = "1.0",
    description = "test",
    executables = [Executable("CLIENT.py")]
)
