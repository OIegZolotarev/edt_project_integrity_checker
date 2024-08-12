import os
import argparse
import shutil
from edt_project import ProjectContext


def checkProject(projectDir:
                  str):

    projectMetaData = ProjectContext(projectDir)
        
    for objectClass in projectMetaData.objects:
        checkStrayObjects(objectClass, projectMetaData)


    pass

def checkStrayObjects(objectClass: str, projectMetadata: ProjectContext):

    classDir = projectMetadata.getClassDirectory(objectClass)
    classDirItems = os.listdir(classDir)

    for item in classDirItems:
        
        if not projectMetadata.contains(objectClass, item):
            print("Объект не описан в Configuration.mdo: {0} -> {1}".format(objectClass, item))

            if item.startswith("Удалить") or item.startswith("Драйвер"):
                print(" Удаляем: {0}.{1}".format(objectClass, item))
                fullPath = (classDir + '/' + item)
                shutil.rmtree(fullPath)


parser = argparse.ArgumentParser(
                    prog = 'Проверка логической целостности проекта EDT',
                    description = 'Анализирует файлы проекта на предмет очевидных ошибок',
                    epilog = '')

parser.add_argument('-d', '--directory')      # option that takes a value
args = parser.parse_args()


if args.directory != None:
    checkProject(args.directory)