import os
import subprocess
import sys

project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_directory)
import config


def createService(serviceName: str):
    strService = f'''[Unit]
Description={serviceName}.py
After=muli-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 {config.usrPath + str(os.path.join(config.path, serviceName + ".py"))}
WorkingDirectory={config.path}
RemainAfterExit=yes
Restart=always

[Install]
WantedBy=multi-user.target'''
    with open(os.path.join(os.path.dirname(__file__), serviceName + ".service"), 'w') as serviceFile:
        serviceFile.write(strService)


def runService(serviceName: str):
    subprocess.run(f'sudo cp {os.path.join(os.path.dirname(__file__), serviceName + ".service")} /etc/systemd/system',
                   shell=True)
    subprocess.run(f'sudo systemctl enable {serviceName}.service', shell=True)
    subprocess.run(f'sudo systemctl restart {serviceName}.service', shell=True)


def restartService(serviceName: str):
    subprocess.run(f'sudo systemctl restart {serviceName}.service', shell=True)


if __name__ == "__main__":
    serviceName = 'main'
    createService(serviceName)
    runService(serviceName)
