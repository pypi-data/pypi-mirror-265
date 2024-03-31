import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()   

project_urls = {
  'Source': 'https://github.com/embzheng/faucet_tool'
}

setuptools.setup(
    name="faucet_tool",
    version="0.1",
    author="embzheng",
    author_email="embzheng@qq.com",
    description="This is a web3 faucet operation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/embzheng/faucet_tool",
    packages=setuptools.find_packages(),
    install_requires=['playwright>=1.42.0','sys','my_logtool','bitbrowser_tool'],    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls = project_urls
)