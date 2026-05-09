import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 1. 基础路径锚点 (自动定位到 config.py 所在目录的上一级/根目录)
    BASE_DIR: Path = Path(__file__).resolve().parent
    
    # 2. 核心参数 (带有默认值，.env 可覆盖)
    PROJECT_NAME: str = "Medical_OCR_Refactor"
    DEBUG: bool = True
    
    # 3. 动态路径 (不要在 .env 里写路径，在这里算)
    @property
    def DATA_DIR(self) -> Path:
        return self.BASE_DIR / "data"
    
    @property
    def PROCESSED_DIR(self) -> Path:
        d = self.DATA_DIR / "processed"
        # 自动创建目录，防止报错（防御性编程）
        d.mkdir(parents=True, exist_ok=True)
        return d

    # 4. 配置加载规则
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # 忽略 .env 里多余的字段
    )

# 实例化单例
settings = Settings()

# 简单的自检代码
if __name__ == "__main__":
    print(f"Project: {settings.PROJECT_NAME}")
    print(f"Data Root: {settings.DATA_DIR}")
    print(f"Processed Dir Exists: {settings.PROCESSED_DIR.exists()}")
