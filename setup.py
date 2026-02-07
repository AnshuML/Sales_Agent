"""
Multi-Agent Sales Analysis System
==================================

A conversational AI system for intelligent sales data analysis.
"""

from setuptools import setup, find_packages

setup(
    name="multi-agent-sales-analysis",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Multi-agent sales analysis system with LLM + function hybrid approach",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/multi-agent-sales-analysis",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "langchain-google-genai>=1.0.0",
        "langgraph>=0.0.20",
        "google-generativeai>=0.3.2",
        "pandas>=2.1.4",
        "numpy>=1.26.2",
        "openpyxl>=3.1.2",
        "xlrd>=2.0.1",
        "google-auth>=2.25.2",
        "google-auth-oauthlib>=1.2.0",
        "google-auth-httplib2>=0.2.0",
        "google-api-python-client>=2.111.0",
        "boto3>=1.34.26",
        "matplotlib>=3.8.2",
        "seaborn>=0.13.0",
        "scipy>=1.11.4",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.23.2",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sales-agent=sales_agent.main:main",
        ],
    },
)
