from setuptools import setup, find_packages

setup(
    name="rtthread_micropython",  # 包名
    version="0.1",               # 版本号
    description="RT-Thread MicroPython Project",  # 项目描述
    author="Your Name",          # 作者
    author_email="your.email@example.com",  # 作者邮箱
    url="https://github.com/yourusername/yourproject",  # 项目主页
    packages=find_packages(where='src'),  # 包含src目录下的所有包
    package_dir={'': 'src'},    # 设定源码目录
    install_requires=[
        "watchdog",
        "requests",
        "opencv-python",
        "Pillow",
        "libcamera",
    ],
    include_package_data=True,  # 包含其他文件，如docs中的文档
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',   # 支持的Python版本
    package_data={
        '': ['*.md'],  # 包含文档文件
    },
)
