# контроллер проекта
from models.database import Database
from models.project import Project
from services.docx_generator import DocxGenerator
from datetime import datetime
from typing import Optional, Dict, Any


class ProjectController:
    def __init__(self):
        # инициализация компонентов
        self.db = Database()
        self.docx_generator = DocxGenerator()
        self.current_project = None

    def save_project(self, name, documentation_type, system_type, deadline,
                     description, functional_requirements, nonfunctional_requirements=None):
        # сохранение проекта

        project = Project(
            name=name,
            doc_type=documentation_type,
            system_type=system_type,
            deadline=deadline,
            description=description,
            func_req=functional_requirements,
            nonfunc_req=nonfunctional_requirements or {}
        )

        project_id = self.db.save_project(project)
        self.current_project = project
        return project_id

    def load_project(self, project_id):
        # загрузка проекта
        project = self.db.load_project(project_id)
        if project:
            self.current_project = project
        return project

    def export_to_docx(self, name, documentation_type, system_type, deadline,
                       description, functional_requirements, nonfunctional_requirements=""):
        # экспорт в DOCX

        output_path = self.docx_generator.generate(
            name=name,
            documentation_type=documentation_type,
            system_type=system_type,
            deadline=deadline,
            description=description,
            functional_requirements=functional_requirements,
            nonfunctional_requirements=nonfunctional_requirements
        )
        return output_path

    def get_all_projects(self):
        # получить все проекты
        return self.db.get_all_projects()

    def delete_project(self, project_id):
        # удалить проект
        if self.current_project and self.current_project.project_id == project_id:
            self.current_project = None
        return self.db.delete_project(project_id)
