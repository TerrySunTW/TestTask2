#!/usr/bin/env python3
import os
import sys
import argparse
import pika
import json


def ParameterValidator(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-TaskServer', required=True, help="TaskServer IP or FQDN. (ex: 10.116.116.108:5672)")
    parser.add_argument('-Port', required=True, help="TaskServer port, (ex: 5672)")
    parser.add_argument('-Github_TaskGit', required=True, help="Github Git for custom script and dockerfile. (ex: https://github.com/TerrySunTW/TestAITask1.git)")
    parser.add_argument('-Github_TaskBranch', required=True, help="Github branch for custom script and dockerfile. (ex: main)")
    parser.add_argument('-DockerFilePath', required=True, help="dockerfile filename for runtime environment, system will using the docker environment to run your script. (ex: docker/)")
    parser.add_argument('-TaskCommand', required=True, help="The commnad you need to run on the disribution system. (ex: python cnn_handwrite.py p1 p2 p3 )")
    parser.add_argument('-ArchiveFolderPath', required=True, help="Archive folderpath(ex:out)")
    parser.add_argument('-ReportFilePath', required=True, help="Report filename(text file in json format). (ex:out/result.txt)")
    parser.add_argument('-Github_TaskResult', required=True, help="Github Git for task archive files. (ex: git@github.com:terrysuntest/DataPool.git)")
    parser.add_argument('-Github_TaskResult_BranchName', required=True, help="Branch Name in Github for task archive files. (ex:p1_p2_p3)")
    args = parser.parse_args(arguments)
    print(args)
    return args

def SendTaskToTaskQueue(args):
    credentials = pika.PlainCredentials('guest', 'guest') 
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = args.TaskServer,port = args.Port,virtual_host = '/',credentials = credentials))
    channel=connection.channel()
    result = channel.queue_declare(queue = 'python-test',durable=True)

    message=json.dumps({
        'Github_TaskGit':args.Github_TaskGit,
        'Github_TaskBranch':args.Github_TaskBranch,
        'DockerFilePath':args.DockerFilePath,
        'TaskCommand':args.TaskCommand,
        'ArchiveFolderPath':args.ArchiveFolderPath,
        'ReportFilePath':args.ReportFilePath,
        'Github_TaskResult':args.Github_TaskResult,
        'Github_TaskResult_BranchName':args.Github_TaskResult_BranchName
        })
    channel.basic_publish(exchange = '',routing_key = 'python-test',body = message)
    print(message)
    connection.close()


def main(arguments):
    ValidatedArgs=ParameterValidator(arguments)
    SendTaskToTaskQueue(ValidatedArgs)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))



