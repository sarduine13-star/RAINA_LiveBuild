@echo off
title RAINA Local
call venv\Scripts\activate
uvicorn main:app --reload
pause
