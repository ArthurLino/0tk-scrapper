@echo off
cd "C:\Program Files (x86)\Google\Chrome\Application"
start chrome.exe --remote-debugging-port=8989 --user-data-dir="C:\Users\Usuario\PycharmProjects\chromeData"