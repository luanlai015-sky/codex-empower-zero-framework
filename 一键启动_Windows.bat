@echo off
chcp 65001 >nul
echo ===================================================
echo   Codex Empower Zero Framework - 启动引导
echo ===================================================
echo 正在检查并自动安装依赖库 (可能会花费几十秒)...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo 依赖安装完成，正在为您在浏览器中打开应用...
echo (请勿关闭此黑色终端窗口)
echo.

streamlit run app.py

pause