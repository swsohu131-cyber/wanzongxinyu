@echo off
chcp 65001 >nul
echo ========================================
echo   万宗心悟AI疗愈智能体 - 一键启动
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查Docker状态...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] Docker未启动，请先启动Docker Desktop
    pause
    exit /b 1
)

echo [2/3] 构建前端...
cd ..
cd frontend
call npm install
call npm run build
if %errorlevel% neq 0 (
    echo [错误] 前端构建失败
    pause
    exit /b 1
)
cd ..
cd docker

echo [3/3] 启动所有服务...
docker-compose up -d

echo.
echo ========================================
echo   服务启动中，请等待...
echo ========================================
echo.
echo 等待数据库就绪...
timeout /t 15 /nobreak >nul

echo 启动完成！
echo.
echo 访问地址：
echo   - 用户端界面: http://localhost
echo   - 管理后台:   http://localhost/admin
echo   - API文档:    http://localhost:8000/docs
echo.
docker-compose ps
echo.
pause
