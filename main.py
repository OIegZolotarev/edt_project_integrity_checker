#!/usr/bin/python3

import os
import argparse
import shutil
from edt_project import ProjectContext

from EventSubscription import EventSubscirpiton
from ScheduledJob import ScheduledJob

# TODO: проверки дублей идентификаторов метаданных


def checkProject(args):

    context = ProjectContext(args.directory, args.hardrun)
    
        
    for objectClass in context.objects:
        checkStrayObjects(objectClass, context)
        checkMissingMDOFiles(objectClass, context)


    if 'EventSubscription' in context.objects:
        eventSubscriptions = context.objects['EventSubscription']

        for ES in eventSubscriptions:
            sub = EventSubscirpiton(ES, context)
            sub.validate()
                
    if 'ScheduledJob' in context.objects:
        scheduledJobs = context.objects['ScheduledJob']

        for sjName in scheduledJobs:
            sj = ScheduledJob(sjName, context)
            sj.validate()
                                
 
    pass

def checkMissingMDOFiles(objectClass: str, context: ProjectContext):

    classDir = context.getClassDirectory(objectClass)
    classDirItems = os.listdir(classDir)

    for item in classDirItems:

        # TODO: проверить наличие объекта в Configuration.mdo и удалить если его там нет.

        fullPath = (classDir + '/' + item)
        mdoPath = fullPath + "/" + item + ".mdo"

        if os.path.isfile(mdoPath) == False:
            if context.contains(objectClass, item):
                print("!!! Объект {0}.{1} без файла .mdo, но есть в Configuration.mdo - возможно проект серьезно поврежден".format(objectClass, item))
            else:
                print("Объект {0}.{1} без файла .mdo и удален".format(objectClass, item))

                if context.hardRun():
                    fullPath = (classDir + '/' + item)
                    shutil.rmtree(fullPath)

        pass

    pass

def checkStrayObjects(objectClass: str, context: ProjectContext):

    classDir = context.getClassDirectory(objectClass)
    classDirItems = os.listdir(classDir)

    for item in classDirItems:
        
        if not context.contains(objectClass, item):
            print("Объект не описан в Configuration.mdo: {0} -> {1}".format(objectClass, item))

            if context.hardRun():

                fullPath = (classDir + '/' + item)
                shutil.rmtree(fullPath)
                
                pass
            


parser = argparse.ArgumentParser(
                    prog = 'Проверка логической целостности проекта EDT',
                    description = 'Анализирует файлы проекта на предмет очевидных ошибок. Крайне рекомендуется использовать репозиторий, для контроля изменений',
                    epilog = '')

parser.add_argument('-d', '--directory')      # option that takes a value
parser.add_argument('-hard', '--hardrun', default=False, action='store_true', help="Финишный прогон")      # option that takes a value
args = parser.parse_args()


if args.directory != None:
    checkProject(args)