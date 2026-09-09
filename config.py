from pathlib import Path
from typing import Dict, List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Physical environment
    BASE_DIR: Path = Path(__file__).resolve().parent
    DATA_DIR: Path = Field(
            default=BASE_DIR / "data",
            description="Default root directory of data"
    )

    @property
    def IMAGE_DIR(self) -> Path:
        return self.DATA_DIR / "image"

    @property
    def RECOGNIZED_JSON_DIR(self) -> Path:
        return self.DATA_DIR / "recognized_json"
    
    @property
    def REFACTORED_JSON_DIR(self) -> Path:
        return self.DATA_DIR / "refactored_json"

    @property
    def RESULT_DIR(self) -> Path:
        return self.DATA_DIR / "result"

    # Hyper parameters
    CONFIDENCE_THRESHOLD: float = Field(default=0.5) # TODO
    HEADER_THRESHOLD_FACTOR: float = Field(default=1.5)  # Add desc
    BODY_THRESHOLD_FACTOR: float = Field(default=0.5)

    # Header features
    HEADER_KEYS: List[str] = Field(default_factory=lambda: [
        "检验单号",
        "检验类型",
        "采集时间",
        "报告时间",
        "检测机构",
    ])
    
    DEVIDE_FEATURES: List[str] = Field(default_factory=lambda: [
        "检验项目",
        "测定结果",
        "参考范围",
    ])


