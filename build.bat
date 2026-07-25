@echo off
D:
cd D:\FeatherPen\FeatherPen
call .venv\Scripts\activate
python -m PyInstaller -c -n FeatherPen_V1.0.0 ^
--add-data "web;web" ^
--add-data "assets;assets" ^
--add-data "data;data" ^
--add-data "docs;docs" ^
--add-data "runtime;runtime" ^
--add-data "config.yaml;." ^
--add-data "member_config.json;." ^
--add-data ".env.example;." ^
main.py
pause