
import xml.etree.ElementTree as ET
from edt_project import ProjectContext


class ScheduledJob:
    def __init__(self, objectName: str, edtProject: ProjectContext):
        
        self.project = edtProject

        mdoPath = '{1}src/ScheduledJobs/{0}/{0}.mdo'.format(objectName, edtProject.directory)
        self.mdoFile = mdoPath

    def validate(self) -> bool:

        mdoData = ET.parse(self.mdoFile)

        root = mdoData.getroot();

        methodName = root.find("methodName")
        if methodName != None and methodName.text != None:
            
            methodItems = methodName.text.split('.')

            if self.project.contains(methodItems[0], methodItems[1]) == False:
                print("Ссылка на неизвестный общий модуль в регл. задании: " + methodName.text)
                # TODO: надо грохать весь объект метаданных
                methodName.text = ""

        if self.project.hardRun():
            mdoData.write(self.mdoFile)